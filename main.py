from http.client import HTTPException
import json
import os
from dotenv import load_dotenv
load_dotenv('/Submodules/fastapi-env/.env')

from typing import List, Optional, Union
import uvicorn
from fastapi import FastAPI, Header, status
app = FastAPI()

from pydantic import BaseModel
from utils.jwt_service import encode, decode
from fastapi.middleware.cors import CORSMiddleware
from utils.openai_service import generate_hashtag, generate_text, generate_image, modify_spell, genereate_summary

import pymongo

import redis
conn = redis.Redis()

# MongoDB에 연결할 클라이언트 생성
client = pymongo.MongoClient(os.getenv("MONGO_URL"))
db = client[os.getenv("CLUSTER_NAME")]

origins = [
    "http://localhost",
    "http://localhost:3000",
    "*",
]

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 허용할 Origin(출처) 리스트
    allow_credentials=True,  # 인증 정보 허용 여부
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # 허용할 HTTP 메서드
    allow_headers=["Authorization", "Content-Type", "Accept"],  # 허용할 헤더
)



# api/post/check?postid=2
@app.get("/api/post/check")
def post_check(postid: int = 0, token: Union[str, None] = Header(default=None)):
    if postid == 0:
        return status.HTTP_502_BAD_GATEWAY
    else:
        text = decode(token)['id'] + '_' + str(postid)
        conn.set(text, '1')
        return True



class TextPayload(BaseModel):
    text: str

@app.post("/generate/hashtag")
async def generate_hashtag_api(payload: TextPayload):
    # Access the text from the payload
    text = payload.text
    hashtags = generate_hashtag(text)
    jsonData = json.loads(hashtags.choices[0].message.content)

    return jsonData['hashtags']

@app.post("/generate/text")
async def generate_text_api(payload: TextPayload):
    # Access the text from the payload
    text = payload.text
    generated_text = generate_text(text)
    jsonData = json.loads(generated_text.choices[0].message.content)

    return jsonData['sentence']

@app.post("/modify/spell")
async def modify_spell_api(payload: TextPayload):
    # Access the text from the payload
    text = payload.text
    generated_text = modify_spell(text)
    jsonData = json.loads(generated_text.choices[0].message.content)

    return jsonData

@app.post("/generate/summary")
async def genereate_summary_api(payload: TextPayload):
    # Access the text from the payload
    text = payload.text
    generated_text = genereate_summary(text)
    jsonData = json.loads(generated_text.choices[0].message.content)

    return jsonData

@app.post("/generate/image")
async def generate_image_api(payload: TextPayload):
    # Access the text from the payload
    text = payload.text
    image_url = generate_image(text)
    # jsonData = json.loads(hashtags.choices[0].message.content)

    return image_url

# uvicorn
if __name__ == '__main__' :
    uvicorn.run('main:app', host='0.0.0.0', port=int(os.getenv('PORT')), access_log=True, reload=True, reload_dirs='./main.py')
