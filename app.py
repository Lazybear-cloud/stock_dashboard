import requests
import yfinance as yf
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup

# VIX 데이터
vix = yf.Ticker("^VIX")
vix_data = vix.history(period="max", interval="1d").round(2)

sp500 = yf.Ticker("^GSPC")
sp500_data = sp500.history(period="1mo")

nasdaq = yf.Ticker("^IXIC")
nasdaq_data = nasdaq.history(period="1mo")

# Streamlit UI
st.title("📊 시장 심리 대시보드")

# VIX 시각화
st.subheader(f"VIX (공포 지수):{vix_data["Close"].iloc[-1]}")
st.line_chart(vix_data["Close"])




# 평균값 계산
mean_value = vix_data["Close"].mean()

# Streamlit에 출력
st.subheader(f"VIX (공포 지수): {vix_data['Close'].iloc[-1]} (기준일: {vix_data.index[-1].date()})")

# 그래프 그리기
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(vix_data.index, vix_data["Close"], label="VIX")
ax.axhline(mean_value, color="red", linestyle="--", label=f"평균: {mean_value:.2f}")
ax.legend()
ax.set_title("VIX (공포 지수) 추이")
ax.set_xlabel("날짜")
ax.set_ylabel("지수")

# Streamlit에 그래프 표시
st.pyplot(fig)





