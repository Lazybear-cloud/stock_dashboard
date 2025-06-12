import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# 📌 타이틀
st.title("📉 VIX (공포 지수) 시각화 대시보드")

# ✅ VIX 데이터 불러오기 및 Date 컬럼 처리
vix = yf.Ticker("^VIX")
vix_data = vix.history(period="max", interval="1d").round(2).reset_index()

# 🔧 Date 컬럼이 datetime 타입인지 확실히 변환
vix_data["Date"] = pd.to_datetime(vix_data["Date"])

# ✅ 날짜 슬라이더
min_date = vix_data["Date"].min()
max_date = vix_data["Date"].max()

start_date, end_date = st.slider(
    "📅 표시할 날짜 범위 선택",
    min_value=min_date,
    max_value=max_date,
    value=(max_date - pd.Timedelta(days=365), max_date),
    format="YYYY-MM-DD"
)

# ✅ 날짜 필터링 (타입 동일하므로 에러 없음)
filtered_data = vix_data[
    (vix_data["Date"] >= start_date) & (vix_data["Date"] <= end_date)
]

# ✅ 평균값 및 최신값 계산
mean_value = filtered_data["Close"].mean()
latest_value = filtered_data["Close"].iloc[-1]
latest_date = filtered_data["Date"].iloc[-1].date()

# ✅ 2컬럼 레이아웃 구성
col1, col2 = st.columns([1, 1])

# ✅ col1: Plotly 차트
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
        title=f"VIX 공포 지수 ({start_date.date()} ~ {end_date.date()})",
        xaxis_title="날짜",
        yaxis_title="지수",
        height=500,
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

# ✅ col2: 수치 정보
with col2:
    st.subheader("📌 최신 정보")
    st.metric("VIX", f"{latest_value}")
    st.write(f"📅 기준일: **{latest_date}**")
    st.write(f"📊 평균값: **{mean_value:.2f}**")
