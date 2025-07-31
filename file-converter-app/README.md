# FileForge - 파일 변환 도구

간편하고 빠른 파일 변환 웹 애플리케이션입니다. 다양한 이미지 및 문서 형식 간 변환을 지원합니다.

## 🚀 주요 기능

- **다중 파일 업로드**: 드래그 앤 드롭으로 여러 파일을 한 번에 업로드
- **이미지 변환**: JPG, PNG, GIF, BMP, TIFF, WebP 형식 간 변환
- **압축 품질 조절**: 이미지 압축률을 1-100% 범위에서 조절
- **실시간 변환**: 업로드된 파일을 즉시 변환하여 다운로드
- **반응형 UI**: 모바일과 데스크톱에서 모두 사용 가능

## 🛠 기술 스택

### 백엔드
- **FastAPI**: 고성능 Python 웹 프레임워크
- **Pillow**: 이미지 처리 라이브러리
- **Uvicorn**: ASGI 서버

### 프론트엔드
- **React 18**: 사용자 인터페이스
- **Tailwind CSS**: 스타일링
- **Vite**: 빌드 도구
- **Lucide React**: 아이콘 라이브러리

## 📦 설치 및 실행

### 사전 요구사항
- Python 3.8+
- Node.js 16+
- npm 또는 yarn

### 1. 저장소 클론
```bash
git clone <repository-url>
cd file-converter-app
```

### 2. 백엔드 실행
```bash
# 스크립트 사용 (Linux/Mac)
chmod +x scripts/run_backend.sh
./scripts/run_backend.sh

# 또는 수동 실행
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 3. 프론트엔드 실행
```bash
# 스크립트 사용 (Linux/Mac)
chmod +x scripts/run_frontend.sh
./scripts/run_frontend.sh

# 또는 수동 실행
cd frontend
npm install
npm run dev
```

### 4. 브라우저에서 접속
- 프론트엔드: http://localhost:3000
- 백엔드 API: http://localhost:8000

## 📁 프로젝트 구조

```
file-converter-app/
├── backend/
│   ├── app.py                 # FastAPI 메인 애플리케이션
│   ├── routes/
│   │   └── convert.py         # 파일 변환 API 라우터
│   ├── utils/
│   │   └── convert_helpers.py # 파일 변환 헬퍼 클래스
│   └── requirements.txt       # Python 의존성
├── frontend/
│   ├── src/
│   │   ├── components/        # React 컴포넌트
│   │   ├── pages/            # 페이지 컴포넌트
│   │   └── main.jsx          # 앱 진입점
│   ├── package.json          # Node.js 의존성
│   └── tailwind.config.js    # Tailwind 설정
├── scripts/                  # 실행 스크립트
└── README.md
```

## 🔧 API 엔드포인트

### POST /api/v1/convert
파일을 변환합니다.

**요청:**
- `files`: 업로드할 파일들 (multipart/form-data)
- `target_format`: 변환할 형식 (string)
- `compression_quality`: 압축 품질 (integer, 1-100, 선택사항)

**응답:**
- 변환된 파일 또는 ZIP 파일

### GET /api/v1/formats
지원되는 파일 형식을 반환합니다.

### DELETE /api/v1/cleanup/{session_id}
임시 파일을 정리합니다.

## 🎯 지원하는 파일 형식

### 이미지 파일
- **입력**: JPG, JPEG, PNG, GIF, BMP, TIFF, WebP
- **출력**: JPG, PNG, GIF, BMP, TIFF, WebP

### 문서 파일 (기본 지원)
- **입력**: PDF, DOCX, DOC, TXT, RTF
- **출력**: PDF, DOCX, TXT, RTF

## 🔮 향후 계획

### 2단계 기능
- [ ] 다국어 지원 (한국어/영어)
- [ ] 사용 통계 표시
- [ ] 변환 히스토리
- [ ] 배치 처리 최적화

### 3단계 기능
- [ ] 사용자 계정 시스템
- [ ] 클라우드 저장소 연동 (S3, Google Drive)
- [ ] PDF 병합/분할 기능
- [ ] OCR 텍스트 추출
- [ ] 모바일 앱 (React Native)

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 문의

프로젝트에 대한 문의사항이나 버그 리포트는 GitHub Issues를 통해 제출해주세요. 