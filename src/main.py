from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
import os

from .models.schemas import VideoRequest, VideoResponse
from .services.video_scorer import VideoScorer
from .services.video_generator import VideoGenerator
from .utils.helpers import get_video_metadata, send_email
from .utils.db_helpers import init_db, set_response_data, get_response_data

app = FastAPI(title="Video Scoring API | Team Chill Guys")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
init_db()
FRONTEND_URL = os.environ.get("FRONTEND_URL")

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
        print(f"Generated video url: {generated_url}")
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
        metadata.resolution.width = request.video_details.dimensions.width
        metadata.resolution.height = request.video_details.dimensions.height
        # creating response
        response = VideoResponse(
            status="success",
            video_url=generated_url,
            scoring=scoring,
            metadata=metadata,
            identifier=""
        )
        # save response to db
        response = set_response_data(response)
        # send email if email is provided
        if request.email:
            send_email("VideoCreativeGen", request.email, "Your Requested Video is Ready", 
                       f"""Thank you for using VideoCreativeGen. 
Your requested video has been generated and scored.
Access it now at {FRONTEND_URL}/{response.identifier}.
""")
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # clean up uploaded file
        if video_path.exists():
            # for testing we are not deleting the video
            #video_path.unlink()
            ...

@app.get("/score-video/{identifier}/", response_model=VideoResponse)
async def get_scored_video(identifier: str):
    """
    Get the scored video response from sqlite db
    """
    try:
        response = get_response_data(identifier)
        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)