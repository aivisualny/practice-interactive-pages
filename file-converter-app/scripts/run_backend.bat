@echo off
echo FileForge 백엔드 서버를 시작합니다...

REM Python 가상환경 확인 및 생성
if not exist "venv" (
    echo Python 가상환경을 생성합니다...
    python -m venv venv
)

REM 가상환경 활성화
echo 가상환경을 활성화합니다...
call venv\Scripts\activate.bat

REM 의존성 설치
echo Python 의존성을 설치합니다...
pip install -r backend\requirements.txt

REM 백엔드 디렉토리로 이동
cd backend

REM 서버 실행
echo FastAPI 서버를 시작합니다...
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload

pause 