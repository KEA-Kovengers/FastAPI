import os
from dotenv import load_dotenv
load_dotenv()

from typing import Optional
import uvicorn
from fastapi import FastAPI
app = FastAPI()

from pydantic import BaseModel
from utils.karlo_service import image_create

import pymongo

# MongoDB에 연결할 클라이언트 생성
client = pymongo.MongoClient(os.getenv("MONGO_URL"))
db = client[os.getenv("CLUSTER_NAME")]

# 사진을 요청하기 위해서 작성한 텍스트를 받기 위한 클래스
class Content(BaseModel):
    content: Optional[str] = None

# 이미지 생성을 요청하기 위해 호출하는 함수
# post 방식을 통해서 content: text 식으로 API를 호출하고
# image_url을 통해서 사진을 돌려받는다.
@app.post("/create")
def create_item(item: Content):
    image_url = image_create(item.content)
    return {"content": image_url}

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
    first_document = cursor.next()
    print(first_document)
    return "123"

# uvicorn
if __name__ == '__main__' :
    uvicorn.run('main:app', host='0.0.0.0', port=int(os.getenv('PORT')), access_log=True, reload=True, reload_dirs='./main.py')
