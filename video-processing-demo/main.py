import cv2
import numpy as np
from moviepy.editor import VideoFileClip, concatenate_videoclips
from mtcnn import MTCNN
import whisper
from tqdm import tqdm
import os
import moviepy
import moviepy.editor

# 1. 모션 감지 (프레임 차분)
def motion_detection(video_path, threshold=30, output_path="motion_output.mp4"): 
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

    ret, prev = cap.read()
    if not ret:
        print("비디오를 읽을 수 없습니다.")
        return
    prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

    pbar = tqdm(total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), desc="모션 감지")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(prev_gray, gray)
        _, mask = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
        # 움직임 영역 표시
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            if cv2.contourArea(cnt) > 500:
                x, y, w_box, h_box = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x+w_box, y+h_box), (0,0,255), 2)
        out.write(frame)
        prev_gray = gray
        pbar.update(1)
    pbar.close()
    cap.release()
    out.release()
    print(f"모션 감지 결과 저장: {output_path}")

# 2. 배경 제거 (MOG2)
def background_subtraction(video_path, output_path="bg_sub_output.mp4"):
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))
    fgbg = cv2.createBackgroundSubtractorMOG2()
    pbar = tqdm(total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), desc="배경 제거")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        fgmask = fgbg.apply(frame)
        fg = cv2.bitwise_and(frame, frame, mask=fgmask)
        out.write(fg)
        pbar.update(1)
    pbar.close()
    cap.release()
    out.release()
    print(f"배경 제거 결과 저장: {output_path}")

# 3. 얼굴 검출 및 블러링 (MTCNN + Gaussian Blur)
def face_blur(video_path, output_path="face_blur_output.mp4"):
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))
    detector = MTCNN()
    pbar = tqdm(total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), desc="얼굴 블러")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = detector.detect_faces(rgb)
        for face in faces:
            x, y, w_box, h_box = face['box']
            x, y = max(0, x), max(0, y)
            face_roi = frame[y:y+h_box, x:x+w_box]
            if face_roi.size == 0:
                continue
            blur = cv2.GaussianBlur(face_roi, (51, 51), 0)
            frame[y:y+h_box, x:x+w_box] = blur
        out.write(frame)
        pbar.update(1)
    pbar.close()
    cap.release()
    out.release()
    print(f"얼굴 블러 결과 저장: {output_path}")

# 4. 비디오 요약 (Whisper + 객체/장면 감지)
def video_summarization(video_path, output_path="summary_output.mp4", min_clip_len=2):
    # 1) Whisper로 음성 전사
    model = whisper.load_model("tiny")
    print("Whisper로 음성 전사 중...")
    result = model.transcribe(video_path)
    segments = result['segments']
    print("음성 전사 완료. 중요 구간 추출 중...")
    # 2) 키워드/음성 변화가 있는 구간만 추출 (예시: segment별로 2초 이상만)
    clips = []
    for seg in segments:
        start = seg['start']
        end = seg['end']
        if end - start >= min_clip_len:
            clips.append((start, end))
    # 3) MoviePy로 해당 구간만 추출
    video = VideoFileClip(video_path)
    subclips = [video.subclip(start, end) for start, end in clips]
    if subclips:
        final = concatenate_videoclips(subclips)
        final.write_videofile(output_path)
        print(f"비디오 요약 결과 저장: {output_path}")
    else:
        print("요약할 구간이 없습니다.")

# 5. 하이라이트 추출 (움직임 급증 or 객체 등장)
def extract_highlights(video_path, output_path="highlight_output.mp4", motion_threshold=40, min_area=1000):
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    highlight_frames = []
    ret, prev = cap.read()
    if not ret:
        print("비디오를 읽을 수 없습니다.")
        return
    prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    idx = 1
    pbar = tqdm(total=frame_count, desc="하이라이트 추출")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(prev_gray, gray)
        _, mask = cv2.threshold(diff, motion_threshold, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        motion = sum([cv2.contourArea(cnt) for cnt in contours])
        if motion > min_area:
            highlight_frames.append(idx)
        prev_gray = gray
        idx += 1
        pbar.update(1)
    pbar.close()
    # 하이라이트 프레임만 모아서 저장 (간단히 연속 구간만 추출)
    if not highlight_frames:
        print("하이라이트 프레임이 없습니다.")
        return
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))
    idx = 0
    frame_idx = 0
    highlight_set = set(highlight_frames)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx in highlight_set:
            out.write(frame)
        frame_idx += 1
    cap.release()
    out.release()
    print(f"하이라이트 추출 결과 저장: {output_path}")

if __name__ == "__main__":
    print("비디오 처리 데모: main.py 실행")
    print("테스트용 input.mp4 파일이 필요합니다.")
    test_video = "input.mp4"  # 같은 폴더에 테스트용 비디오 파일 필요
    if os.path.exists(test_video):
        motion_detection(test_video)
        background_subtraction(test_video)
        face_blur(test_video)
        video_summarization(test_video)
        extract_highlights(test_video)
    else:
        print("input.mp4 파일을 video-processing-demo 폴더에 넣어주세요.")

print(moviepy.__file__)
print(moviepy.editor.__file__) 