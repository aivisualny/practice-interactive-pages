import streamlit as st
import cv2
import numpy as np
from PIL import Image
import ffmpeg
import tempfile
import os

st.title('OpenCV & FFmpeg Python 실습 데모')

# 탭 구성: OpenCV 실습 / FFmpeg 실습
tab1, tab2 = st.tabs(["OpenCV 실습", "FFmpeg 실습"])

# OpenCV 실습 탭: 이미지 업로드 및 그레이스케일 변환
def opencv_tab():
    st.header("OpenCV: 이미지 처리")
    uploaded_file = st.file_uploader("이미지 파일 업로드", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="원본 이미지", use_column_width=True)
        img_array = np.array(image)
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        st.image(gray, caption="Grayscale 변환 결과", use_column_width=True)

# FFmpeg 실습 탭: 비디오 업로드, 썸네일 추출 및 다운로드
def ffmpeg_tab():
    st.header("FFmpeg: 비디오 썸네일 추출")
    video_file = st.file_uploader("비디오 파일 업로드", type=["mp4", "avi", "mov", "mkv"], key="video")
    if video_file is not None:
        # 업로드된 비디오를 임시 파일로 저장
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        tfile.write(video_file.read())
        tfile.close()
        # 썸네일(첫 프레임) 추출
        thumb_path = tfile.name + '_thumb.jpg'
        (
            ffmpeg
            .input(tfile.name, ss=0)
            .output(thumb_path, vframes=1)
            .run(overwrite_output=True, quiet=True)
        )
        # 썸네일 이미지 표시
        thumb_img = Image.open(thumb_path)
        st.image(thumb_img, caption="썸네일 (첫 프레임)", use_column_width=True)
        # 썸네일 다운로드 버튼
        with open(thumb_path, "rb") as f:
            st.download_button(
                label="썸네일 이미지 다운로드",
                data=f,
                file_name="thumbnail.jpg",
                mime="image/jpeg"
            )
        # 임시 파일 정리
        os.remove(thumb_path)
        os.remove(tfile.name)

# 각 탭에 함수 연결
with tab1:
    opencv_tab()
with tab2:
    ffmpeg_tab()