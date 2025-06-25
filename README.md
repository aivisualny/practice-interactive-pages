# 📁 AI/ML 실험 페이지 모음

딥러닝, 머신러닝, 데이터 시각화 프로젝트들을 한 곳에서 관리하는 중앙 통합 포털 사이트입니다.

## 🚀 프로젝트 개요

이 프로젝트는 여러 개의 독립적인 AI/ML 시각화 및 데모 프로젝트들을 하나의 포털 사이트에서 중앙 관리할 수 있도록 설계되었습니다.

### 주요 특징

- **중앙화된 관리**: 모든 프로젝트를 한 곳에서 접근 가능
- **현대적인 UI**: 반응형 디자인과 부드러운 애니메이션
- **카테고리 분류**: 시각화, 애플리케이션 등으로 프로젝트 분류
- **검색 기능**: 프로젝트 검색 및 필터링 (향후 확장)
- **모바일 친화적**: 모든 디바이스에서 최적화된 경험

## 📋 포함된 프로젝트

### 🎨 시각화 프로젝트
- **CNN 구조 시각화**: Convolutional Neural Network 레이어 구조
- **신경망 설명**: 고양이 인식 예제를 통한 신경망 원리
- **신경망 학습**: 실시간 학습 과정 시각화
- **GAN 구조 시각화**: D3.js를 활용한 GAN 구조
- **스타일 전송 데모**: Neural Style Transfer 시각화
- **PCA 시각화**: 차원 축소 시각화
- **D3.js 시각화**: 데이터 시각화 프로젝트

### 🔧 애플리케이션 프로젝트
- **딥러닝 특화 과정**: 교육용 시각화
- **감정 분석 앱**: React 기반 NLP 애플리케이션
- **손실함수 + 슬라이더**: 인터랙티브 손실함수 시각화
- **Sin(x) 함수 시각화**: 수학 함수 시각화
- **SVD 데모**: Singular Value Decomposition
- **다중 페이지 앱**: Streamlit 기반 웹앱
- **FastAPI 데모**: 백엔드 API 서버

## 🛠️ 기술 스택

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **스타일링**: CSS Grid, Flexbox, CSS Animations
- **폰트**: Inter (Google Fonts)
- **아이콘**: Font Awesome 6
- **반응형**: Mobile-first 접근법

## 📦 설치 및 실행

### 로컬 개발 환경

1. **저장소 클론**
   ```bash
   git clone <repository-url>
   cd practice-interactive-pages
   ```

2. **로컬 서버 실행**
   ```bash
   # Python 3의 내장 서버 사용
   python -m http.server 8000
   
   # 또는 Node.js의 live-server 사용
   npx live-server --port=8000
   ```

3. **브라우저에서 접속**
   ```
   http://localhost:8000
   ```

### 배포 방법

#### 1. GitHub Pages (추천)

1. **GitHub 저장소 생성**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/username/repository-name.git
   git push -u origin main
   ```

2. **GitHub Pages 활성화**
   - 저장소 설정 → Pages
   - Source를 "Deploy from a branch"로 설정
   - Branch를 "main"으로 설정
   - 폴더를 "/ (root)"로 설정

3. **배포 완료**
   ```
   https://username.github.io/repository-name
   ```

#### 2. Vercel

1. **Vercel CLI 설치**
   ```bash
   npm i -g vercel
   ```

2. **배포**
   ```bash
   vercel
   ```

#### 3. Netlify

1. **Netlify CLI 설치**
   ```bash
   npm install -g netlify-cli
   ```

2. **배포**
   ```bash
   netlify deploy
   ```

## 🎯 프로젝트 구조

```
practice-interactive-pages/
├── index.html              # 메인 포털 페이지
├── styles.css              # 메인 스타일시트
├── script.js               # 메인 JavaScript
├── README.md               # 프로젝트 문서
├── cnn-visualization-demo/ # CNN 시각화
├── neural-network-explanation/ # 신경망 설명
├── gan-visualization/      # GAN 시각화
├── style-transfer-demo/    # 스타일 전송
├── pca-visualization/      # PCA 시각화
├── D3/                     # D3.js 프로젝트
├── deep-learning-specialization/ # 딥러닝 교육
├── ml-sentiment-app/       # 감정 분석 앱
├── lossfunction+sliderbar/ # 손실함수 시각화
├── sinxfunction/           # Sin 함수 시각화
├── svd-demo/               # SVD 데모
├── multipages/             # 다중 페이지 앱
└── FastAPI_Demo/           # FastAPI 서버
```

## 🔧 커스터마이징

### 새 프로젝트 추가

1. **프로젝트 폴더 생성**
   ```bash
   mkdir new-project
   cd new-project
   # 프로젝트 파일들 생성
   ```

2. **포털에 추가**
   `index.html`의 `.projects-grid` 섹션에 새 카드 추가:

   ```html
   <div class="project-card" data-category="visualization">
       <div class="card-header">
           <i class="fas fa-icon-name"></i>
           <h3>프로젝트 제목</h3>
       </div>
       <p class="card-description">프로젝트 설명</p>
       <div class="card-tags">
           <span class="tag">태그1</span>
           <span class="tag">태그2</span>
       </div>
       <a href="./new-project/index.html" class="card-link" target="_blank">
           <i class="fas fa-external-link-alt"></i>
           보러가기
       </a>
   </div>
   ```

### 스타일 수정

- `styles.css`에서 색상, 폰트, 레이아웃 수정
- CSS 변수를 활용하여 테마 변경 가능

### 기능 확장

- `script.js`에 검색, 필터링, 정렬 기능 추가
- 카테고리별 분류 시스템 확장
- 다크 모드, 다국어 지원 등

## 📱 반응형 디자인

- **데스크톱**: 3열 그리드 레이아웃
- **태블릿**: 2열 그리드 레이아웃
- **모바일**: 1열 그리드 레이아웃

## 🎨 디자인 시스템

### 색상 팔레트
- **Primary**: #667eea (보라색)
- **Secondary**: #764ba2 (진보라색)
- **Text**: #2d3748 (진회색)
- **Background**: 그라데이션 (보라색 계열)

### 타이포그래피
- **Font Family**: Inter
- **Weights**: 300, 400, 500, 600, 700

### 애니메이션
- **Duration**: 0.3s - 0.6s
- **Easing**: ease, ease-in-out
- **Effects**: fadeInUp, hover, scale

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 연락처

프로젝트에 대한 문의사항이나 제안사항이 있으시면 이슈를 생성해 주세요.

---

**Made with ❤️ for AI/ML Education** 