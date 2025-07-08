import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# 페이지 설정: wide 모드 활성화
st.set_page_config(page_title="📊 VIX 차트", page_icon="📉", layout="wide")

# 스트림릿 웹 앱 제목
st.title("Stock Back Test")

# 종목 리스트
tickers = ["SPY", "QQQ", "QLD", "TQQQ"]


col1, col2, col3 = st.columns([1, 1, 3])

# 사용자 입력: 종목 선택 및 날짜 범위 설정
selected_ticker = col1.selectbox("Select ETF", tickers)
invest = col2.number_input("월 투자금", value=100000, step=10000)

# 날짜 범위 설정
min_date = datetime(2000, 1, 1)  # 슬라이더 시작 날짜 (datetime)
max_date = datetime.combine(date.today(), datetime.min.time())  # 오늘 날짜를 datetime으로 변환

# 날짜 범위 슬라이더
start_date, end_date = st.slider(
    "Select Date Range:",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),  # 기본 선택 범위
    format="YYYY-MM-DD"  # 날짜 형식
)


# 데이터 다운로드 함수
@st.cache_data
def get_stock_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    data.reset_index(inplace=True)
    data["Ticker"] = ticker
    return data


stock_data = get_stock_data(selected_ticker, start_date, end_date)






# 'Date' 열을 datetime으로 변환
stock_data['Date'] = pd.to_datetime(stock_data['Date'])

# 월말 데이터가 아닌 각 월의 마지막 데이터 선택
stock_data['YearMonth'] = stock_data['Date'].dt.to_period('M')  # 연도-월 단위로 그룹화
month_end_data = stock_data.groupby('YearMonth').tail(1)  # 각 월의 마지막 데이터 선택

# Adj Close 열만 추출
adj_close_data = month_end_data[['Date', 'Close']]


# Adj Close 값을 소수점 2자리로 반올림
adj_close_data['Close'] = adj_close_data['Close'].round(2)


# MultiIndex 헤더 처리
if isinstance(adj_close_data.columns, pd.MultiIndex):
    adj_close_data.columns = adj_close_data.columns.get_level_values(0)  # 첫 번째 헤더만 유지


# end_date와 같은 날짜의 Adj Close 값 가져오기
selected_date_adj_close = stock_data.loc[stock_data['Date'] == pd.to_datetime(end_date), 'Close']

# 값이 존재할 경우 처리
if not selected_date_adj_close.empty:
    selected_adj_close_value = selected_date_adj_close.values[0]
else:
    # 정확히 end_date가 없으면 가장 가까운 이전 날짜의 값 선택
    closest_date_row = stock_data.loc[stock_data['Date'] <= pd.to_datetime(end_date)].tail(1)
    if not closest_date_row.empty:
        selected_adj_close_value = closest_date_row['Close'].values[0]
    else:
        selected_adj_close_value = None  # 데이터가 완전히 없을 경우 처리

# 선택한 Adj Close 값을 소수점 셋째 자리에서 반올림
if selected_adj_close_value is not None:
    selected_adj_close_value = round(float(selected_adj_close_value), 2)  # 단일 값으로 변환 후 반올림

# 선택한 값을 모든 행에 반복적으로 할당
adj_close_data['Selected Close'] = [selected_adj_close_value] * len(adj_close_data)


# 수익률 추가
adj_close_data['수익률'] = (adj_close_data['Selected Close'] / adj_close_data['Close'] - 1) * 100

# 소수점 2자리로 반올림
adj_close_data['수익률'] = adj_close_data['수익률'].round(0).astype(int)

# 백분율 값에 콤마 추가 및 % 기호 붙이기
adj_close_data['수익률'] = adj_close_data['수익률'].apply(lambda x: f"{x:,}%" if pd.notnull(x) else None)



# 월 투자금 추가
adj_close_data['월 투자금'] = [invest] * len(adj_close_data)




# 현재 금액 추가
adj_close_data['현재금액'] = adj_close_data['월 투자금'] * (adj_close_data['Selected Close'] / adj_close_data['Close'])

adj_close_data['현재금액'] = adj_close_data['현재금액'].round(0).astype(int)






# Date 열에서 시간 단위 제거 (날짜 형식으로 변환)
adj_close_data['Date'] = adj_close_data['Date'].dt.date

# start_date와 end_date의 시간 단위를 제거
start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")

#데이터프레임 표시
st.write(f"{selected_ticker} backtest result from {start_date_str} to {end_date_str}")
adj_close_data.rename(columns={
    'Date': 'Date', 
    'Close': 'Stock Price',
    'Selected Close': '현재가'
}, inplace=True)


col1, col2 = st.columns([2, 1])
col1.dataframe(adj_close_data, use_container_width=True)

total_invest = invest * len(adj_close_data)
total_amount = adj_close_data['현재금액'].sum()
total_rate = ((total_amount / total_invest)*100).round(1)

col2.write(f"투자금액 : {total_invest:,}원")
col2.write(f"투자 수익률 : {total_rate:,}%")
col2.write(f"최종 금액 : {total_amount:,}원")



st.title(f"{selected_ticker}")

# 월말 Adj Close 데이터 시각화
fig = px.line(adj_close_data, x="Date", y="Stock Price")
st.plotly_chart(fig)





# 모든 데이터 통합 (선택)
if st.checkbox("Show all stocks combined"):
    all_data = pd.concat([get_stock_data(ticker, start_date, end_date) for ticker in tickers])
    st.write("Combined data for all stocks:")
    st.dataframe(all_data.head())
