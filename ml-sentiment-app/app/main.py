from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
import mlflow
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="감정 분석 API", description="한국어 텍스트 감정 분석 API입니다.")

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 개발 서버 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MLflow 설정
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"))
mlflow.set_experiment("sentiment-analysis")

# 감정 분석 모델 로드
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="klue/bert-base",
    tokenizer="klue/bert-base"
)

# 감정 레이블 매핑 (KLUE/BERT-base 기준 예시)
id2label = {
    "LABEL_0": "부정",
    "LABEL_1": "중립",
    "LABEL_2": "긍정"
}

class TextInput(BaseModel):
    text: str

@app.get("/")
async def root():
    return {"message": "감정 분석 API에 오신 것을 환영합니다!"}

@app.post("/analyze")
async def analyze_sentiment(input_data: TextInput):
    try:
        with mlflow.start_run():
            result = sentiment_analyzer(input_data.text)
            label = result[0]["label"]
            sentiment = id2label.get(label, label)  # 사람이 읽을 수 있게 변환
            mlflow.log_param("input_text", input_data.text)
            mlflow.log_metric("sentiment_score", result[0]["score"])
            return {
                "text": input_data.text,
                "sentiment": sentiment,
                "confidence": result[0]["score"]
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 