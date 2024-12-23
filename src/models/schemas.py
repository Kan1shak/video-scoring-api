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

class Justifications(BaseModel):
    background_foreground_separation: str
    brand_guideline_adherence: str
    creativity_visual_appeal: str
    product_focus: str
    call_to_action: str
    audience_relevance: str
    
class Scoring(BaseModel):
    background_foreground_separation: float
    brand_guideline_adherence: float
    creativity_visual_appeal: float
    product_focus: float
    call_to_action: float
    audience_relevance: float
    total_score: float
    justifications: Justifications


class ScoringTypedDict(typing.TypedDict):
    background_foreground_separation: float
    brand_guideline_adherence: float
    creativity_visual_appeal: float
    product_focus: float
    call_to_action: float
    audience_relevance: float
    total_score: float
    justifications: Justifications

class VideoResponse(BaseModel):
    status: str
    video_url: str
    scoring: Scoring
    metadata: Metadata

class VideoGenerationPrompts(BaseModel):
    hero_prompt: str
    segment_one_keyframe: str
    segment_one_motion: str
    segment_two_keyframe: str
    segment_two_motion: str
    segment_three_keyframe: str
    segment_three_motion: str
