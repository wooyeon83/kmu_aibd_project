#!/bin/bash

# 스크립트 실행 디렉토리로 이동
cd "$(dirname "$0")"

# Docker Desktop이 실행 중인지 확인
if [[ "$OSTYPE" == "darwin"* ]]; then
    if ! pgrep -f "Docker Desktop" > /dev/null; then
        echo "Docker Desktop이 실행되지 않았습니다."
        echo "Docker Desktop을 시작합니다..."
        open -a "Docker Desktop"
        
        # Docker Desktop이 완전히 시작될 때까지 대기
        echo "Docker 서비스가 시작될 때까지 대기중..."
        max_attempts=60
        attempt=1
        while [ $attempt -le $max_attempts ]; do
            if docker info &>/dev/null; then
                echo "Docker 서비스가 시작되었습니다."
                break
            fi
            echo "Docker 시작 대기 중... ($attempt/$max_attempts)"
            sleep 2
            attempt=$((attempt + 1))
        done

        if [ $attempt -gt $max_attempts ]; then
            echo "Error: Docker를 시작할 수 없습니다."
            echo "Docker Desktop이 제대로 설치되어 있는지 확인해주세요."
            exit 1
        fi
    fi
fi

# Docker 및 Docker Compose 설치 확인
if ! command -v docker &> /dev/null; then
    echo "Error: Docker가 설치되어 있지 않습니다."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose가 설치되어 있지 않습니다."
    exit 1
fi

# 8000 포트 사용 중인 프로세스 확인 및 종료
port_pid=$(lsof -ti:8000)
if [ ! -z "$port_pid" ]; then
    echo "8000 포트를 사용 중인 프로세스를 발견했습니다. (PID: $port_pid)"
    read -p "이 프로세스를 종료하시겠습니까? (y/n): " choice
    if [[ "$choice" =~ ^[Yy]$ ]]; then
        echo "프로세스를 종료합니다..."
        kill -9 $port_pid
        sleep 2
        echo "프로세스가 종료되었습니다."
    else
        echo "프로세스 종료를 취소했습니다. 스크립트를 종료합니다."
        exit 1
    fi
fi

# 이전 컨테이너 정리
echo "기존 컨테이너 확인 중..."
if docker ps -a --filter "name=kyobo-review-web" | grep -q kyobo-review-web; then
    echo "기존 컨테이너를 제거합니다..."
    docker-compose down
    sleep 2
fi

# Docker 이미지 빌드 및 컨테이너 실행
echo "Docker 컨테이너를 시작합니다..."
docker-compose up --build -d

# 컨테이너 실행 확인
echo "컨테이너 상태 확인 중..."
if ! docker ps | grep -q kyobo-review-web; then
    echo "Error: 컨테이너 실행에 실패했습니다."
    docker-compose logs
    exit 1
fi

# 웹 서버 응답 확인
echo "웹 서버 준비 중..."
max_attempts=30
attempt=1
while [ $attempt -le $max_attempts ]; do
    if curl -s http://localhost:8000 > /dev/null; then
        echo "웹 서버가 준비되었습니다."
        break
    fi
    echo "웹 서버 응답 대기 중... ($attempt/$max_attempts)"
    sleep 1
    attempt=$((attempt + 1))
done

if [ $attempt -gt $max_attempts ]; then
    echo "Error: 웹 서버가 응답하지 않습니다."
    docker-compose logs
    exit 1
fi

# result 디렉토리에 HTML 파일 존재 확인
if [ ! -f "result/2024_kyobo_bestseller_review_trend_visualization.html" ]; then
    echo "Error: HTML 파일을 찾을 수 없습니다."
    echo "result 디렉토리에 2024_kyobo_bestseller_review_trend_visualization.html 파일이 있는지 확인해주세요."
    exit 1
fi

# 브라우저에서 페이지 열기
echo "웹 페이지를 엽니다..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    open "http://localhost:8000/2024_kyobo_bestseller_review_trend_visualization.html"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open "http://localhost:8000/2024_kyobo_bestseller_review_trend_visualization.html"
else
    echo "브라우저를 수동으로 열어 다음 주소로 접속해주세요:"
    echo "http://localhost:8000/2024_kyobo_bestseller_review_trend_visualization.html"
fi

# 컨테이너 로그 표시
echo "컨테이너 로그를 표시합니다. 종료하려면 Ctrl+C를 누르세요..."
docker-compose logs -f 