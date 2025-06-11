import streamlit as st

st.set_page_config(
    page_title="멀티페이지 앱",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 홈페이지")
st.write("환영합니다! 아래 링크를 통해 다른 페이지로 이동할 수 있습니다.")

# 페이지 링크 생성
st.page_link("pages/Page_1.py", label="▶ 페이지 1로 이동", icon="1️⃣")
st.page_link("pages/Page_2.py", label="▶ 페이지 2로 이동", icon="2️⃣")

# 사이드바에 정보 추가
with st.sidebar:
    st.header("📌 페이지 정보")
    st.write("이 앱은 Streamlit의 멀티페이지 기능을 보여주는 예제입니다.")
    st.write("사이드바에서도 페이지를 선택할 수 있습니다.") 