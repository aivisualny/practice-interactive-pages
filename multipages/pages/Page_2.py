import streamlit as st

st.set_page_config(
    page_title="페이지 2",
    page_icon="2️⃣",
    layout="wide"
)

st.title("2️⃣ 페이지 2")
st.write("이것은 두 번째 페이지입니다.")

# 홈으로 돌아가는 링크
st.page_link("Home.py", label="🏠 홈으로 돌아가기", icon="🏠")

# 페이지 2의 특별한 기능
with st.expander("🎨 인터랙티브 위젯 예제"):
    # 슬라이더
    number = st.slider("숫자를 선택하세요", 0, 100, 50)
    st.write(f"선택한 숫자: {number}")
    
    # 체크박스
    if st.checkbox("추가 옵션 보기"):
        st.write("추가 옵션이 활성화되었습니다!")
        
    # 라디오 버튼
    option = st.radio(
        "선호하는 색상을 선택하세요",
        ["빨강", "파랑", "초록"]
    )
    st.write(f"선택한 색상: {option}") 