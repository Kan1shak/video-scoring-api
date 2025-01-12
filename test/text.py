import json
import sys
from pathlib import Path
from typing import Dict, Tuple
sys.path.append(str(Path(__file__).parent.parent))

import google.generativeai as genai
from src.models.schemas import VideoRequest, VideoGenerationPrompts, TextOverlays
from src.utils.llm_helpers import upload_to_gemini, wait_for_files_active, safety_settings, gemini_generation_config


llm =  genai.GenerativeModel(
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
llm_json_text_overlay_writer = genai.GenerativeModel(
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

output_path_w = "data/merged_output_watermarked.mp4"

# adding textual content
# we upload the final video to gemini first and get the textual content
files = [
    upload_to_gemini(output_path_w)
]
chat_sess = llm.start_chat()
wait_for_files_active(files)
chat_sess.history.append(
    {
        "role": "user",
        "parts": [
            files[0],
        ],
    }
)
input_text = """Provide the Post-Production Text Overlays for the final video, The details are: 
"product_name": "L'Essence Noir Luxury Perfume",
"tagline": "Unveil Your Essence",
"cta_text": "Experience Luxury at LESSENCE.com","""

response = chat_sess.send_message(input_text).text
print(f"text_prompt_{response=}")
json_t = llm_json_text_overlay_writer.generate_content(response).text
print(f"json_t={json_t}")
text_overlays = json.loads(json_t)
print(f"text_overlays={text_overlays}")


json_t={
  "texts": [
    {
      "color": "rgb(255,255,255)",
      "font": "Stylish",
      "font_size": "large",
      "position": {
        "x": 50.0,
        "y": 20.0
      },
      "text": "L'Essence Noir",
      "text_duration": {
        "end": 3.0,
        "start": 0.0
      }
    },
    {
      "color": "rgb(230,230,230)",
      "font": "Normal",
      "font_size": "medium",
      "position": {
        "x": 50.0,
        "y": 30.0
      },
      "text": "Luxury Perfume",
      "text_duration": {
        "end": 6.0,
        "start": 3.0
      }
    },
    {
      "color": "rgb(255,255,255)",
      "font": "Bold",
      "font_size": "large",
      "position": {
        "x": 50.0,
        "y": 80.0
      },
      "text": "Unveil Your Essence",
       "text_duration": {
        "end": 12.0,
        "start": 8.0
      }
    },
    {
      "color": "rgb(200,200,200)",
      "font": "Normal",
      "font_size": "medium",
      "position": {
        "x": 50.0,
        "y": 90.0
      },
      "text": "Experience Luxury at LESSENCE.com",
       "text_duration": {
        "end": 25.0,
        "start": 20.0
      }
    }
  ]
}
from moviepy import TextClip, ImageClip, CompositeVideoClip, ColorClip, VideoClip,VideoFileClip
import moviepy.video.fx as vfx

import colorsys

def get_stroke_color(rgb:Tuple)->Tuple:
    r, g, b = [x/255 for x in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    new_l = max(0, l - 0.2)
    new_r, new_g, new_b = colorsys.hls_to_rgb(h, new_l, s)
    return tuple(round(x * 255) for x in (new_r, new_g, new_b))

def fade_in(video_path:str, duration:Dict, content:str, size:str, position:Dict, color:str, font:str) -> None:
    font_sizes = {
        "small": 30,
        "medium": 60,
        "large": 100
    }
    #get rgb in tuple
    colors = color.split("(")[1].split(")")[0].split(",")
    color = tuple(map(int, colors))
    total_duration = duration["end"] - duration["start"]
    orignalClip = VideoFileClip(video_path)
    width, height = orignalClip.size

    size = size.strip().lower()
    font = font.strip().lower()
    fonts_dict = {
        "normal": "resources/inter.ttf",
        "bold": "resources/bebas.ttf",
        "stylish": "resources/playfair.ttf"
    }

    txt_clip = TextClip(fonts_dict[font],content, margin=(10,10),font_size=font_sizes[size], color=color, method="label",stroke_color=get_stroke_color(color),stroke_width=2).with_duration(total_duration).with_start(duration["start"])
    textclip_width, textclip_height = txt_clip.size

    # calculate the position
    x = max(width * position["x"]/100 - textclip_width/2, 0)
    y = max(height * position["y"]/100 - textclip_height/2, 0)
    fade_duration = 0.3
    txt_clip = txt_clip.with_position((x, y)).with_effects([vfx.CrossFadeIn(fade_duration), vfx.CrossFadeOut(fade_duration)])
    return txt_clip

# creating text clips for each text
text_clips = []
for text in json_t["texts"]:
    text_clip = fade_in("data/merged_output_watermarked.mp4", text["text_duration"], text["text"], text["font_size"], text["position"], text["color"], text["font"])
    text_clips.append(text_clip)

# composite the text clips with the original video
composite = CompositeVideoClip([VideoFileClip("data/merged_output_watermarked.mp4"), *text_clips] )
composite.write_videofile("data/textss.mp4", codec='libx264', audio_codec='aac')

# # testing the fade_in function
# text=  fade_in("data/merged_output_watermarked.mp4", {"end": 3.0, "start": 0.0}, "L'Essence Noir Luxury Perfume", "large", {"x": 50.0, "y": 20.0})       
# composite = CompositeVideoClip([VideoFileClip("data/merged_output_watermarked.mp4"), text])
# composite.write_videofile("data/merged_output_watermarked_text.mp4", codec='libx264', audio_codec='aac')
