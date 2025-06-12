import requests
import yfinance as yf
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import altair as alt
import plotly.graph_objs as go

# 📈 보조 데이터 (사용 안해도 괜찮지만 유지)
sp500 = yf.Ticker("^GSPC")
sp500_data = sp500.history(period="1mo")

nasdaq = yf.Ticker("^IXIC")
nasdaq_data = nasdaq.history(period="1mo")

# 📌 타이틀
st.title("📉 VIX (공포 지수) 시각화 대시보드")

# ✅ VIX 데이터 불러오기
vix = yf.Ticker("^VIX")
vix_data = vix.history(period="max", interval="1d").round(2).reset_index()

# ✅ 날짜 슬라이더 (기본: 최근 1년)
min_date = vix_data["Date"].min().date()
max_date = vix_data["Date"].max().date()

start_date, end_date = st.slider(
    "📅 표시할 날짜 범위 선택",
    min_value=min_date,
    max_value=max_date,
    value=(max_date.replace(year=max_date.year - 1), max_date),
    format="YYYY-MM-DD"
)

# ✅ 선택된 날짜 범위로 필터링
filtered_data = vix_data[
    (vix_data["Date"] >= pd.to_datetime(start_date)) &
    (vix_data["Date"] <= pd.to_datetime(end_date))
]

# ✅ 평균값 및 최신값 재계산
mean_value = filtered_data["Close"].mean()
latest_value = filtered_data["Close"].iloc[-1]
latest_date = filtered_data["Date"].iloc[-1].date()

# ✅ 2컬럼 레이아웃 구성
col1, col2 = st.columns([1, 1])

with col1:
    # ✅ Plotly 그래프 생성
    fig = go.Figure()

    # VIX 선 그래프
    fig.add_trace(go.Scatter(
        x=filtered_data["Date"],
        y=filtered_data["Close"],
        name="VIX",
        line=dict(color="blue")
    ))

    # 평균선 추가
    fig.add_hline(
        y=mean_value,
        line=dict(color="red", dash="dash"),
        annotation_text=f"평균: {mean_value:.2f}",
        annotation_position="top right"
    )

    # 그래프 레이아웃 설정
    fig.update_layout(
        title=f"VIX 공포 지수 : {latest_value}",
        height=500,
        template="plotly_white",
        xaxis_title="날짜",
        yaxis_title="지수"
    )

    # ✅ Streamlit에 그래프 출력
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📌 최신 정보")
    st.metric("VIX", f"{latest_value}")
    st.write(f"📅 기준일: **{latest_date}**")
    st.write(f"📊 평균값: **{mean_value:.2f}**")
