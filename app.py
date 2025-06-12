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



one_year_ago = pd.Timestamp.today() - pd.Timedelta(days=365)
vix_last_year = vix_data[vix_data.index >= one_year_ago]


# 날짜 범위 선택 슬라이더
start_date = st.date_input("시작 날짜", one_year_ago.date())
end_date = st.date_input("종료 날짜", vix_data.index[-1].date())

# 선택된 범위로 필터링
filtered_data = vix_data.loc[start_date:end_date]

# 그래프 출력
st.line_chart(filtered_data["Close"])






