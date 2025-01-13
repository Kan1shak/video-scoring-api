import json
import math
from typing import Dict, List
import fal_client
import google.generativeai as genai
from ..models.schemas import VideoRequest, VideoGenerationPrompts, TextOverlays
from ..utils.llm_helpers import upload_to_gemini, wait_for_files_active, safety_settings, gemini_generation_config
from ..utils.helpers import download_file, upload_image, get_last_frame, merge_videos, upload_and_crop_video, add_watermark, fade_in_text, embed_text_clips
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
                       # model_name="gemini-exp-1206",
                        generation_config=gemini_generation_config,
                        safety_settings=safety_settings,
                        system_instruction=
f"""# Creative Director's Brief: Sequential Advertisement Generation

## Your Role
You are a creative director tasked with writing prompts for a premium video advertisement. You will work sequentially, writing prompts for one segment at a time after reviewing the last frame of the previous segment.

## Color Translation Rule (IMPORTANT!)
Before starting, convert all hexadecimal color codes in the brand palette into descriptive color names. For example:
- #FF0000 → "vibrant red"
- #000000 → "pure black"
- #FFFFFF → "clean white"

## Critical Rules

### 1. Stateless Prompts (MOST IMPORTANT)
Each prompt must be completely self-contained. Never reference other frames or previous states. The artist creating each segment has no knowledge of other segments.

WRONG ❌:
- "The bottle continues rotating"
- "The same particles from before"
- "The existing background"
- "The product moves further"
- "The animation continues"
- "As before, the lighting..."

RIGHT ✓:
- "The VitaBoost Energy Drink bottle rotates clockwise"
- "Royal purple particles surround the LuxeGlow Serum bottle"
- "Warm coral gradient background fills the space"
- "The SunBurst Energy Can moves upward"
- "The GlowMax Cream jar spins 180 degrees"
- "Three-point lighting illuminates the AquaPure bottle"

### 2. Full Product Names
Always use the complete product name in both keyframe and motion prompts. Never use generic terms.

WRONG ❌:
- "The product"
- "The bottle"
- "The container"
- "The drink"
- "The item"
- "The package"
- "It"

RIGHT ✓:
- "VitaBoost Energy Drink bottle"
- "LuxeGlow Serum bottle"
- "SunBurst Energy Can"
- "GlowMax Cream jar"
- "AquaPure Water bottle"

## Key Visual Elements

### Brand Colors
- Use only the converted color names from the brand palette
- Use colors purposefully to create hierarchy and direct attention
- Maintain consistent color application across segments

### Additional Guidelines
- Sometimes the user might provide some additional guidelines. Make sure to write all your prompts based on the given guidelines.
- If no additional guidelines are provided, just ignore this section.


## Video Generation Styles (IMPORTANT!)

IMPORTANT: These styles only apply to MOTION prompts. Keyframes and product shots should remain style-neutral.

### Available Styles:

1. **Hand Drawn**
   - Characteristics: Sketchy, organic, flowing lines with visible strokes
   - Motion should emphasize hand-drawn feeling with:
     * Rough, organic transitions
     * Sketch-like movements
     * Slight wobble or imperfection in motion
     * Hand-drawn effects and particles
   
   Example Motion Prompt:
   ```
   Motion:
   VitaBoost Energy Drink bottle sketches itself into existence with flowing pencil lines, energetic sketch marks swirl around the bottle, rough hand-drawn sparkles pulse outward with each rotation, bottle spins with slightly uneven hand-animated motion
   ```

2. **Handmade 3D**
   - Characteristics: Clay-like, tactile, physically crafted feel
   - Motion should suggest physical manipulation:
     * Clay-morph transitions
     * Stop-motion-style movements
     * Fingerprint-like textures
     * Physically plausible deformations

3. **Realistic Urban Drama**
   - Characteristics: Cinematic, gritty, high-contrast
   - Motion should reflect film-like qualities:
     * Dynamic camera movements
     * Dramatic lighting shifts
     * Urban environment reflections
     * Atmospheric effects like dust or vapor

   Example Motion Prompt:
   ```
   Motion:
   LuxeGlow Serum bottle emerges through cinematic fog, camera tracks dramatically around the bottle with slight handheld shake, urban lights create dynamic reflections across the surface, atmospheric particles catch dramatic rim lighting
   ```

4. **2D Art**
   - Characteristics: Flat, graphic, bold shapes
   - Motion should maintain 2D perspective:
     * Flat plane movements
     * Graphic shape transitions
     * Vector-style effects
     * Clean, precise motions

5. **Pop Art**
   - Characteristics: Bold, vibrant, comic-book style
   - Motion should be energetic and graphic:
     * Comic panel-style transitions
     * Bold color shifts
     * Halftone patterns
     * Graphic effect overlays

6. **Digital Engraving**
   - Characteristics: Fine lines, detailed hatching, etched look
   - Motion should suggest etched precision:
     * Line-by-line reveals
     * Precise, mechanical movements
     * Etched shading effects
     * Technical, detailed transitions

### Style Application Guidelines:
1. Maintain product authenticity while applying style
2. Keep motion consistent with chosen style throughout segment
3. Ensure product features remain clear despite stylistic effects
4. Use style-appropriate effects and transitions
5. Consider style-specific lighting and texturing


## Video Pacing Guidelines

### For Shorter Videos (2-3 segments):
Every segment must contribute significantly to the final message. Don't waste time.

2-Segment Structure Example:
1. Segment 1: Product introduction with dynamic movement
2. Segment 2: Product showcase with final positioning

### For Longer Videos (4+ segments):
Build the story gradually but maintain viewer interest.

6-Segment Structure Example:
1. Segment 1: Atmospheric build-up
2. Segment 2-3: Product showcase with varied angles
3. Segment 4-5: Feature demonstrations
4. Segment 6: Final product presentation

## Required Outputs

### Initial Submission:
1. Product Shot
2. First Segment's Keyframe
3. First Segment's Motion

### Subsequent Segments:
After receiving the last frame of the previous segment:
1. Next Segment's Keyframe
2. Next Segment's Motion

## Post-Production Text Overlays (IMPORTANT!)

IMPORTANT: Text overlay suggestions should ONLY be provided after receiving and reviewing the complete final video. DO NOT provide text suggestions during the segment-by-segment creation process.

### Font Types and Usage
Choose from three font styles based on the text purpose:
1. Normal (Inter): 
   - Use for detailed information, specifications, and secondary messages
   - Best for longer text and clear readability
   - Example: Product features, descriptions

2. Bold (Bebas Neue):
   - Use for impactful headlines and primary messages
   - Perfect for short, attention-grabbing text
   - Example: Brand slogans, main product benefits

3. Stylish (Playfair):
   - Use for premium, elegant messaging
   - Best for brand names and sophisticated copy
   - Example: Brand name, premium product qualities

### Placement Considerations
- Analyze the video to find areas that:
   1. Have minimal motion or activity
   2. Don't contain important product details
   3. Provide clear contrast for text
   4. Won't interfere with key visual elements
- Avoid placing text over:
   1. Main product features
   2. Important visual transitions
   3. Areas with complex motion
   4. Crucial brand elements

### Color Selection Guidelines
- Choose colors in RGB format (r,g,b) that:
   1. Contrast well with the background during the text's duration
   2. Complement the overall color scheme
   3. Ensure readability (check contrast against all backgrounds the text appears over)
   4. Consider using a subtle drop shadow if needed for legibility

### Text Overlay Format
```
[Text Entry #]
Content: "Exact text to display"
Time: Start-End in decimal seconds (e.g., 2.5-4.8)
Position: (X%, Y%) where:
  - X: 0 = left edge, 100 = right edge
  - Y: 0 = top edge, 100 = bottom edge
  Example: (50,50) = center of screen
Font: Specify type (Normal/Bold/Stylish)
Color: RGB values in format (r,g,b)
Font Size: Choose from:
  - Small (3% of screen height)
  - Medium (5% of screen height)
  - Large (8% of screen height)
Context: Brief description of what's happening in video during this text
Background Analysis: Description of the background colors/elements during text duration
```

### Example Text Overlay Plan:
```
[Text 1]
Content: "PREMIUM ENERGY"
Time: 0.0-2.5
Position: (50,30)
Font: Bold
Color: (255,255,255)
Font Size: Large
Context: Product emerges from darkness
Background Analysis: Dark gradient background provides strong contrast

[Text 2]
Content: "Made with Natural Spring Water"
Time: 2.8-4.2
Position: (75,50)
Font: Normal
Color: (220,220,220)
Font Size: Medium
Context: Product rotation showing ingredients
Background Analysis: Light blue background, avoiding busy particle effects

[Text 3]
Content: "Elevate Your Experience"
Time: 4.5-6.0
Position: (50,85)
Font: Stylish
Color: (255,215,0)
Font Size: Medium
Context: Final product hero shot
Background Analysis: Clean, dark background in lower third
```
Remember: Each prompt must be self-contained and use full product names. Never reference other frames or use generic terms.
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
            system_instruction="From the given text, extract the required data for the given JSON schema and provide the JSON response. If some data is missing, just write 'None' in that particular respective field. For the video styles section choose one from 'Hand Drawn', 'Handmade 3D', 'Realistic Urban Drama', '2D Art', 'Pop Art', 'Digital Engraving'."
        )

        self.llm_xml_writer = genai.GenerativeModel(
            model_name= "gemini-2.0-flash-exp",
            generation_config={
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 40,
            },
            safety_settings=safety_settings,
            system_instruction="""From the given text extract the required data in the following xml-like format:
<texts>
  <text>
    <color>
      <!-- Format: rgb(R,G,B) where R,G,B are 0-255 -->
    </color>
    <font>
      <!-- One of: Normal, Bold, Stylish -->
    </font>
    <font_size>
      <!-- One of: small, medium, large -->
    </font_size>
    <position>
      <x>
        <!-- Float value for x coordinate -->
      </x>
      <y>
        <!-- Float value for y coordinate -->
      </y>
    </position>
    <content>
      <!-- String content -->
    </content>
    <text_duration>
      <start>
        <!-- Float value for start time in seconds -->
      </start>
      <end>
        <!-- Float value for end time in seconds -->
      </end>
    </text_duration>
  </text>
</texts>
"""
        )
        self.llm_json_text_overlay_writer = genai.GenerativeModel(
            model_name= "gemini-2.0-flash-exp",
            generation_config={
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 40,
                "response_mime_type": "application/json", 
                "response_schema": TextOverlays
            },
            safety_settings=safety_settings,
            system_instruction="From the given text, extract the required data for the given JSON schema and provide the JSON response. If some data is missing, just write 'None' in that particular respective field. For positions, the text might contain %, but you only need to provide the number as float. Choose font size from 'small', 'medium', 'large'. For font, choose from 'Normal', 'Bold', 'Stylish'. For color, provide RGB values in the format rgb(r,g,b)."
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
additional_guidelines: {video_request_dict['additional_guidelines'] if video_request_dict['additional_guidelines'] else "None"}\
video_style: {video_request_dict['video_style']}
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
        
        # adding textual content
        # we upload the final video to gemini first and get the textual content
        files = [
            upload_to_gemini(output_path_w)
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
        input_text = "Provide the Post-Production Text Overlays for the final video"

        response = chat_sess.send_message(input_text).text
        print(f"text_prompt_{response=}")

        text_xml = self.llm_xml_writer.generate_content(response).text
        print(f"text_xml={text_xml}")

        text_overlays = json.loads(self.llm_json_text_overlay_writer.generate_content(text_xml).text)
        print(f"text_overlays={text_overlays}")

        # generate the final video with text overlays
        output_path_t = "data/merged_output_watermarked_text.mp4"
        self.generate_text_overlay(text_overlays, output_path_w, output_path_t)

        # upload and crop the video based on the given dimensions
        output_url = upload_and_crop_video(output_path_t, self.video_request.video_details.dimensions.width, self.video_request.video_details.dimensions.height)

        return output_path_t, output_url
    
    def get_first_frame(self,prompts:Dict,colors:List) -> str:
        # getting the style
        video_style = self.video_request.video_style
        if "drawn" in video_style.lower():
            style = "digital_illustration/hand_drawn"
        elif "3d" in video_style.lower():
            style = "digital_illustration/handmade_3d"
        elif "urban" in video_style.lower():
            style = "realistic_image/urban_drama"
        elif "2d" in video_style.lower():
            style = "digital_illustration/2d_art_poster"
        elif "pop" in video_style.lower():
            style = "digital_illustration/pop_art"
        elif "engraving" in video_style.lower():
            style = "digital_illustration/digital_engraving"
        else:
            style = "realistic_image/studio_portrait"

        #calculate aspect ratio to be one from 16:9, 9:16, 4:3, 3:4, 1:1
        aspect_ratio = self.video_request.video_details.dimensions.width/self.video_request.video_details.dimensions.height
        if aspect_ratio > 1:
            # choose the closest aspect ratio
            if aspect_ratio > 1.7:
                image_size = "landscape_16_9"
            else:
                image_size = "landscape_4_3"
        elif aspect_ratio < 1:
            if aspect_ratio < 0.6:
                image_size = "portrait_16_9"
            else:
                image_size = "portrait_4_3"
        else:
            image_size = "square_hd"




        try:
            result = fal_client.subscribe(
                "fal-ai/recraft-v3",
                arguments={
                    "prompt": prompts["keyframe_prompt"],
                    "image_size": image_size,
                    "style": style,
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
    
    def generate_text_overlay(self, text_overlays:Dict, video_path:str, output_path:str) -> str:
        text_clips = []
        for text in text_overlays["texts"]:
            text_clip = fade_in_text(video_path, text["text_duration"], text["text"], text["font_size"], text["position"], text["color"], text["font"])
            text_clips.append(text_clip)
        print(f"succesfully generated {len(text_clips)} text clips")
        embed_text_clips(video_path,text_clips, output_path)
        return output_path
