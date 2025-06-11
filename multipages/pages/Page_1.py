import streamlit as st

st.set_page_config(
    page_title="페이지 1",
    page_icon="1️⃣",
    layout="wide"
)

st.title("1️⃣ 페이지 1")
st.write("이것은 첫 번째 페이지입니다.")

# 홈으로 돌아가는 링크
st.page_link("Home.py", label="🏠 홈으로 돌아가기", icon="🏠")

# 페이지 1의 특별한 기능
with st.expander("📊 데이터 시각화 예제"):
    import numpy as np
    import pandas as pd
    
    # 샘플 데이터 생성
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['A', 'B', 'C']
    )
    
    st.line_chart(chart_data) 