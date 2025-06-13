from manim import *
import numpy as np


class TimeRelativity(Scene):
    """
    기다리는 5분 vs 쉬는 5분이 체감상 왜 다른지 1분+ 길이로 동적 시각화.
    - 다양한 카메라 이동·페이드 전환으로 '장면 수'를 늘려 시청 재미 ↑
    - 총 러닝타임 ≈ 70 s (타이틀 & 인트로 6 s + 기다림 25 s + 전환 5 s + 휴식 12 s + 동시 비교 12 s + 아웃트로 10 s)
    - 런타임 조정은 상단 상수만 바꾸면 손쉽게 가능.
    """

    # ------------------ 시간 파라미터 ------------------
    WAIT_RT = 25   # 지루한 5분(체감) 구간 애니메이션 seconds
    REST_RT = 12   # 휴식 5분(체감) 구간 seconds
    COMPARE_RT = 12  # 동시 비교 seconds

    def construct(self):
        # 배경 음악 효과를 위한 사운드 파일이 있다면 추가할 수 있습니다
        # self.add_sound("background_music.mp3")
        
        # 제목 - 더 역동적인 등장
        title = Text("시간의 상대성", font="Malgun Gothic", color=BLUE)
        title.scale(1.5)
        title.to_edge(UP)
        
        # 제목이 회전하며 등장
        self.play(
            Write(title),
            title.animate.scale(1.2).set_color(YELLOW),
            rate_func=rate_functions.there_and_back,
            run_time=1.5
        )
        
        # 시계 생성 - 더 화려한 시계
        clock = Circle(radius=2, color=WHITE)
        clock_ticks = VGroup()
        numbers = VGroup()
        
        for i in range(12):
            angle = i * TAU / 12
            # 시계 눈금
            tick = Line(
                clock.point_at_angle(angle) * 0.9,
                clock.point_at_angle(angle),
                stroke_width=3,
                color=YELLOW
            )
            clock_ticks.add(tick)
            
            # 시계 숫자
            num = Text(str(i+1), font="Malgun Gothic", color=WHITE)
            num.scale(0.5)
            num.move_to(clock.point_at_angle(angle) * 0.7)
            numbers.add(num)
        
        clock_group = VGroup(clock, clock_ticks, numbers)
        clock_group.to_edge(LEFT)
        
        # 시계가 회전하며 등장
        self.play(
            Create(clock),
            Create(clock_ticks),
            Write(numbers),
            clock_group.animate.scale(1.1),
            rate_func=rate_functions.ease_out_bounce,
            run_time=1.5
        )
        
        # 캐릭터 생성 - 더 극적인 표정
        waiting_character = Text("😫", font_size=100)
        resting_character = Text("😌", font_size=100)
        
        waiting_character.next_to(clock_group, RIGHT, buff=2)
        resting_character.next_to(clock_group, RIGHT, buff=2)
        
        # 감정 곡선 - 더 극적인 변화
        def create_emotion_curve(is_waiting):
            if is_waiting:
                return FunctionGraph(
                    lambda x: -0.8 * np.sin(x) - 1.5,
                    x_range=[0, 5],
                    color=RED
                )
            else:
                return FunctionGraph(
                    lambda x: 0.8 * np.sin(x) + 1.5,
                    x_range=[0, 5],
                    color=GREEN
                )
        
        waiting_curve = create_emotion_curve(True)
        resting_curve = create_emotion_curve(False)
        
        waiting_curve.next_to(waiting_character, UP, buff=1)
        resting_curve.next_to(resting_character, UP, buff=1)
        
        # 시계 바늘 - 더 화려한 디자인
        hour_hand = Line(ORIGIN, UP * 1.5, stroke_width=6, color=BLUE)
        minute_hand = Line(ORIGIN, UP * 2, stroke_width=4, color=RED)
        
        hands = VGroup(hour_hand, minute_hand)
        hands.move_to(clock.get_center())
        
        # 기다리는 장면 - 더 극적인 표현
        self.play(
            FadeIn(waiting_character, scale=1.5),
            Create(waiting_curve),
            Create(hands),
            run_time=1
        )
        
        # 5분 기다리는 애니메이션 - 더 지루해 보이게
        self.play(
            Rotate(minute_hand, angle=TAU/12, about_point=clock.get_center()),
            waiting_character.animate.scale(0.9).set_color(RED),
            rate_func=rate_functions.ease_in_sine,
            run_time=3
        )
        
        # 쉬는 장면으로 전환 - 더 극적인 변화
        self.play(
            ReplacementTransform(waiting_character, resting_character),
            ReplacementTransform(waiting_curve, resting_curve),
            rate_func=rate_functions.ease_out_bounce,
            run_time=1.5
        )
        
        # 5분 쉬는 애니메이션 - 더 즐거워 보이게
        self.play(
            Rotate(minute_hand, angle=TAU/12, about_point=clock.get_center()),
            resting_character.animate.scale(1.2).set_color(GREEN),
            rate_func=rate_functions.ease_out_bounce,
            run_time=1.5
        )
        
        # 마무리 - 더 임팩트 있는 메시지
        final_text = Text("시간은 상황에 따라 다르게 느껴집니다", font="Malgun Gothic", color=YELLOW)
        final_text.scale(1.2)
        final_text.to_edge(DOWN)
        
        self.play(
            Write(final_text),
            final_text.animate.scale(1.3).set_color(ORANGE),
            rate_func=rate_functions.there_and_back,
            run_time=2
        )
        
        # 마지막 장면에서 모든 요소가 함께 움직임
        self.play(
            *[mob.animate.scale(0.8) for mob in self.mobjects],
            rate_func=rate_functions.there_and_back,
            run_time=1.5
        )

    # --------------------------------------------------
    # Utility builders
    # --------------------------------------------------
    def build_clock(self):
        clock = Circle(radius=1.6)
        ticks = VGroup(*[
            Line(clock.point_at_angle(i * TAU / 12) * 0.88,
                 clock.point_at_angle(i * TAU / 12), stroke_width=2)
            for i in range(12)
        ])
        hour_hand = Line(ORIGIN, UP * 1.05, stroke_width=4)
        minute_hand = Line(ORIGIN, UP * 1.45, stroke_width=3)
        hands = VGroup(hour_hand, minute_hand).move_to(clock.get_center())
        return VGroup(clock, ticks, hands), hour_hand, minute_hand

    def emotion_curve(self, is_wait):
        func = (lambda x: -0.8 * np.sin(x) - 1.3) if is_wait else (lambda x: 0.8 * np.sin(x) + 1.3)
        color = RED if is_wait else GREEN
        curve = FunctionGraph(func, x_range=[0, 5], color=color, stroke_width=6).scale(0.6)
        return curve

    # --------------------------------------------------
    # Scene blocks
    # --------------------------------------------------
    def title_sequence(self):
        title = Text("시간의 상대성", font="NanumGothic", font_size=78, weight=BOLD)
        subtitle = Text("기다리는 5분 vs 쉬는 5분", font="NanumGothic", font_size=38)
        subtitle.next_to(title, DOWN)
        self.play(Write(title), run_time=3)
        self.play(FadeIn(subtitle), run_time=2)
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

    def waiting_sequence(self):
        # 세트 구축
        clock_grp, hour, minute = self.build_clock()
        clock_grp.to_edge(LEFT)
        wait_char = Text("😫", font_size=110)
        wait_char.next_to(clock_grp, RIGHT, buff=1.8)
        wait_curve = self.emotion_curve(True).next_to(wait_char, UP, buff=0.4)
        wait_label = Text("더 길게 느껴짐", font="NanumGothic", font_size=26, color=RED)
        wait_label.next_to(wait_curve, UP, buff=0.2)

        self.play(Create(clock_grp), FadeIn(wait_char), run_time=2)
        self.play(Create(wait_curve), FadeIn(wait_label), run_time=2)

        # 카메라 줌 → 분침 슬로우 모션
        self.play(self.camera.frame.animate.set(width=3).move_to(clock_grp), run_time=2)
        self.play(Rotate(minute, angle=TAU/12, about_point=clock_grp[0].get_center()),
                  run_time=self.WAIT_RT, rate_func=linear)
        self.play(self.camera.frame.animate.set(width=14).move_to(ORIGIN), run_time=2)
        self.wait(1)

        # 모든 오브젝트 전체 fade 살짝
        self.waiting_objects = VGroup(clock_grp, wait_char, wait_curve, wait_label)

    def resting_sequence(self):
        # 이전 오브젝트 슬라이드 왼쪽으로 페이드 → 새로운 세트 등장
        self.play(self.waiting_objects.animate.shift(LEFT*7).set_opacity(0.2), run_time=1.5)

        clock_grp, hour, minute = self.build_clock()
        clock_grp.to_edge(RIGHT)
        rest_char = Text("😌", font_size=110)
        rest_char.next_to(clock_grp, LEFT, buff=1.8)
        rest_curve = self.emotion_curve(False).next_to(rest_char, UP, buff=0.4)
        rest_label = Text("더 짧게 느껴짐", font="NanumGothic", font_size=26, color=GREEN)
        rest_label.next_to(rest_curve, UP, buff=0.2)

        self.play(Create(clock_grp), FadeIn(rest_char), run_time=1.5)
        self.play(Create(rest_curve), FadeIn(rest_label), run_time=1.5)
        self.play(Rotate(minute, angle=TAU/12, about_point=clock_grp[0].get_center()),
                  run_time=self.REST_RT, rate_func=linear)
        self.wait(1)

        self.resting_objects = VGroup(clock_grp, rest_char, rest_curve, rest_label)

    def comparison_sequence(self):
        # 이전 대기·휴식 세트 모두 중앙 정렬 → 동시 진행 비교
        left_set = self.waiting_objects.copy().shift(LEFT*3.5).set_opacity(1)
        right_set = self.resting_objects.copy().shift(RIGHT*3.5).set_opacity(1)
        self.add(left_set, right_set)
        self.play(
            self.waiting_objects.animate.fade(1),  # 원본은 사라짐
            self.resting_objects.animate.fade(1),
            run_time=1
        )

        # 클락 핸들 객체 얻기
        left_minute = left_set[0][2][1]  # clock, ticks, hands[ minute index 1 ]
        right_minute = right_set[0][2][1]
        # 동시에 회전(속도 차)
        self.play(
            Rotate(left_minute, angle=TAU/12, about_point=left_set[0][0].get_center()),
            Rotate(right_minute, angle=TAU/6, about_point=right_set[0][0].get_center()),  # 2배 빠름
            run_time=self.COMPARE_RT, rate_func=linear
        )
        self.wait(1)

    def outro_sequence(self):
        outro_text = Text("같은 5분도 상황·감정에 따라 다르게 느껴진다!", font="NanumGothic", font_size=40)
        self.play(Write(outro_text), run_time=4)
        self.wait(6)
        self.play(FadeOut(outro_text, shift=DOWN), run_time=2)
