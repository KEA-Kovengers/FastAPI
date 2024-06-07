from http.client import HTTPException
import json
import os
from dotenv import load_dotenv
load_dotenv('/Submodules/fastapi-env/.env')
import re
from elasticsearch import Elasticsearch

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

origins = [
    "http://localhost",
    "http://localhost:3000",
    "*",
]

es = Elasticsearch(['http://3.36.133.139:9200'])

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 허용할 Origin(출처) 리스트
    allow_credentials=True,  # 인증 정보 허용 여부
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # 허용할 HTTP 메서드
    allow_headers=["Authorization", "Content-Type", "Accept"],  # 허용할 헤더
)


def extract_brace_content(string):
    # 정규 표현식을 사용하여 중괄호 사이의 내용을 찾습니다.
    pattern = re.compile(r"\{ .*\} ", re.IGNORECASE)
    matches = pattern.findall(string)
    return matches

# JSON 파일에서 쿼리를 읽어오는 함수
def read_query_from_file(file_path):
    with open(file_path, "r") as f:
        query = json.load(f)
    return query

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
    print(text)
    generated_text = modify_spell(text)
    print(generated_text.choices[0].message.content)
    print(extract_brace_content(generated_text.choices[0].message.content))
    jsonData = json.loads((generated_text.choices[0].message.content))

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
    # print('123')
    # jsonData = json.loads(hashtags.choices[0].message.content)

    return image_url



@app.get("/search_users")
async def search_users(keyword: str):
    # JSON 파일에서 쿼리 읽어오기
    query = read_query_from_file("json/user.json")
    
    # 검색어로 쿼리 업데이트
    query["query"]["bool"]["must"][0]["bool"]["should"][0]["wildcard"]["nick_name"] = "*{}*".format(keyword)
    query["query"]["bool"]["must"][0]["bool"]["should"][1]["wildcard"]["blog_name"] = "*{}*".format(keyword)

    # Elasticsearch에 쿼리를 보내고 결과를 받음
    try:
        result = es.search(index="user.newcord_user_db.users", body=query)
        res = [{
            "id": hit["_source"]["id"], 
            "blog_name": hit["_source"]["blog_name"], 
            "nick_name": hit["_source"]["nick_name"], 
            "profile_img": hit["_source"]["profile_img"]
            } for hit in result["hits"]["hits"]]
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# id, blog_name, nick_name, profile_img
# 데이터 조회 API 엔드포인트 정의
@app.get("/search_posts")
async def search_posts(keyword: str):
    # JSON 파일에서 쿼리 읽어오기
    query = read_query_from_file("json/post.json")
    
    # 검색어로 쿼리 업데이트
    query["query"]["bool"]["must"][0]["wildcard"]["title"] = "*{}*".format(keyword)

    # Elasticsearch에 쿼리를 보내고 결과를 받음
    try:
        result = es.search(index="article.newcord_article_db.posts", body=query)

        res = []
        for hit in result["hits"]["hits"]:
            query = read_query_from_file("json/thumbnail.json")
            query["query"]["bool"]["must"][1]["match"]["post_id"] = hit["_source"]["post_id"]
            thumbs = es.search(index="article.newcord_article_db.post_thumbnails", body=query)
            res.append({
            "post_id": hit["_source"]["post_id"], 
            "title": hit["_source"]["title"], 
            "body": hit["_source"]["body"], 
            "views": hit["_source"]["views"],
            "thumbnails": [thumb["_source"]["url"] for thumb in thumbs["hits"]["hits"]]
            })

        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# uvicorn
if __name__ == '__main__' :
    uvicorn.run('main:app', host='0.0.0.0', port=int(os.getenv('PORT')), access_log=True, reload=True, reload_dirs='./main.py')
