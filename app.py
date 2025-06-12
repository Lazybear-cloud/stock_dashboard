import requests
import yfinance as yf
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import altair as alt
import plotly.graph_objs as go

# VIX 데이터
vix = yf.Ticker("^VIX")
vix_data = vix.history(period="max", interval="1d").round(2)

sp500 = yf.Ticker("^GSPC")
sp500_data = sp500.history(period="1mo")

nasdaq = yf.Ticker("^IXIC")
nasdaq_data = nasdaq.history(period="1mo")

# 평균값 먼저 계산
mean_value = vix_data["Close"].mean()

chart = alt.Chart(vix_data.reset_index()).mark_line().encode(
    x='Date:T',
    y='Close:Q'
)

mean_line = alt.Chart(pd.DataFrame({'y': [mean_value]})).mark_rule(
    color='red', strokeDash=[5,5]
).encode(y='y')

st.altair_chart(chart + mean_line, use_container_width=True)


fig = go.Figure()
fig.add_trace(go.Scatter(x=vix_data.index, y=vix_data["Close"], name="VIX"))
fig.add_hline(y=mean_value, line=dict(color="red", dash="dash"), name="평균선")
fig.update_layout(title="VIX 공포 지수", xaxis_title="날짜", yaxis_title="지수")

st.plotly_chart(fig, use_container_width=True)

# 데이터 불러오기
vix = yf.Ticker("^VIX")
vix_data = vix.history(period="max", interval="1d").round(2).reset_index()

# 평균값 먼저 계산
mean_value = vix_data["Close"].mean()

# 기본 차트
vix_chart = alt.Chart(vix_data).mark_line().encode(
    x='Date:T',
    y='Close:Q',
    tooltip=['Date:T', 'Close:Q']
)

# 평균선 차트
mean_line = alt.Chart(pd.DataFrame({'y': [mean_value]})).mark_rule(
    color='red', strokeDash=[5,5]
).encode(y='y:Q')

# 차트 합치기
st.altair_chart(vix_chart + mean_line, use_container_width=True)

# 최신값 정보 출력
latest_value = vix_data["Close"].iloc[-1]
latest_date = vix_data["Date"].iloc[-1].date()
st.subheader(f"VIX (공포 지수): {latest_value} (기준일: {latest_date})")
