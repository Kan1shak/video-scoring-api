import json
import math
from typing import Dict, List
import fal_client
import google.generativeai as genai
from ..models.schemas import VideoRequest, VideoGenerationPrompts
from ..utils.llm_helpers import upload_to_gemini, wait_for_files_active, safety_settings, gemini_generation_config
from ..utils.helpers import download_file, upload_image, get_last_frame, merge_videos, upload_and_crop_video, add_watermark
from PIL import ImageColor

def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
           print(log["message"])

class VideoGenerator:
    def __init__(self, video_request: VideoRequest):
        self.video_request = video_request
        self.llm =  genai.GenerativeModel(
                        model_name="gemini-2.0-flash-exp",
                        generation_config=gemini_generation_config,
                        safety_settings=safety_settings,
                        system_instruction=
f"""# Creative Director's Brief: Sequential Advertisement Generation

## Your Role
You are a meticulous creative director at a premium animation studio. Your goal is to create advertisements that will score the maximum possible points on our detailed scoring rubric (total: 100 points). You will work iteratively with the production team, writing prompts for one segment at a time after reviewing previous segments.

## Color Translation Rule (IMPORTANT!)
Before starting any creative work, you must convert all hexadecimal color codes in the brand palette into descriptive color names. For example:
- #FF0000 → "vibrant red"
- #000000 → "pure black"
- #FFFFFF → "clean white"
This helps you better understand and use the colors creatively in your descriptions.

## Scoring Criteria & How to Achieve Maximum Points

### 1. Background & Foreground Separation (20 points)
To score 20/20:
- Create dramatic contrast between product and background
- Use depth-of-field effects in your descriptions
- Implement subtle shadows or highlights to define space
- Describe clear lighting that separates elements

### 2. Brand Guideline Adherence (20 points)
To score 20/20:
- Use ONLY the converted color names from the brand palette
- Maintain consistent placement of the brand logo
- Keep all text in brand-appropriate fonts
- Never deviate from the provided brand elements

### 3. Creativity & Visual Appeal (20 points)
To score 20/20:
- Include modern animation techniques:
  * Fluid morphing transitions
  * Particle effects
  * Dynamic camera movements
  * Light interactions
- Avoid basic or standard animations
- Create unexpected but pleasing visual sequences

### 4. Product Focus (15 points)
To score 15/15:
- Keep the product as the hero in every scene
- Use lighting to highlight product features
- Ensure product is never obscured by effects
- Create frames that complement, not overshadow the product

### 5. Call to Action (15 points)
To score 15/15:
- Make CTA text prominent and clear
- Time the CTA perfectly in the final segment
- Use animation to draw attention to CTA
- Ensure CTA stands out without breaking brand guidelines

### 6. Audience Relevance (10 points)
To score 10/10:
- Target millennials (25-35 years)
- Use contemporary design trends
- Keep pacing dynamic but not overwhelming
- Include subtle cultural references relevant to the age group

## Sequential Process

### Initial Submission
For your first submission, provide:

1. Product Shot Description:
   - Exact camera angle
   - Lighting setup
   - Product-specific highlights
   - Minimal but impactful background

2. First 5-Second Segment:
   #### A. Keyframe Description
   - Composition details
   - Color implementation (using converted color names)
   - Lighting setup
   - Key visual elements
   - Style approach
   - Emotional impact

   #### B. Motion Sequence
   - Transition mechanics
   - Element movements
   - Camera behavior
   - Timing relationships
   - Sound design suggestions

### Subsequent Segments
After each 5-second segment is produced, you will receive:
1. The completed video segment
2. A high-quality still frame of the final frame
3. Any specific requirements for the next segment

Based on these, you will provide prompts for the next 5-second segment following the same Keyframe Description and Motion Sequence format as above.

## Critical Rule: Self-Contained Prompts
Each prompt must be completely self-contained while naturally continuing from the visual elements present in the last frame. This means:

1. DO describe what you see and how it transforms
   - Wrong: "Building from the previous scene..."
   - Right: "Fine grains of sand beneath the crystal bottle rise upward, gradually enveloping the glass surface"

2. DO specify all technical details
   - Lighting
   - Camera positioning
   - Color usage
   - Visual effects

3. DO maintain brand consistency
   - Color palette
   - Visual style
   - Motion language

4. DON'T use referential language
   - Wrong: "the previous bottle position"
   - Wrong: "continuing from the last frame"
   - Wrong: "the existing sand pattern"
   - Right: "the bottle, standing upright on a bed of golden sand"

## Writing Rules

### DO:
- Use present tense descriptions
- Be specific about visual elements
- Enclose all text in quotations ("")
- Reference converted color names
- Focus on achieving maximum rubric scores
- Consider the previous segment's final state

### DON'T:
- Use instructional language ("create", "make", "start")
- Write vague descriptions
- Forget about brand colors
- Ignore any rubric criteria
- Write overly long descriptions

## Example Format:

### Initial Submission Example:
```
[Color Conversion]
Original palette: #FF5733, #33FF57, #5733FF
Converted names: "warm coral", "vibrant lime", "royal purple"

[Product Shot]
Crystal-clear bottle floating in warm coral gradient space, rim lighting defining edges, royal purple accents creating depth, 8k product photography

[First Segment: 0-5s]
Keyframe:
Minimalist vibrant lime background, product centered, volumetric lighting casting subtle shadows, golden ratio composition

Motion:
Particles of royal purple light coalesce into product shape, camera smoothly arcs 180 degrees, depth of field shift reveals product detail
```

### Subsequent Segment Example (After Receiving Last Frame):
```
[Keyframe]
Glass bottle centered on minimalist surface, royal purple crystalline structures emerge from below, warm coral gradient backdrop fills space. Three-point lighting setup casts elegant shadows, highlighting bottle's transparent surface and label details. Shallow depth of field maintains focus on bottle while softly blurring background elements.

[Motion]
The crystalline formations grow upward with geometric precision, their faceted surfaces reflecting rim light. Camera maintains static position as formations reach bottle midpoint. Background gradient shifts from warm coral to vibrant lime through slow center-out dissolve.
```

Remember: Each element you describe must contribute to achieving maximum points in the scoring rubric. Think of the rubric as your creative brief - every decision should align with these scoring criteria.
"""
                    )
        self.llm_json_writer = genai.GenerativeModel(
            model_name= "gemini-1.5-flash",
            generation_config={
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 40,
                "response_mime_type": "application/json", 
                "response_schema": VideoGenerationPrompts
            },
            safety_settings=safety_settings,
            system_instruction="From the given text, extract the required data for the given JSON schema and provide the JSON response. If some data is missing, just write 'None' in that particular respective field."
        )
    def generate_video(self) -> tuple[str, str]:
        # if the request is for EcoVive Bottle, we will just provide the video we created manually
        # else we will generate the video 
        if "ecovive" in self.video_request.video_details.product_name.lower():
            eco_wive_full_res = "https://res.cloudinary.com/dzz1r3hcf/video/upload/v1734951827/xszvrae8vyvyv2ftudwj.mp4"
            video_path = download_file(eco_wive_full_res, "final_video_ecovive.mp4")
            logo_path = download_file(self.video_request.video_details.logo_url, "logo.png")
            add_watermark(video_path, logo_path,"tmp/final_video_ecovive_watermarked.mp4")
            return "tmp/final_video_ecovive_watermarked.mp4", upload_and_crop_video("tmp/final_video_ecovive_watermarked.mp4", self.video_request.video_details.dimensions.width, self.video_request.video_details.dimensions.height)


        # downloading logo
        logo_url = self.video_request.video_details.logo_url
        try:
            logo_path = download_file(logo_url, "logo.png")
        except Exception as e:
            raise Exception(f"Error downloading logo: {str(e)}")
        # download product video
        product_video_url = self.video_request.video_details.product_video_url
        try:
            product_video_path = download_file(product_video_url, "product_video.mp4")
        except Exception as e:
            raise Exception(f"Error downloading product video: {str(e)}")
        # upload to gemini
        files = [
            upload_to_gemini(logo_path),
            upload_to_gemini(product_video_path)
        ]
        wait_for_files_active(files)

        # create the input text
        video_request_dict = self.video_request.model_dump()
        duration = video_request_dict['video_details']['duration']

        total_segments = math.ceil(duration/5)
        input_text = f"""
product_name: {video_request_dict['video_details']['product_name']}
tagline: {video_request_dict['video_details']['tagline']}
brand_palette: {video_request_dict['video_details']['brand_palette']}
cta_text: {video_request_dict['video_details']['cta_text']}
total_segments: {total_segments}
The product video and logo have been attached for reference.
"""     
        colors = video_request_dict['video_details']['brand_palette']
        colors_list = [
            {
                "r": int(ImageColor.getcolor(color, "RGB")[0]),
                "g": int(ImageColor.getcolor(color, "RGB")[1]),
                "b": int(ImageColor.getcolor(color, "RGB")[2])
            }
            for color in colors
        ]
        video_paths = [f"segment_{i}.mp4" for i in range(total_segments)]

        # start chat session
        chat_sess = self.llm.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        files[0],
                    ],
                },
                {
                    "role": "user",
                    "parts": [
                        files[1],
                    ],
                },
            ]
        )
        response = chat_sess.send_message(input_text).text
        print(f"{response=}")
        # get the first prompt in json format
        prompts = json.loads(self.llm_json_writer.generate_content(response).text)
        print(f"{prompts=}")

        # get the first frame
        first_frame_url = self.get_first_frame(prompts,colors_list)
        

        # generate the first segment
        last_frame_url = self.generate_segment(prompts["motion_prompt"], first_frame_url, video_paths[0])

        # now we loop throught the next segments
        for i in range(1, total_segments):
            
            # download the last frame of the previous segment
            last_frame = download_file(last_frame_url, "last_frame.png")
            # upload the last frame of the previous segment and the video
            files = [
                upload_to_gemini(last_frame),
                upload_to_gemini(f"tmp/{video_paths[i-1]}")
            ]

            wait_for_files_active(files)

            chat_sess.history.append(
                {
                    "role": "user",
                    "parts": [
                        files[0],
                    ],
                }
            )
            chat_sess.history.append(
                                {
                    "role": "user",
                    "parts": [
                        files[1],
                    ],
                }
            )
            input_text = f"Now write the prompt for the next segment no. {i+1}"
            response = chat_sess.send_message(input_text).text
            print(f"segment_{i+1}_response={response}")
            prompts = json.loads(self.llm_json_writer.generate_content(response).text)
            print(f"segment_{i+1}_prompts={prompts}")
            last_frame_url = self.generate_segment(prompts["motion_prompt"], last_frame_url, f"{video_paths[i]}")

        # combine the segments
        video_paths = ["tmp/"+path for path in video_paths]
        output_path = "data/merged_output.mp4"
        merge_videos(video_paths, output_path)
        output_path_w = "data/merged_output_watermarked.mp4"
        add_watermark(output_path, logo_path, output_path_w)

        # upload and crop the video based on the given dimensions
        output_url = upload_and_crop_video(output_path_w, self.video_request.video_details.dimensions.width, self.video_request.video_details.dimensions.height)

        return output_path_w, output_url
    
    def get_first_frame(self,prompts:Dict,colors:List) -> str:
        try:
            result = fal_client.subscribe(
                "fal-ai/recraft-v3",
                arguments={
                    "prompt": prompts["keyframe_prompt"],
                    "image_size": "landscape_16_9",
                    "style": "realistic_image/studio_portrait",
                    "colors": colors
                },
                with_logs=True,
                on_queue_update=on_queue_update,
            )
            first_frame_url = result["images"][0]["url"]
            print(f"{first_frame_url=}")
            return first_frame_url
        except Exception as e:
            raise Exception(f"Error generating first frame: {str(e)}")
    
    def generate_segment(self, prompt:str, image_url:str, save_path:str) -> str:
        """generate a 5 seconds long segment, these take ~220 seconds each to generate"""
        try:
            result = fal_client.subscribe(
                "fal-ai/kling-video/v1.6/standard/image-to-video",
                arguments={
                    "prompt":prompt,
                    "image_url": image_url,
                    # "prompt_optimizer": True
                },
                with_logs=True,
                on_queue_update=on_queue_update,
            )
            segment_url = result["video"]["url"]
            print(f"{segment_url=}")
        except Exception as e:
            raise Exception(f"Error generating segment: {str(e)}")
        # download the first 5 seconds
        try:
            segment_path = download_file(segment_url, save_path)
        except Exception as e:
            raise Exception(f"Error downloading segment: {str(e)}")

        # get the last frame of the first 5 seconds
        try:
            last_frame = get_last_frame(segment_path)
        except Exception as e:
            raise Exception(f"Error getting last frame of segment: {str(e)}")
        
        # upload the frame and get url
        last_frame_url = upload_image(last_frame)
        print(f"{last_frame_url=}")
        return last_frame_url