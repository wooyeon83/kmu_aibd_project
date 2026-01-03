#!/bin/bash


# 8000번 포트를 사용하는 프로세스의 PID 찾기
pid=$(lsof -ti:8000)

if [ -z "$pid" ]; then
    echo "8000번 포트를 사용하는 프로세스가 없습니다."
else
    echo "8000번 포트를 사용하는 프로세스(PID: $pid)를 종료합니다."
    kill -9 $pid
    echo "프로세스가 종료되었습니다."
fi 

cd "../result"
python3 -m http.server 8000 &
sleep 1
open "http://localhost:8000/2024_kyobo_bestseller_review_trend_visualization.html"
wait
