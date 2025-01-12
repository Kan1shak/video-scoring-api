from pydantic import BaseModel, HttpUrl
from typing import List, Dict
import typing_extensions as typing
class Dimensions(BaseModel):
    width: int
    height: int

class VideoDetails(BaseModel):
    product_name: str
    tagline: str
    brand_palette: List[str]
    dimensions: Dimensions
    duration: int
    cta_text: str
    logo_url: HttpUrl
    product_video_url: HttpUrl

class VideoRequest(BaseModel):
    video_details: VideoDetails
    scoring_criteria: Dict[str, int]
    additional_guidelines: str
    video_style: str

class Resolution(BaseModel):
    width: int
    height: int

class Metadata(BaseModel):
    file_size_mb: float
    duration_seconds: int
    resolution: Resolution

# class Scoring(BaseModel):
#     background_foreground_separation: float
#     brand_guideline_adherence: float
#     creativity_visual_appeal: float
#     product_focus: float
#     call_to_action: float
#     audience_relevance: float
#     total_score: float
#     justifications: Dict[str, str]


class VideoResponse(BaseModel):
    status: str
    video_url: str
    scoring: Dict
    metadata: Metadata

class VideoGenerationPrompts(BaseModel):
    hero_prompt: str
    keyframe_prompt: str
    motion_prompt: str

class TextDuration(typing.TypedDict):
    start: float
    end: float

class TextPosition(typing.TypedDict):
    x: float
    y: float


class TextOverlay(typing.TypedDict):
    text: str
    text_duration: TextDuration
    position: TextPosition
    font_size: str # small, medium, large
    font: str # font type from Normal, Bold, Stylish
    color: str # RGB color code

class TextOverlays(typing.TypedDict):
    texts: List[TextOverlay]