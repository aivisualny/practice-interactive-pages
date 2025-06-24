const courses = [
  {
    title: '1. Neural Networks and Deep Learning',
    goal: '신경망과 딥러닝의 기초 개념을 익히고, 간단한 인공신경망을 직접 구현해봅니다.',
    content: `
      <b>핵심 개념:</b> 인공신경망(ANN), 뉴런, 가중치, 활성화 함수, 층(layer), 순전파/역전파, 로지스틱 회귀<br>
      <b>쉬운 비유:</b> 뉴런은 미니 의사결정자, 신경망은 여러 단계의 시각 피질처럼 특징을 추출<br>
      <b>실습:</b> 파이썬/NumPy로 신경망 구현, 고양이 이미지 분류, 벡터화, 얕은/심층 신경망 실습
    `
  },
  {
    title: '2. Improving Deep Neural Networks',
    goal: '딥러닝 모델의 성능을 높이는 하이퍼파라미터 튜닝, 규제화, 최적화 기법을 배웁니다.',
    content: `
      <b>핵심 개념:</b> 하이퍼파라미터(학습률, 층 수 등), 규제화(L2, 드롭아웃), 최적화(Adam, RMSprop), 배치 정규화<br>
      <b>쉬운 비유:</b> 모델 튜닝은 빵 굽기(온도, 시간, 재료 조절), 드롭아웃은 농구팀 훈련<br>
      <b>실습:</b> 드롭아웃/학습률 실험, gradient checking, TensorFlow 기본 실습
    `
  },
  {
    title: '3. Structuring Machine Learning Projects',
    goal: '머신러닝/딥러닝 프로젝트의 문제 진단과 개선 우선순위 설정법을 배웁니다.',
    content: `
      <b>핵심 개념:</b> Bias-Variance 진단, 데이터셋 구성, 에러 분석, 엔드투엔드 vs 모듈식, 전이/멀티태스크 학습<br>
      <b>쉬운 비유:</b> 모델을 진단하는 머신러닝 주치의, 프로젝트 매니지먼트 감각<br>
      <b>실습:</b> 오류 진단 퀴즈, 시나리오별 개선 전략 연습
    `
  },
  {
    title: '4. Convolutional Neural Networks (CNNs)',
    goal: '이미지 인식 혁신을 이끈 합성곱 신경망(CNN) 구조와 응용을 배웁니다.',
    content: `
      <b>핵심 개념:</b> 합성곱/풀링, 필터, 패딩, 스트라이드, 다양한 CNN 아키텍처(LeNet, AlexNet, VGG, ResNet), 스타일 변환<br>
      <b>쉬운 비유:</b> CNN은 이미지에 돋보기를 여러 번 통과시키는 것, 계층적 특징 추출<br>
      <b>실습:</b> CNN 구현, 손글씨 분류, ResNet 블록, Neural Style Transfer 실습
    `
  },
  {
    title: '5. Sequence Models',
    goal: '텍스트, 음성 등 순차 데이터를 다루는 RNN, LSTM, Transformer 모델을 배웁니다.',
    content: `
      <b>핵심 개념:</b> RNN, LSTM, GRU, 워드 임베딩, Seq2Seq, 어텐션, Transformer, HuggingFace 활용<br>
      <b>쉬운 비유:</b> 기억과 언어의 마술사, 문맥을 기억하며 대화/번역하는 구조<br>
      <b>실습:</b> RNN 문자 생성, 감성 분류, Seq2Seq 번역, 사전학습 NLP모델 실습
    `
  }
];

// 각 과정별 상세 설명과 시각화 이미지 경로
const courseDetail = [
  {
    detail: `인공신경망은 사람 뇌의 뉴런을 본뜬 모델로, 입력층-은닉층-출력층 구조를 가집니다. 각 뉴런은 입력값에 가중치를 곱해 더한 뒤, 활성화 함수를 거쳐 출력을 만듭니다. 여러 층이 쌓이면 복잡한 패턴도 인식할 수 있습니다.<br><br><b>비유:</b> 입력층은 사진의 픽셀, 은닉층은 귀/수염/얼굴 등 부분 특징, 출력층은 '고양이일 확률'을 판단하는 역할입니다.<br><br><b>실습:</b> 로지스틱 회귀, 얕은 신경망, 심층 신경망을 직접 구현하며 순전파/역전파 개념을 익힙니다.`,
    img: 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Artificial_neural_network.svg/600px-Artificial_neural_network.svg.png'
  },
  {
    detail: `딥러닝 모델의 성능을 높이기 위해 하이퍼파라미터(학습률, 층 수 등)를 조정하고, 과적합을 막는 규제화(L2, 드롭아웃), 학습을 빠르게 하는 최적화(Adam, RMSprop) 기법을 배웁니다.<br><br><b>비유:</b> 하이퍼파라미터는 빵 굽기의 온도/시간, 드롭아웃은 농구팀 훈련에서 일부러 선수를 빼는 것과 비슷합니다.<br><br><b>실습:</b> 드롭아웃/학습률 실험, gradient checking, TensorFlow 실습 등으로 모델 개선을 체험합니다.`,
    img: 'https://miro.medium.com/v2/resize:fit:700/1*JrOq1t2r6U0Yk1K9lQ7QNA.png'
  },
  {
    detail: `머신러닝 프로젝트에서 오류를 진단하고, 편향-분산 분석, 데이터셋 구성, 에러 분석, 전이학습/멀티태스크 전략 등 프로젝트 성공을 위한 실전 노하우를 배웁니다.<br><br><b>비유:</b> 모델을 진단하는 주치의처럼, 문제의 원인을 단계별로 파악하고 개선 방향을 제시합니다.<br><br><b>실습:</b> 오류 진단 퀴즈, 시나리오별 개선 전략 연습 등으로 프로젝트 리더의 사고방식을 익힙니다.`,
    img: 'https://developers.google.com/machine-learning/crash-course/images/ML-Project-Flow.png'
  },
  {
    detail: `합성곱 신경망(CNN)은 이미지의 공간 정보를 활용해 특징을 추출합니다. 필터(커널)가 이미지를 훑으며 특징맵을 만들고, 풀링으로 정보를 압축합니다. 다양한 CNN 구조(LeNet, AlexNet, VGG, ResNet)와 스타일 변환 등 응용도 배웁니다.<br><br><b>비유:</b> CNN은 여러 돋보기를 통과하며 점점 복잡한 특징을 인식하는 것과 같습니다.<br><br><b>실습:</b> CNN 구현, 손글씨 분류, ResNet 블록, Neural Style Transfer 등 실습을 진행합니다.`,
    img: 'https://upload.wikimedia.org/wikipedia/commons/6/63/Typical_cnn.png'
  },
  {
    detail: `RNN, LSTM, Transformer 등은 순차 데이터를 처리하는 모델입니다. RNN은 이전 정보를 기억하며 처리하고, LSTM/GRU는 장기 기억을 보완합니다. Transformer는 어텐션을 활용해 병렬처리가 가능합니다.<br><br><b>비유:</b> 시퀀스 모델은 대화나 번역처럼 앞 문맥을 기억하며 처리하는 마술사입니다.<br><br><b>실습:</b> RNN 문자 생성, 감성 분류, Seq2Seq 번역, 사전학습 NLP모델 실습 등 다양한 순차 데이터 실습을 경험합니다.`,
    img: 'https://jalammar.github.io/images/t/transformer_illustrated.png'
  }
];

const main = document.getElementById('course-list');
courses.forEach((course, idx) => {
  const card = document.createElement('section');
  card.className = 'course-card';
  card.innerHTML = `
    <div class="course-title">${course.title}</div>
    <div class="course-goal">${course.goal}</div>
    <div class="course-content">${course.content}</div>
  `;
  card.addEventListener('click', () => openModal(idx));
  main.appendChild(card);
});

// 모달 관련
const modal = document.getElementById('modal');
const modalTitle = document.getElementById('modal-title');
const modalDetail = document.getElementById('modal-detail');
const modalImage = document.getElementById('modal-image');
const closeBtn = document.querySelector('.close-btn');

function openModal(idx) {
  modalTitle.innerText = courses[idx].title;
  modalDetail.innerHTML = courseDetail[idx].detail;
  modalImage.innerHTML = `<img src="${courseDetail[idx].img}" alt="${courses[idx].title} 시각화">`;
  modal.style.display = 'flex';
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  modal.style.display = 'none';
  document.body.style.overflow = '';
}

closeBtn.addEventListener('click', closeModal);
modal.addEventListener('click', (e) => {
  if (e.target === modal) closeModal();
});

