# 베이스 이미지 설정
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 파일 복사
COPY . .

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 컨테이너 내에서 사용할 환경 변수 설정
ENV PORT=8000

# 포트 노출
EXPOSE 8000

# 실행 명령 설정
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
