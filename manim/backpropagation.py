from manim import *
import numpy as np

class BackpropagationAnimation(Scene):
    def construct(self):
        # 신경망 구조 정의
        input_layer = [Circle(radius=0.3, color=BLUE) for _ in range(2)]
        hidden_layer = [Circle(radius=0.3, color=GREEN) for _ in range(2)]
        output_layer = [Circle(radius=0.3, color=RED) for _ in range(1)]

        # 레이어 배치
        for i, node in enumerate(input_layer):
            node.move_to(LEFT * 4 + UP * (1 - i))
        for i, node in enumerate(hidden_layer):
            node.move_to(LEFT * 2 + UP * (1 - i))
        output_layer[0].move_to(RIGHT * 2)

        # 가중치 선 그리기
        weights = []
        for i in input_layer:
            for h in hidden_layer:
                line = Line(i.get_center(), h.get_center(), color=YELLOW)
                weights.append(line)
        for h in hidden_layer:
            line = Line(h.get_center(), output_layer[0].get_center(), color=YELLOW)
            weights.append(line)

        # 신경망 그리기
        self.play(
            *[Create(node) for node in input_layer],
            *[Create(node) for node in hidden_layer],
            *[Create(node) for node in output_layer],
            *[Create(weight) for weight in weights]
        )

        # 역전파 애니메이션
        error_text = Text("Error = y - y_hat", font_size=24).next_to(output_layer[0], UP)
        self.play(Write(error_text))
        self.wait()

        # 출력층에서 은닉층으로의 역전파
        for h in hidden_layer:
            arrow = Arrow(output_layer[0].get_center(), h.get_center(), color=RED)
            self.play(Create(arrow))
            self.wait(0.5)
            self.play(FadeOut(arrow))

        # 은닉층에서 입력층으로의 역전파
        for i in input_layer:
            arrow = Arrow(hidden_layer[0].get_center(), i.get_center(), color=RED)
            self.play(Create(arrow))
            self.wait(0.5)
            self.play(FadeOut(arrow))

        self.wait(2) 