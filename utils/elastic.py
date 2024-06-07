import boto3
from requests_aws4auth import AWS4Auth
import requests

# AWS 자격 증명 및 지역 설정
region = 'ap-northeast-2'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# OpenSearch 엔드포인트
host = 'https://search-kov-elastic-5hdufsqtj45fr2iucmw3z4rmba.ap-northeast-2.es.amazonaws.com'
index = 'my-index'
type = '_doc'
url = host + '/' + index + '/' + type

# 데이터 생성
document = {
    "title": "Test Document",
    "content": "This is a test document."
}

# 요청
response = requests.put(url, auth=awsauth, json=document)
print(response.status_code)
print(response.text)
