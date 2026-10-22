# 파이썬 공식 슬림 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# Cloud Run에서 사용하는 포트 (기본 8080)
ENV PORT=8080
EXPOSE 8080

# Gunicorn을 이용해 프로덕션 환경에서 Flask 서버 구동
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
