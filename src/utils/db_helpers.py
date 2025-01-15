import json
import sqlite3
import uuid

from fastapi import HTTPException
from ..models.schemas import VideoResponse
from typing import Optional

def generate_unique_id()->str:
    return str(uuid.uuid4())

def init_db():
    conn = sqlite3.connect('video_responses.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS video_responses
        (id TEXT PRIMARY KEY,
         response_data TEXT)
    ''')
    conn.commit()
    conn.close()

def set_response_data(video_response:VideoResponse)->VideoResponse:
    response_id = generate_unique_id()
    conn = sqlite3.connect('video_responses.db')
    video_response.identifier = response_id
    c = conn.cursor()
    response_json = video_response.model_dump_json()
    c.execute('INSERT INTO video_responses (id, response_data) VALUES (?, ?)', 
              (response_id, response_json))
    
    conn.commit()
    conn.close()
    return video_response

def get_response_data(response_id:str)->Optional[VideoResponse]:
    conn = sqlite3.connect('video_responses.db')
    c = conn.cursor()
    c.execute('SELECT response_data FROM video_responses WHERE id = ?', (response_id,))
    result = c.fetchone()
    conn.close()
    if result is None:
        raise HTTPException(status_code=404, detail="Video response not found")
    response_json = result[0]
    response = VideoResponse.model_validate(json.loads(response_json))
    return response