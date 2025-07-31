#!/bin/bash

echo "FileForge 프론트엔드를 시작합니다..."

# 프론트엔드 디렉토리로 이동
cd frontend

# Node.js 의존성 설치
echo "Node.js 의존성을 설치합니다..."
npm install

# 개발 서버 실행
echo "React 개발 서버를 시작합니다..."
npm run dev 