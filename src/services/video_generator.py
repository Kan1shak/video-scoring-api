from models.schemas import VideoRequest


class VideoGenerator:
    def __init__(self, request: VideoRequest):
        self.request = request

    def generate_video(self) -> tuple[str, str]:
        """
        Generate a video based on provided criteria and returns the path to the generated video and the uploaded video url
        """
        # placeholder for video generation for now
        return "data/less_bg_fg_separation.mp4", "https://example.com/generated_video.mp4"