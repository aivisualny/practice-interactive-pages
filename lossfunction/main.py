import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import imageio

# 학습 곡선 데이터 생성 (더 큰 변동성 추가)
epochs = 100
x = np.linspace(0, 10, epochs)
train_loss = np.exp(-0.05 * x) + 0.2 * np.sin(x) + 0.1 * np.random.randn(epochs)
val_loss = np.exp(-0.03 * x) + 0.25 * np.sin(x + 0.5) + 0.15 * np.random.randn(epochs)

# 그래프 설정
plt.style.use('default')
fig, ax = plt.subplots(figsize=(10, 6))

# 초기 그래프 설정
line1, = ax.plot([], [], label='Training Loss', color='blue', linewidth=2)
line2, = ax.plot([], [], label='Validation Loss', color='red', linewidth=2)
ax.set_xlabel('Epochs', fontsize=12)
ax.set_ylabel('Loss', fontsize=12)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

# y축 범위 설정
y_min = np.minimum(np.min(train_loss), np.min(val_loss)) - 0.1
y_max = np.maximum(np.max(train_loss), np.max(val_loss)) + 0.1
ax.set_ylim(y_min, y_max)
ax.set_xlim(0, epochs)

# 애니메이션 업데이트 함수
def update(frame):
    line1.set_data(range(frame + 1), train_loss[:frame + 1])
    line2.set_data(range(frame + 1), val_loss[:frame + 1])
    ax.set_title(f'Learning Curve (Epoch {frame + 1})', fontsize=14)
    return line1, line2

# 애니메이션 생성
anim = FuncAnimation(fig, update, frames=epochs, interval=50, blit=True)

# GIF로 저장
anim.save('learning_curve.gif', writer='pillow', fps=20)

plt.close()
