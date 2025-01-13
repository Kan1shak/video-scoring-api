import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.utils.helpers import send_email

# from src.services.video_scorer import VideoScorer
# from src.models.schemas import VideoRequest, VideoDetails, Dimensions

# video_request = VideoRequest(
#     video_details=VideoDetails(
#         product_name="Chili",
#         tagline="The carbon Neutral Brand",
#         brand_palette=["gold", "black", "white"],
#         dimensions=Dimensions(width=1920, height=1080),
#         duration=44,
#         cta_text="Call to action",
#         logo_url="https://i.postimg.cc/KzqB6DQG/logo.png",
#         product_video_url="https://example.com/video.mp4"
#     ),
#     scoring_criteria=ScoringCriteria(
#         background_foreground_separation=5,
#         brand_guideline_adherence=5,
#         creativity_visual_appeal=5,
#         product_focus=5,
#         call_to_action=5,
#         audience_relevance=5
#     )
# )

# video_request = VideoRequest(
#     video_details=VideoDetails(
#         product_name="Quistive",
#         tagline="The water bottle for the new gen.",
#         brand_palette=["pink", "black", "white"],
#         dimensions=Dimensions(width=1920, height=1080),
#         duration=34,
#         cta_text="Call to action",
#         logo_url="https://i.postimg.cc/XvSdfv18/logo2.png",
#         product_video_url="https://example.com/video.mp4"
#     ),
#     scoring_criteria = {
#         "background_foreground_separation": "20",
#         "brand_guideline_adherence": "20",    
#         "creativity_visual_appeal": "20",
#         "product_focus": "15",
#         "call_to_action": "15",
#         "audience_relevance": "10",
#         "trendyness": "5"
#     }
#     # =ScoringCriteria(
#     #     background_foreground_separation=20,
#     #     brand_guideline_adherence=20,
#     #     creativity_visual_appeal=20,
#     #     product_focus=15,
#     #     call_to_action=15,
#     #     audience_relevance=10
        
#     )

# scorer = VideoScorer(video_request,"data/less_bg_fg_separation.mp4")
# response = scorer.score_video()

# print(response)

res = send_email("Video Gen", "kanishak202@gmail.com", "This is a test email", "Your video is ready for review. Please check the website to view the video.")
print(res.text)