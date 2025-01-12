import typing
from typing import List, Tuple, Dict
import requests
import os
import cv2
import cloudinary 
import cloudinary.uploader
import cloudinary.api
import colorsys
import numpy as np
from ..models.schemas import Metadata, Resolution
from io import BytesIO
from PIL import Image
from moviepy import VideoFileClip, concatenate_videoclips, ImageClip, CompositeVideoClip,TextClip, VideoFileClip
import moviepy.video.fx as vfx
cloud_name = os.getenv('CLOUD_NAME')
api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')

cloudinary.config(
    cloud_name=cloud_name,
    api_key=api_key,
    api_secret=api_secret
)

def download_file(url:str, filename:str) -> str:
    """
    Downloads a file from the given url and saves it with 
    the given filename in the tmp folder in the project 
    root directory.
    """
    tmp_dir = os.path.abspath("tmp")
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    
    filename = os.path.join(tmp_dir, filename)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return filename

def get_video_metadata(video_path: str) -> Metadata:
    """
    Get video metadata using OpenCV
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Could not open video file")

    # Get basic video metadata
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS))
    file_size = os.path.getsize(video_path) / (1024 * 1024)  # convert to MBs

    cap.release()

    return Metadata(
        file_size_mb=round(file_size, 2),
        duration_seconds=duration,
        resolution=Resolution(width=width, height=height)
    )


def upload_image(image: Image) -> str:
    try:
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG') 
        img_byte_arr.seek(0) 
        url = cloudinary.uploader.upload(img_byte_arr)
        return url['secure_url']
    except Exception as e:
        return f"Error uploading the image: {e}"
    
def get_last_frame(video_path: str) -> Image:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Could not open video file")

    cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_FRAME_COUNT) - 1)
    ret, frame = cap.read()
    if not ret:
        raise ValueError("Could not read the video frame")

    cap.release()

    return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

def merge_videos(video_paths:List, output_path:str)->None:
    try:
        video_clips = [VideoFileClip(path) for path in video_paths]
        final_clip = concatenate_videoclips(video_clips)
        final_clip.write_videofile(output_path)
        
        for clip in video_clips:
            clip.close()
    except Exception as e:
        print(f"Error merging videos: {e}")

def upload_and_crop_video(video_path:str, crop_width:int, crop_height:int) -> str:
    try:
        # Upload with cropping transformation
        result = cloudinary.uploader.upload(video_path,
            resource_type = "video",
            transformation=[
                {
                    'width': crop_width, 
                    'height': crop_height,
                    'crop': 'fill'  # or 'fill', 'pad', 'scale', etc.
                }
            ]
        )
        return result['secure_url']
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
    
def add_watermark(video_path:str, logo_path:str, output_path:str) -> None:
    video = VideoFileClip(video_path)
    
    logo = ImageClip(logo_path, transparent=True)
    
    logo_width = video.w // 8  # w is video width
    logo = logo.resized(width=logo_width)  # maintains aspect ratio
    logo = logo.with_opacity(0.7)
    padding = 20
    x = video.w - logo.w - padding
    y = video.h - logo.h - padding
    
    logo = logo.with_position((x, y))
    logo = logo.with_duration(video.duration)
    
    final_video = CompositeVideoClip([video, logo])
    
    final_video.write_videofile(
        output_path,
        codec='libx264',
        audio_codec='aac'
    )
    
    video.close()
    final_video.close()

def create_dynamic_scoring_td(criteria_names: list[str]):
    justification_fields = {
        criterion: str for criterion in criteria_names
    }
    DynamicJustifications = typing.TypedDict('Justifications', justification_fields)
    
    # Create Scoring TypedDict
    scoring_fields = {
        criterion: float for criterion in criteria_names
    }
    scoring_fields.update({
        'total_score': float,
        'justifications': DynamicJustifications
    })
    
    DynamicScoringDict = typing.TypedDict('ScoringTypedDict', scoring_fields)
    
    return DynamicScoringDict

def get_stroke_color(rgb:Tuple)->Tuple:
    r, g, b = [x/255 for x in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    new_l = max(0, l - 0.2)
    new_r, new_g, new_b = colorsys.hls_to_rgb(h, new_l, s)
    return tuple(round(x * 255) for x in (new_r, new_g, new_b))

def fade_in_text(video_path:str, duration:Dict, content:str, size:str, position:Dict, color:str, font:str) -> None:
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

def embed_text_clips(video_path:str, text_clips:List[TextClip], output_path:str) -> None:
    composite = CompositeVideoClip([VideoFileClip(video_path), *text_clips] )
    composite.write_videofile(output_path, codec='libx264', audio_codec='aac')
    composite.close()