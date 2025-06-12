import requests
import yfinance as yf
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import altair as alt
import plotly.graph_objs as go

sp500 = yf.Ticker("^GSPC")
sp500_data = sp500.history(period="1mo")

nasdaq = yf.Ticker("^IXIC")
nasdaq_data = nasdaq.history(period="1mo")

# 📌 타이틀
st.title("📉 VIX (공포 지수) 시각화 대시보드")

# ✅ VIX 데이터 불러오기
vix = yf.Ticker("^VIX")
vix_data = vix.history(period="max", interval="1d").round(2)

# ✅ 평균값 계산
mean_value = vix_data["Close"].mean()

# ✅ 최신 값 출력
latest_value = vix_data["Close"].iloc[-1]
latest_date = vix_data.index[-1].date()

with col1
    # ✅ Plotly 그래프 생성
    fig = go.Figure()
    
    # VIX 선 그래프
    fig.add_trace(go.Scatter(
        x=vix_data.index,
        y=vix_data["Close"],
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
        xaxis_title="날짜",
        yaxis_title="지수",
        height=500,
        template="plotly_white"
    )
    
    # ✅ Streamlit에 그래프 출력
    st.plotly_chart(fig, use_container_width=True)




