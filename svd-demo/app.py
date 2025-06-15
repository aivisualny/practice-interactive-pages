import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import svd
import plotly.graph_objects as go

st.title('SVD (특이값 분해) 시각화 데모')

# 사이드바에 설명 추가
st.sidebar.markdown("""
## SVD (특이값 분해)란?
SVD는 행렬을 세 개의 행렬의 곱으로 분해하는 방법입니다:
- U: 왼쪽 특이 벡터
- Σ: 특이값을 대각성분으로 가지는 행렬
- V^T: 오른쪽 특이 벡터의 전치

이 데모에서는 2x2 행렬의 SVD를 시각화합니다.
""")

# 사용자 입력을 받는 부분
st.subheader('행렬 입력')
col1, col2 = st.columns(2)

with col1:
    a = st.number_input('a', value=1.0)
    c = st.number_input('c', value=0.0)

with col2:
    b = st.number_input('b', value=0.0)
    d = st.number_input('d', value=1.0)

# 입력 행렬 생성
A = np.array([[a, b], [c, d]])

# SVD 수행
U, s, Vh = svd(A)
S = np.diag(s)

# 결과 표시
st.subheader('SVD 결과')
st.write('입력 행렬 A:')
st.write(A)

st.write('U 행렬 (왼쪽 특이 벡터):')
st.write(U)

st.write('Σ 행렬 (특이값):')
st.write(S)

st.write('V^T 행렬 (오른쪽 특이 벡터의 전치):')
st.write(Vh)

# 시각화
st.subheader('시각화')

# 단위 원 생성
theta = np.linspace(0, 2*np.pi, 100)
x = np.cos(theta)
y = np.sin(theta)
unit_circle = np.vstack((x, y))

# 변환된 원 계산
transformed_circle = A @ unit_circle

# Plotly를 사용한 시각화
fig = go.Figure()

# 단위 원
fig.add_trace(go.Scatter(
    x=unit_circle[0],
    y=unit_circle[1],
    mode='lines',
    name='단위 원',
    line=dict(color='blue')
))

# 변환된 원
fig.add_trace(go.Scatter(
    x=transformed_circle[0],
    y=transformed_circle[1],
    mode='lines',
    name='변환된 원',
    line=dict(color='red')
))

# 특이 벡터 시각화
for i in range(2):
    # U의 열 벡터
    fig.add_trace(go.Scatter(
        x=[0, U[0, i]],
        y=[0, U[1, i]],
        mode='lines+markers',
        name=f'U 벡터 {i+1}',
        line=dict(color='green', width=2)
    ))
    
    # V의 열 벡터
    fig.add_trace(go.Scatter(
        x=[0, Vh[i, 0]],
        y=[0, Vh[i, 1]],
        mode='lines+markers',
        name=f'V 벡터 {i+1}',
        line=dict(color='purple', width=2)
    ))

fig.update_layout(
    title='SVD 시각화',
    xaxis_title='x',
    yaxis_title='y',
    showlegend=True,
    xaxis=dict(
        scaleanchor="y",
        scaleratio=1,
    )
)

st.plotly_chart(fig)

# 설명 추가
st.markdown("""
### 시각화 설명
- 파란색 원: 원래의 단위 원
- 빨간색 타원: 행렬 A에 의해 변환된 원
- 초록색 벡터: U 행렬의 열 벡터
- 보라색 벡터: V 행렬의 열 벡터

특이값은 타원의 주축 길이를 나타내며, U와 V의 열 벡터는 각각 변환된 타원의 주축 방향을 나타냅니다.
""") 