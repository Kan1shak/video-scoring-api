# Video Creative Scoring API | Team Chill Guys

A FastAPI-based service that evaluates video creatives using multimodal LLM analysis. The service processes videos according to provided brand guidelines and scoring criteria, providing detailed scoring and justifications for marketing videos.

## Table of Contents
- [Setup Instructions](#setup-instructions)
- [API Documentation](#api-documentation)
- [Technical Stack](#technical-stack)
- [Environment Variables](#environment-variables)
- [Scoring Methodology](#scoring-methodology)

## Setup Instructions

### Prerequisites
- Python 3.12.7
- pip (Python package manager)
- Docker (for containerized deployment)
- Gemini API access
- Cloudinary account
- Fal.ai API access

### Local Setup

1. Clone the repository:
```bash
git clone [your-repo-url]
cd video-scoring-api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables in `.env`:
```env
CLOUD_NAME=your_cloudinary_cloud_name
API_KEY=your_cloudinary_api_key
API_SECRET=your_cloudinary_secret_key
FAL_KEY=your_fal_ai_key
GEMINI_API_KEY=your_gemini_api_key
```

5. Run the application:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### Docker Setup

1. Build the Docker image:
```bash
docker build -t video-scoring-api .
```

2. Run the container:
```bash
docker run -p 7860:7860 \
  -e CLOUD_NAME=your_cloudinary_cloud_name \
  -e API_KEY=your_cloudinary_api_key \
  -e API_SECRET=your_cloudinary_secret_key \
  -e FAL_KEY=your_fal_ai_key \
  -e GEMINI_API_KEY=your_gemini_api_key \
  video-scoring-api
```

### Hugging Face Spaces Deployment
1. Fork this repository
2. Create a new Space on Hugging Face
3. Choose Docker as the SDK
4. Configure the following environment variables in your Space settings:
   - Public Variables:
     - CLOUD_NAME
     - API_KEY
   - Secret Variables:
     - API_SECRET
     - FAL_KEY
     - GEMINI_API_KEY

## API Documentation

### Score Video Endpoint

**Endpoint:** `/score-video`  
**Method:** POST  
**Content-Type:** application/json

#### Request Body

```json
{
    "video_details": {
        "product_name": "string",
        "tagline": "string",
        "brand_palette": ["string"],
        "dimensions": {
            "width": integer,
            "height": integer
        },
        "duration": integer,
        "cta_text": "string",
        "logo_url": "string (uri)",
        "product_video_url": "string (uri)"
    },
    "scoring_criteria": {
        "background_foreground_separation": integer,
        "brand_guideline_adherence": integer,
        "creativity_visual_appeal": integer,
        "product_focus": integer,
        "call_to_action": integer,
        "audience_relevance": integer
    }
}
```

#### Successful Response (200 OK)

```json
{
    "status": "success",
    "video_url": "string",
    "scoring": {
        "background_foreground_separation": number,
        "brand_guideline_adherence": number,
        "creativity_visual_appeal": number,
        "product_focus": number,
        "call_to_action": number,
        "audience_relevance": number,
        "total_score": number,
        "justifications": {
            "background_foreground_separation": "string",
            "brand_guideline_adherence": "string",
            "creativity_visual_appeal": "string",
            "product_focus": "string",
            "call_to_action": "string",
            "audience_relevance": "string"
        }
    },
    "metadata": {
        "file_size_mb": number,
        "duration_seconds": integer,
        "resolution": {
            "width": integer,
            "height": integer
        }
    }
}
```

#### Error Responses

**422 Validation Error**
```json
{
    "detail": [
        {
            "loc": ["string"],
            "msg": "string",
            "type": "string"
        }
    ]
}
```

## Technical Stack

### Core Technologies
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.12.7**: Programming language
- **Uvicorn**: ASGI web server for production deployment
- **Cloudinary**: Cloud storage for video assets
- **Gemini**: Multimodal LLM for video analysis
- **Fal.ai**: AI model inference for automatic video generation

### Key Libraries
- **OpenCV (cv2)**: Video processing and analysis
- **Google Generative AI**: Multimodal LLM integration
- **Pydantic**: Data validation
- **cloudinary**: Cloud asset management

### Architecture Components
- **main.py**: API routes and application setup
- **models/schemas.py**: Pydantic models
- **services/video_scorer.py**: Scoring logic
- **services/video_generator.py**: Video generation
- **utils/**: Helper functions

## Environment Variables

| Variable | Description | Type | Required |
|----------|-------------|------|----------|
| CLOUD_NAME | Cloudinary cloud name | Public | Yes |
| API_KEY | Cloudinary API key | Public | Yes |
| API_SECRET | Cloudinary API secret | Secret | Yes |
| FAL_KEY | Fal.ai API key | Secret | Yes |
| GEMINI_API_KEY | Google Gemini API key | Secret | Yes |

## Scoring Methodology

The API employs a three-stage evaluation process:

1. **Rubric Generation**
   - Creates detailed scoring criteria
   - Ensures consistent evaluation standards
   - Adapts to specific brand requirements

2. **Video Analysis**
   - Processes video using multimodal LLM
   - Evaluates against established rubric
   - Generates detailed justifications

3. **Structured Output**
   - Standardizes scoring format
   - Provides comprehensive feedback
   - Includes technical metadata

### Scoring Criteria
- Background & Foreground Separation (20 points)
- Brand Guideline Adherence (20 points)
- Creativity & Visual Appeal (20 points)
- Product Focus (15 points)
- Call-to-Action (15 points)
- Audience Relevance (10 points)

Total possible score: 100 points

Each criterion includes detailed justifications in the API response, explaining the rationale behind the scores and providing actionable feedback for improvements.

---
title: video-scoring-api
emoji: 🐻
colorFrom: blue
sdk: docker
pinned: false
license: mit
short_description: Video Scoring API written in FastAPI
---