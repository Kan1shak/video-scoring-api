from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import os

from .models.schemas import VideoRequest, VideoResponse, Scoring, Metadata, Resolution
from .services.video_scorer import VideoScorer
from .services.video_generator import VideoGenerator
from .utils.helpers import get_video_metadata

app = FastAPI(title="Video Scoring API | Team Chill Guys")

@app.post("/score-video", response_model=VideoResponse)
async def score_video(
    request: VideoRequest,
):
    """
    Score a video based on provided criteria
    """
    # first we generate the video
    generator = VideoGenerator(request)
    try:
        video_path, generated_url = generator.generate_video()
        video_path = Path(video_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # now we score the video
    try:
        # initialize scorer with request data
        scorer = VideoScorer(request, video_path)
        
        # get video scoring
        scoring = scorer.score_video()
        
        # get video metadata
        metadata = get_video_metadata(str(video_path))
        
        # creating response
        response = VideoResponse(
            status="success",
            # just a placeholder for now
            video_url=generated_url,
            scoring=scoring,
            metadata=metadata
        )
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # clean up uploaded file
        if video_path.exists():
            # for testing we are not deleting the video
            #video_path.unlink()
            ...


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)