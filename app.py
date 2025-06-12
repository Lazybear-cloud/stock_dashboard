import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta

# 📌 타이틀
st.title("📉 VIX (공포 지수) 시각화 대시보드")

# ✅ VIX 데이터 로딩
vix = yf.Ticker("^VIX")
vix_data = vix.history(period="max", interval="1d").round(2).reset_index()

# ✅ Date 컬럼 타입 확실히 datetime64로 변환
vix_data["Date"] = pd.to_datetime(vix_data["Date"], errors='coerce')

# ✅ 필터링 가능한 범위 설정
min_date = vix_data["Date"].min().to_pydatetime().date()
max_date = vix_data["Date"].max().to_pydatetime().date()
default_start = max_date - timedelta(days=365)
default_end = max_date

# ✅ 날짜 슬라이더 (모두 date 타입)
start_date, end_date = st.slider(
    "📅 표시할 날짜 범위 선택",
    min_value=min_date,
    max_value=max_date,
    value=(default_start, default_end),
    format="YYYY-MM-DD"
)

# ✅ 슬라이더 값 → datetime64로 변환 (비교를 위해)
start_ts = pd.to_datetime(start_date)
end_ts = pd.to_datetime(end_date)

st.wirite(start_ts)

# ✅ 날짜 필터링
filtered_data = vix_data[(vix_data["Date"] >= start_ts) & (vix_data["Date"] <= end_ts)]

# ✅ 평균 및 최신 데이터 계산
mean_value = filtered_data["Close"].mean()
latest_value = filtered_data["Close"].iloc[-1]
latest_date = filtered_data["Date"].iloc[-1].date()

# ✅ 레이아웃 구성
col1, col2 = st.columns([1, 1])

# 📈 차트 출력
with col1:
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=filtered_data["Date"],
        y=filtered_data["Close"],
        name="VIX",
        line=dict(color="blue")
    ))

    fig.add_hline(
        y=mean_value,
        line=dict(color="red", dash="dash"),
        annotation_text=f"평균: {mean_value:.2f}",
        annotation_position="top right"
    )

    fig.update_layout(
        title=f"VIX 공포 지수 ({start_date} ~ {end_date})",
        xaxis_title="날짜",
        yaxis_title="지수",
        height=500,
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

# 📊 수치 요약
with col2:
    st.subheader("📌 최신 정보")
    st.metric(label="VIX", value=f"{latest_value}")
    st.write(f"📅 기준일: **{latest_date}**")
    st.write(f"📊 평균값: **{mean_value:.2f}**")
