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
