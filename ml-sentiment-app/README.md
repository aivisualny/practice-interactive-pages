# 감정 분석 데모 프로젝트

이 프로젝트는 FastAPI와 React를 사용한 감정 분석 웹 애플리케이션입니다. 한국어 텍스트의 감정을 분석하고 결과를 시각적으로 보여줍니다.

## 주요 기능

- 한국어 텍스트 감정 분석
- MLflow를 통한 실험 추적
- Docker 컨테이너화
- React 기반 프론트엔드
- GCP 배포 지원

## 기술 스택

- Backend: FastAPI, PyTorch, Transformers
- Frontend: React
- ML: Hugging Face Transformers, MLflow
- DevOps: Docker, GCP

## 설치 및 실행 방법

### 백엔드 실행

1. 가상환경 생성 및 활성화:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. 의존성 설치:
```bash
pip install -r requirements.txt
```

3. 서버 실행:
```bash
uvicorn app.main:app --reload
```

### 프론트엔드 실행

1. 프론트엔드 디렉토리로 이동:
```bash
cd frontend
```

2. 의존성 설치:
```bash
npm install
```

3. 개발 서버 실행:
```bash
npm start
```

### Docker로 실행

```bash
docker build -t sentiment-analysis .
docker run -p 8000:8000 sentiment-analysis
```

## GCP 배포

1. GCP 프로젝트 설정
2. Cloud Run 서비스 생성
3. Docker 이미지 빌드 및 푸시
4. 서비스 배포

## MLflow 설정

MLflow 서버 실행:
```bash
mlflow server --host 0.0.0.0 --port 5000
```

## 라이선스

MIT 