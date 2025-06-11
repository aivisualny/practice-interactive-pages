import streamlit as st
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d import Axes3D
import tempfile
import os

# 한글 폰트 설정 (예: 나눔고딕, AppleGothic 등)
matplotlib.rcParams['font.family'] = 'NanumGothic'  # 또는 'AppleGothic', 'Malgun Gothic' 등
matplotlib.rcParams['axes.unicode_minus'] = False  # 마이너스 부호 깨짐 방지

# ---------------- Streamlit 설정 ----------------
st.set_page_config(page_title="수학 애니메이션", layout="wide")
st.title("수학 애니메이션 시각화")

# ---------------- 공통 유틸 ----------------
def save_animation(_animation_obj, fps=30):
    with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tmp:
        _animation_obj.save(tmp.name, writer=PillowWriter(fps=fps))
        with open(tmp.name, "rb") as f:
            gif_data = f.read()
    # 🔽 삭제는 생략하거나 시각화 후 명시적으로
    # os.unlink(tmp.name)
    return gif_data

# ---------------- 애니메이션 생성 함수 ----------------
def generate_sine():
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.linspace(0, 10, 500)
    y = np.sin(x)

    ax.set_xlim(0, 10)
    ax.set_ylim(-1.5, 1.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y = sin(x)")
    ax.set_title("사인 함수 자취")
    ax.grid(True)

    line, = ax.plot([], [], "b-", lw=2)
    point, = ax.plot([], [], "ro")

    x_trace, y_trace = [], []

    def update(frame):
        x_trace.append(x[frame])
        y_trace.append(y[frame])
        line.set_data(x_trace, y_trace)
        point.set_data([x[frame]], [y[frame]])
        return line, point

    ani = FuncAnimation(fig, update, frames=len(x), interval=20, blit=True)
    return ani

def generate_circle():
    fig, ax = plt.subplots(figsize=(6, 6))
    t = np.linspace(0, 2 * np.pi, 100)
    x, y = np.cos(t), np.sin(t)

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("2차원 원운동")
    ax.grid(True)

    path, = ax.plot(x, y, "b--", alpha=0.3)
    point, = ax.plot([], [], "ro", ms=8)
    trace, = ax.plot([], [], "r-", alpha=0.5)

    x_trace, y_trace = [], []

    def update(frame):
        x_trace.append(x[frame])
        y_trace.append(y[frame])
        point.set_data([x[frame]], [y[frame]])
        trace.set_data(x_trace, y_trace)
        return point, trace

    ani = FuncAnimation(fig, update, frames=len(t), interval=50, blit=True)
    return ani

def generate_spiral():
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")

    t = np.linspace(0, 10, 200)
    x, y, z = np.cos(t), np.sin(t), t / 5

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(0, 2)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_title("3차원 나선형 곡선")

    line, = ax.plot([], [], [], "b-", alpha=0.3)
    point, = ax.plot([], [], [], "ro", ms=6)

    x_trace, y_trace, z_trace = [], [], []

    def update(frame):
        x_trace.append(x[frame])
        y_trace.append(y[frame])
        z_trace.append(z[frame])
        line.set_data(x_trace, y_trace)
        line.set_3d_properties(z_trace)
        point.set_data([x[frame]], [y[frame]])
        point.set_3d_properties([z[frame]])
        return line, point

    ani = FuncAnimation(fig, update, frames=len(t), interval=50, blit=True)
    return ani

# ---------------- UI: 애니메이션 선택 ----------------
animation_type = st.sidebar.selectbox(
    "애니메이션 유형 선택",
    ("사인 함수 자취", "2차원 원운동", "3차원 나선형 곡선")
)

if animation_type == "사인 함수 자취":
    ani = generate_sine()
elif animation_type == "2차원 원운동":
    ani = generate_circle()
else:
    ani = generate_spiral()

# ---------------- 화면 출력 ----------------
gif = save_animation(ani)
st.image(gif, caption=f"{animation_type} 애니메이션", use_column_width=True)

# ---------------- 설명 ----------------
st.markdown(
    """
### 애니메이션 설명
- **사인 함수 자취**: 사인 함수 그래프를 따라가는 점의 자취.
- **2차원 원운동**: 단위원을 도는 점의 위치 변화를 시각적으로 추적.
- **3차원 나선형 곡선**: 3D 공간에서 나선형으로 움직이는 점의 경로.
"""
)
