import json
import google.generativeai as genai
import os
from fastapi import HTTPException
from models.schemas import VideoRequest, VideoResponse, Scoring, ScoringTypedDict, Metadata, Resolution
from utils.llm_helpers import upload_to_gemini, wait_for_files_active, safety_settings, gemini_generation_config
from utils.helpers import download_file


genai.configure(api_key=os.environ["GEMINI_API_KEY"])
class VideoScorer:
    def __init__(self,video_request: VideoRequest, generated_video_path: str):
        self.video_request = video_request
        self.generated_video_path = generated_video_path
        self.llm =  genai.GenerativeModel(
                        model_name="gemini-2.0-flash-exp",
                        generation_config=gemini_generation_config,
                        safety_settings=safety_settings,
                        system_instruction=
f"""You will be given the following information by the user:
- product_name : The name of the product
- tagline: The tagline of the product
- brand_palette : A list of colors that the brand uses
- cta_text : The call to action text
- brand_logo : The brand logo
- a video creative of the product
- scoring_criteria: The criteria for scoring the video
- These videos are targeted at an age group of millennials, aged 25-35. 
Now based on the criteria, and the information provided, you need to:
- Firstly build an even more detailed rubric for awarding points. 
- After creating the rubric, now step by step score the video with your justifications.
- Score the videos for the total duration, and not frame by frame analysis.
- The final score is not a percentage, but a score out of the maximum total score.
- Include jusitifications for each category in the scoring.
"""
                    )
        self.llm_json_writer = genai.GenerativeModel(
            model_name= "gemini-1.5-flash",
            generation_config={
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 40,
                "response_mime_type": "application/json", 
                "response_schema": ScoringTypedDict
            },
            safety_settings=safety_settings,
            system_instruction="From the given text, extract the required data for the given JSON schema and provide the JSON response. For the jusitification part, provide brief summaries of each scoring criteria and how the video meets that criteria."
        )
    def score_video(self) -> VideoResponse:
        generated_video_path = os.path.abspath(self.generated_video_path)
        logo_url = self.video_request.video_details.logo_url
        logo_path = download_file(logo_url, "logo.png")
        video_request_dict = self.video_request.model_dump()
        input_text = f"""
product_name: {video_request_dict['video_details']['product_name']}
tagline: {video_request_dict['video_details']['tagline']}
brand_palette: {video_request_dict['video_details']['brand_palette']}
cta_text: {video_request_dict['video_details']['cta_text']}
scoring_criteria: {video_request_dict['scoring_criteria']}
More info on Scording Criteria:
○ Background and Foreground Separation:
	■ Clear and visually distinct separation.
○ Adherence to Brand Guidelines:
	■ Consistency in using brand colors, fonts, and logo.
○ Creativity and Visual Appeal:
	■ Engaging storytelling, transitions, and animations.
○ Product Focus:
	■ Prominence of the product throughout the video.
○ Call-to-Action:
	■ Visibility and placement of the CTA.
○ Audience Relevance:
	■ Appeal to the target audience's values and preferences.
"""
        files = [
            upload_to_gemini(generated_video_path),
            upload_to_gemini(logo_path)
        ]
        wait_for_files_active(files)

        chat_sess = self.llm.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        files[0],
                    ],
                },
                {
                    "role": "user",
                    "parts": [
                        files[1],
                    ],
                },
            ]
        )
        response = chat_sess.send_message(input_text).text
        print(response)
        scoring = json.loads(self.llm_json_writer.generate_content(response).text)
        scoring = Scoring(**scoring)
        print(scoring.model_dump_json())
        return scoring
