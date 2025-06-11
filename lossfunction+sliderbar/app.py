import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(page_title="Learning Rate 시각화", layout="wide")
st.title("Learning Rate에 따른 손실 함수 변화 시각화")

# 본문 슬라이더 (사이드바 X)
learning_rate = st.slider(
    "Learning Rate",
    min_value=0.001,
    max_value=0.1,
    value=0.01,
    step=0.001,
    format="%.3f"
)

# 손실 함수 데이터 생성 함수
def generate_loss_data(lr, epochs=100):
    x = np.linspace(0, epochs, epochs)
    y = np.exp(-lr * x) + np.random.normal(0, 0.1, epochs)
    return x, y

# 학습률 반영한 그래프 생성
x, y = generate_loss_data(learning_rate)
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, y, 'b-', label='Loss')
ax.set_xlabel('Epochs')
ax.set_ylabel('Loss')
ax.set_title(f'Learning Rate: {learning_rate:.3f}')
ax.grid(True)
ax.legend()

# 그래프 출력
st.pyplot(fig)

# 설명
st.markdown("""
### 설명
- 위 슬라이더를 조절하여 학습률을 변경할 수 있습니다.
- 학습률이 클수록 손실 함수가 더 빠르게 감소하지만, 불안정할 수 있습니다.
- 학습률이 작을수록 더 안정적이지만 학습 속도가 느려질 수 있습니다.
""")
