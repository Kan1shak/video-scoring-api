import requests
import os
import cv2
from models.schemas import Metadata, Resolution

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