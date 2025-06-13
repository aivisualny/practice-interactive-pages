from manim import *

class GANStructureAnimation(Scene):
    def construct(self):
        # 1. 제목
        title = Text("GAN (Generative Adversarial Network)", font_size=48)
        subtitle = Text("생성적 적대 신경망", font_size=36)
        title.to_edge(UP)
        subtitle.next_to(title, DOWN)
        self.play(Write(title))
        self.play(Write(subtitle))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle))

        # 2. Generator 구조 (왼쪽)
        generator_title = Text("Generator (생성자)", font_size=32, color=BLUE).move_to(LEFT * 5 + UP * 2.5)
        noise_layer = [Circle(radius=0.4, color=BLUE) for _ in range(3)]
        for i, node in enumerate(noise_layer):
            node.move_to(LEFT * 6 + UP * (1 - i))
        gen_hidden = [Circle(radius=0.4, color=BLUE) for _ in range(4)]
        for i, node in enumerate(gen_hidden):
            node.move_to(LEFT * 4 + UP * (1.5 - i * 0.8))
        gen_output = [Circle(radius=0.4, color=BLUE) for _ in range(4)]
        for i, node in enumerate(gen_output):
            node.move_to(LEFT * 2 + UP * (1.5 - i * 0.8))
        gen_weights1 = [Line(n.get_center(), h.get_center(), color=BLUE) for n in noise_layer for h in gen_hidden]
        gen_weights2 = [Line(h.get_center(), o.get_center(), color=BLUE) for h in gen_hidden for o in gen_output]
        self.play(Write(generator_title))
        self.play(*[Create(node) for node in noise_layer], *[Create(node) for node in gen_hidden], *[Create(node) for node in gen_output], *[Create(w) for w in gen_weights1], *[Create(w) for w in gen_weights2])
        self.wait(0.5)
        noise_text = Text("랜덤 노이즈", font_size=28, color=BLUE).next_to(noise_layer[0], LEFT)
        self.play(Write(noise_text))
        self.wait(0.5)
        # 예시 이미지(실제 이미지 사용)
        fake_img = ImageMobject("media/images/gan_structure/1.png").scale(0.5).move_to(LEFT * 0.5 + UP * 1.5)
        fake_img_label = Text("생성된 이미지 예시", font_size=20).next_to(fake_img, DOWN)
        self.play(FadeIn(fake_img), Write(fake_img_label))
        gen_explain = Text("Generator는 랜덤 노이즈로\n실제와 유사한 이미지를 생성합니다", font_size=26, color=BLUE).move_to(LEFT * 3.5 + DOWN * 2.5)
        self.play(Write(gen_explain))
        self.wait(2)
        self.play(FadeOut(generator_title), FadeOut(noise_text), FadeOut(fake_img), FadeOut(fake_img_label), FadeOut(gen_explain), *[FadeOut(n) for n in noise_layer], *[FadeOut(n) for n in gen_hidden], *[FadeOut(n) for n in gen_output], *[FadeOut(w) for w in gen_weights1], *[FadeOut(w) for w in gen_weights2])

        # 3. Discriminator 구조 (오른쪽)
        discriminator_title = Text("Discriminator (판별자)", font_size=32, color=RED).move_to(RIGHT * 5 + UP * 2.5)
        disc_input = [Circle(radius=0.4, color=RED) for _ in range(4)]
        for i, node in enumerate(disc_input):
            node.move_to(RIGHT * 2 + UP * (1.5 - i * 0.8))
        disc_hidden = [Circle(radius=0.4, color=RED) for _ in range(3)]
        for i, node in enumerate(disc_hidden):
            node.move_to(RIGHT * 4 + UP * (1 - i))
        disc_output = [Circle(radius=0.4, color=RED)]
        disc_output[0].move_to(RIGHT * 6)
        disc_weights1 = [Line(i.get_center(), h.get_center(), color=RED) for i in disc_input for h in disc_hidden]
        disc_weights2 = [Line(h.get_center(), disc_output[0].get_center(), color=RED) for h in disc_hidden]
        self.play(Write(discriminator_title))
        self.play(*[Create(node) for node in disc_input], *[Create(node) for node in disc_hidden], *[Create(node) for node in disc_output], *[Create(w) for w in disc_weights1], *[Create(w) for w in disc_weights2])
        self.wait(0.5)
        real_text = Text("진짜/가짜 판별", font_size=28, color=RED).next_to(disc_output[0], RIGHT)
        self.play(Write(real_text))
        self.wait(0.5)
        # 예시 이미지(임시 사각형)
        real_img = Square(0.8, color=WHITE, fill_opacity=0.5).move_to(RIGHT * 0.5 + UP * 1.5)
        real_img_label = Text("진짜 이미지 예시", font_size=20).next_to(real_img, DOWN)
        self.play(FadeIn(real_img), Write(real_img_label))
        disc_explain = Text("Discriminator는 입력 이미지를\n진짜/가짜로 판별합니다", font_size=26, color=RED).move_to(RIGHT * 3.5 + DOWN * 2.5)
        self.play(Write(disc_explain))
        self.wait(2)
        self.play(FadeOut(discriminator_title), FadeOut(real_text), FadeOut(real_img), FadeOut(real_img_label), FadeOut(disc_explain), *[FadeOut(n) for n in disc_input], *[FadeOut(n) for n in disc_hidden], *[FadeOut(n) for n in disc_output], *[FadeOut(w) for w in disc_weights1], *[FadeOut(w) for w in disc_weights2])

        # 4. 전체 구조 및 학습 과정
        generator_title = Text("Generator", font_size=28, color=BLUE).move_to(LEFT * 4.5 + UP * 2.5)
        discriminator_title = Text("Discriminator", font_size=28, color=RED).move_to(RIGHT * 4.5 + UP * 2.5)
        self.play(Write(generator_title), Write(discriminator_title))
        # Generator, Discriminator 입력/출력 노드만 다시 그림
        g_in = Circle(radius=0.4, color=BLUE).move_to(LEFT * 6 + UP * 0.5)
        g_out = Circle(radius=0.4, color=BLUE).move_to(LEFT * 2 + UP * 0.5)
        d_in = Circle(radius=0.4, color=RED).move_to(RIGHT * 2 + UP * 0.5)
        d_out = Circle(radius=0.4, color=RED).move_to(RIGHT * 6 + UP * 0.5)
        self.play(Create(g_in), Create(g_out), Create(d_in), Create(d_out))
        # Generator→Discriminator 연결
        connection = Line(g_out.get_center(), d_in.get_center(), color=YELLOW)
        self.play(Create(connection))
        structure_explain = Text("Generator가 만든 이미지는 Discriminator로 전달되어 판별됩니다", font_size=30).move_to(DOWN * 3)
        self.play(Write(structure_explain))
        self.wait(2)
        self.play(FadeOut(generator_title), FadeOut(discriminator_title), FadeOut(g_in), FadeOut(g_out), FadeOut(d_in), FadeOut(d_out), FadeOut(connection), FadeOut(structure_explain))

        # 5. 학습 과정(화살표)
        gen_arrow = Arrow(LEFT * 2, RIGHT * 2, color=GREEN, buff=0.5)
        gen_learn = Text("Generator는 Discriminator를 속이도록 학습", font_size=24, color=GREEN).next_to(gen_arrow, UP)
        self.play(Create(gen_arrow), Write(gen_learn))
        self.wait(1.5)
        self.play(FadeOut(gen_arrow), FadeOut(gen_learn))
        disc_arrow = Arrow(RIGHT * 2, LEFT * 2, color=ORANGE, buff=0.5)
        disc_learn = Text("Discriminator는 가짜 이미지를 더 잘 구분하도록 학습", font_size=24, color=ORANGE).next_to(disc_arrow, DOWN)
        self.play(Create(disc_arrow), Write(disc_learn))
        self.wait(1.5)
        self.play(FadeOut(disc_arrow), FadeOut(disc_learn))
        final_explain = Text("이러한 경쟁적 학습을 통해 Generator는 점점 더 진짜같은 이미지를 생성하게 됩니다", font_size=28).move_to(DOWN * 3)
        self.play(Write(final_explain))
        self.wait(2) 