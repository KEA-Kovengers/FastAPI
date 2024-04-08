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
    collection = db["test"]
    new_document = {
        "name": "count_eeho",
        "age": 30,
        "city": "Seoul"
    }
    cursor = collection.insert_one(new_document)
    # 첫 번째 결과 가져오기
    # first_document = cursor.next()
    # print(first_document)
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
