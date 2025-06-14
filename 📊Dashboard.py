import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from datetime import timedelta

st.set_page_config(
    page_icon="📉",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.sidebar.success("☝ 메뉴에서 페이지를 선택하세요!")


# ✅ VIX 데이터 로딩
vix = yf.Ticker("^VIX")
vix_data = vix.history(period="max", interval="1d").round(2).reset_index()
vix_data["Date"] = pd.to_datetime(vix_data["Date"]).dt.date  # 시간 제거하여 date만 남김


# ✅ 필터링 가능한 범위 설정
min_date = vix_data["Date"].min()
max_date = vix_data["Date"].max()
default_start = min_date
default_end = max_date

# ✅ 날짜 슬라이더 (모두 date 타입)
start_date, end_date = st.slider(
    "📅 표시할 날짜 범위 선택",
    min_value=min_date,
    max_value=max_date,
    value=(default_start, default_end),
    format="YYYY-MM-DD"
)

# ✅ 필터링
filtered_data = vix_data[
    (vix_data["Date"] >= start_date) & (vix_data["Date"] <= end_date)
]


# ✅ 평균 및 최신 데이터 계산
mean_value = filtered_data["Close"].mean()
latest_value = filtered_data["Close"].iloc[-1]
latest_date = filtered_data["Date"].iloc[-1]

# ✅ 레이아웃 구성
col1, col2 = st.columns([1, 1])

with col1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=filtered_data["Date"],
        y=filtered_data["Close"],
        name="VIX",
        line=dict(color="white")
    ))

    fig.add_hline(
        y=mean_value,
        line=dict(color="red", dash="dash"),
        annotation_text=f"평균: {mean_value:.2f}",
        annotation_position="top right"
    )

    fig.update_layout(
        title=f"VIX 공포 지수 : {latest_value}",
        height=500,
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

