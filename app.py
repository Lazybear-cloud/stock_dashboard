import requests
import yfinance as yf
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup

# VIX 데이터
vix = yf.Ticker("^VIX")
vix_data = vix.history(period="1mo")


# Streamlit UI
st.title("📊 시장 심리 대시보드")

# VIX 시각화
st.subheader("VIX (공포 지수)")
st.line_chart(vix_data["Close"])


def get_fear_greed_index_history(start_date="2020-01-01"):
    url = f"https://production.dataviz.cnn.io/index/fearandgreed/graphdata/{start_date}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    try:
        data = response.json().get("fear_and_greed_historical", {}).get("data", [])
        df = pd.DataFrame([
            {"date": pd.to_datetime(item["x"], unit="ms"), "fg": item["y"]}
            for item in data
        ])
        return df
    except Exception as e:
        print("JSON decoding error:", e)
        return pd.DataFrame()
