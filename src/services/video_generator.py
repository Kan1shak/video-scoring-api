import json
from typing import Dict
import fal_client
import google.generativeai as genai
from ..models.schemas import VideoRequest, VideoGenerationPrompts
from ..utils.llm_helpers import upload_to_gemini, wait_for_files_active, safety_settings, gemini_generation_config
from ..utils.helpers import download_file, upload_image, get_last_frame, merge_videos, upload_and_crop_video, add_watermark

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
f"""# Creative Director's Brief: High-Scoring 15-Second Advertisement Generation

## Your Role
You are a meticulous creative director at a premium animation studio. Your goal is to create advertisements that will score the maximum possible points on our detailed scoring rubric (total: 100 points).

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

## Required Outputs

### 1. Initial Product Shot
First, create a clean, striking product visualization:
- Describe the exact camera angle
- Detail the lighting setup
- Specify any product-specific highlights
- Keep the background minimal but impactful

### 2. 15-Second Breakdown
Divide into three 5-second segments. For each segment provide:

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

## Critical Rule: Stateless Prompts
Each prompt MUST be completely independent and self-contained. Think of each prompt as being processed by a separate system that has NO KNOWLEDGE of any other prompts you've written. This means:

1. NEVER reference previous prompts
   - Wrong: "The bottle continues rotating"
   - Right: "A glass bottle rotates clockwise, displaying all sides"

2. NEVER use contextual words
   - Wrong: "then", "next", "previously", "continues", "same as before"
   - Right: New, complete description for each prompt

3. NEVER assume inherited properties
   - Wrong: "with the same lighting setup"
   - Right: Fully describe lighting in each prompt

4. ALWAYS restate critical elements
   - Product details
   - Brand colors
   - Key visual elements
   - Camera positioning
   - Lighting setup

## Writing Rules

### DO:
- Use present tense descriptions
- Be specific about visual elements
- Enclose all text in quotations ("")
- Make each prompt self-contained
- Reference converted color names
- Focus on achieving maximum rubric scores

### DON'T:
- Use instructional language ("create", "make", "start")
- Write vague descriptions
- Forget about brand colors
- Ignore any rubric criteria
- Write overly long descriptions
- Assume knowledge from previous prompts

## Example Format:

### BAD Example (Breaking Stateless Rule):
```
[Segment 1]
A bottle appears from particles against a dark background

[Segment 2]
The same bottle continues rotating while the background transitions to blue

[Segment 3]
Finally, the bottle stops spinning and the logo appears next to it
```

### GOOD Example (Stateless Prompts):
```
[Segment 1]
A crystal glass bottle materializes from swirling particles, centered in frame against a deep navy background, warm spotlights highlighting the label, camera positioned at product height

[Segment 2]
A crystal glass bottle rotates 180 degrees against a gradient blue background, three-point lighting setup emphasizes product texture, camera slightly below product level

[Segment 3]
A crystal glass bottle stands upright, brand logo floats independently in golden light beside it, dramatic side lighting creates product shadows, camera at 15-degree upward angle
```

### Complete Format Example:

```
[Color Conversion]
Original palette: #FF5733, #33FF57, #5733FF
Converted names: "warm coral", "vibrant lime", "royal purple"

[Product Shot]
Crystal-clear bottle floating in warm coral gradient space, rim lighting defining edges, royal purple accents creating depth, 8k product photography

[Segment 1: 0-5s]
Keyframe:
Minimalist vibrant lime background, product centered, volumetric lighting casting subtle shadows, golden ratio composition

Motion:
Particles of royal purple light coalesce into product shape, camera smoothly arcs 180 degrees, depth of field shift reveals product detail
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
            system_instruction="From the given text, extract the required data for the given JSON schema and provide the JSON response."
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
        input_text = f"""
product_name: {video_request_dict['video_details']['product_name']}
tagline: {video_request_dict['video_details']['tagline']}
brand_palette: {video_request_dict['video_details']['brand_palette']}
cta_text: {video_request_dict['video_details']['cta_text']}
The product video and logo have been attached for reference.
Some more things you should focus into:
○ Background and Foreground Separation:
	■ Clear and visually distinct separation.
○ Adherence to Brand Guidelines:
	■ Consistency in using brand colors, fonts, and logo.
○ Creativity and Visual Appeal:
	■ Engaging storytelling, transitions, and animations.
○ Product Focus:
	■ Prominence of the product throughout the video.
○ Call-to-Action:
	■ Visibility and placement of the CTA.
○ Audience Relevance:
	■ Appeal to the target audience's values and preferences.
"""
        
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
        # get the prompts in json format
        prompts = json.loads(self.llm_json_writer.generate_content(response).text)
        print(f"{prompts=}")

        # get the first frame
        first_frame_url = self.get_first_frame(prompts)
        
        # generating the segments
        video_paths = ["segment_1.mp4", "segment_2.mp4", "segment_3.mp4"]
        # generate the first segment
        last_frame_url = self.generate_segment(prompts["segment_one_motion"], first_frame_url, video_paths[0])
        # generate the second segment
        last_frame_url = self.generate_segment(prompts["segment_two_motion"], last_frame_url, video_paths[1])
        # generate the last segment
        _ = self.generate_segment(prompts["segment_three_motion"], last_frame_url, video_paths[2])

        # combine the segments
        video_paths = ["segment_1.mp4", "segment_2.mp4", "segment_3.mp4"]
        video_paths = ["tmp/"+path for path in video_paths]
        output_path = "data/merged_output.mp4"
        merge_videos(video_paths, output_path)
        output_path_w = "data/merged_output_watermarked.mp4"
        add_watermark(output_path, logo_path, output_path_w)

        # upload and crop the video based on the given dimensions
        output_url = upload_and_crop_video(output_path_w, self.video_request.video_details.dimensions.width, self.video_request.video_details.dimensions.height)

        return output_path_w, output_url
    
    def get_first_frame(self,prompts:Dict) -> str:
        try:
            result = fal_client.subscribe(
                "fal-ai/ideogram/v2",
                arguments={
                    "prompt": prompts["segment_one_keyframe"],
                    "aspect_ratio": "16:9",
                    "expand_prompt": False,
                    "style": "render_3D"
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
                "fal-ai/minimax/video-01-live/image-to-video",
                arguments={
                    "prompt":prompt,
                    "image_url": image_url,
                    "prompt_optimizer": True
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