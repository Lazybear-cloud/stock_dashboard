import yfinance as yf
import streamlit as st
import requests
from bs4 import BeautifulSoup

# VIX 데이터
vix = yf.Ticker("^VIX")
vix_data = vix.history(period="1mo")

# 공포탐욕지수 스크래핑 함수
def get_fear_greed_index():
    url = "https://edition.cnn.com/markets/fear-and-greed"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    try:
        fg_value = soup.find("span", class_="market-fng-gauge__dial-number-value").text.strip()
        return fg_value
    except:
        return "지수 추출 실패"

# Streamlit UI
st.title("📊 시장 심리 대시보드")

# VIX 시각화
st.subheader("VIX (공포 지수)")
st.line_chart(vix_data["Close"])

# Fear & Greed Index 출력
st.subheader("CNN 공포 & 탐욕 지수")
fg_index = get_fear_greed_index()
st.write("ㅇㅇㅇ", fg_index)
st.metric(label="현재 탐욕 지수", value=fg_index)

st.markdown(f"### 😬 현재 공포탐욕지수: **{fg_index}**")
