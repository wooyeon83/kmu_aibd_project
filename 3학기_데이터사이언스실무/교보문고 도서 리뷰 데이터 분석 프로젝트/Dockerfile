FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    fonts-nanum \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 필요한 Python 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# result 디렉토리 생성
RUN mkdir -p /app/result

# 포트 설정
EXPOSE 8000

# 웹 서버 실행
CMD ["python", "-m", "http.server", "8000", "--directory", "/app/result"] 