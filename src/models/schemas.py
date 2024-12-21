from pydantic import BaseModel, HttpUrl
from typing import List
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

class ScoringCriteria(BaseModel):
    background_foreground_separation: int
    brand_guideline_adherence: int
    creativity_visual_appeal: int
    product_focus: int
    call_to_action: int
    audience_relevance: int

class VideoRequest(BaseModel):
    video_details: VideoDetails
    scoring_criteria: ScoringCriteria

class Resolution(BaseModel):
    width: int
    height: int

class Metadata(BaseModel):
    file_size_mb: float
    duration_seconds: int
    resolution: Resolution

class Scoring(BaseModel):
    background_foreground_separation: float
    brand_guideline_adherence: float
    creativity_visual_appeal: float
    product_focus: float
    call_to_action: float
    audience_relevance: float
    total_score: float
    justifications: str

class ScoringTypedDict(typing.TypedDict):
    background_foreground_separation: float
    brand_guideline_adherence: float
    creativity_visual_appeal: float
    product_focus: float
    call_to_action: float
    audience_relevance: float
    total_score: float
    justifications: str

class VideoResponse(BaseModel):
    status: str
    video_url: str
    scoring: Scoring
    metadata: Metadata