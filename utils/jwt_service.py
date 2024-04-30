import datetime
import jwt
import os
from dotenv import load_dotenv
load_dotenv('Submodules/fastapi-env/.env')

SECRET_KEY = os.getenv('SECRET_KEY')

def encode(id):
    # 토큰 만료 시간 설정 (예: 현재 시간으로부터 1시간 후)
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

    # 토큰 생성
    payload = {
        'id': id,
        'username': 'example_user',
        'exp': expiration_time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    print("Encoded Token:", token)
    return token

def decode(token):
    # 토큰 해독
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        print("Decoded Payload:", decoded_payload)
        return decoded_payload
    except jwt.ExpiredSignatureError:
        print("Token has expired.")
        return False
    except jwt.InvalidTokenError:
        print("Invalid token.")
        return False
