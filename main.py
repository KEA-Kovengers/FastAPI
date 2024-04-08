from http.client import HTTPException
import os
from dotenv import load_dotenv
load_dotenv()

from typing import List, Optional, Union
import uvicorn
from fastapi import FastAPI, Header, status
app = FastAPI()

from pydantic import BaseModel
from utils.karlo_service import image_create
from utils.gemini_service import find_typo, generate_hashtag, generate_text
from utils.jwt_service import encode, decode

import pymongo

import redis
conn = redis.Redis()

# MongoDB에 연결할 클라이언트 생성
client = pymongo.MongoClient(os.getenv("MONGO_URL"))
db = client[os.getenv("CLUSTER_NAME")]

@app.get("/test")
def text():
    # collection = db["test"]
    # new_document = {
    #     "name": "count_eeho",
    #     "age": 30,
    #     "city": "Seoul"
    # }
    # cursor = collection.insert_one(new_document)
    # 첫 번째 결과 가져오기
    # first_document = cursor.next()
    # print(first_document)
    hashtags = generate_hashtag("1. 동해물과 백두산이 마르고 닳도록 하느님이 보우하사 우리나라 만세 무궁화 삼천리 화려 강산 대한 사람 대한으로 길이 보전하세 " +
                            "2. 남산 위에 저 소나무 철갑을 두른 듯 바람 서리 불변함은 우리 기상일세 무궁화 삼천리 화려 강산 대한 사람 대한으로 길이 보전하세 "+ 
                            "3. 가을 하늘 공활한데 높고 구름 없이 밝은 달은 우리 가슴 일편단심일세 무궁화 삼천리 화려 강산 대한 사람 대한으로 길이 보전하세 "+
                            "4. 이 기상과 이 맘으로 충성을 다하여 괴로우나 즐거우나 나라 사랑하세 무궁화 삼천리 화려 강산 대한 사람 대한으로 길이 보전하세")
    print("Hashtags:")
    print(hashtags)
    generated_text = generate_text(["파이썬", "FastAPI", "설치"])
    print("Generated text:")
    print(generated_text)
    typo_results = find_typo("친구는 세월의도둑이다. 봄부터 흐르느느물은 겨울이 되어도 얼지 않는다.")
    print("Typo results:")
    print(typo_results)
    return "123"

# api/post/check?postid=2
@app.get("/api/post/check")
def post_check(postid: int = 0, token: Union[str, None] = Header(default=None)):
    if postid == 0:
        return status.HTTP_502_BAD_GATEWAY
    else:
        text = decode(token)['id'] + '_' + str(postid)
        conn.set(text, '1')
        return True

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.post("/items/")
async def create_item(item: Item):
    return item


# test
@app.get("/api/get/token")
def get_token():
    return encode('660dff3450c489e4d36312eb')

# uvicorn
if __name__ == '__main__' :
    uvicorn.run('main:app', host='0.0.0.0', port=int(os.getenv('PORT')), access_log=True, reload=True, reload_dirs='./main.py')
