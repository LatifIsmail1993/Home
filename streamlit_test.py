# Import packages
import pandas as pd
import yfinance as yf
import streamlit as st
import numpy as np
import time
from datetime import datetime, date

# Welcome title
st.title("Latif's Portfolio Analysis")

portfolio_dict = {
    "Microsoft": {"tick": "MSFT", "start_price": 120, "bought_date": date(2020, 1 ,1)},
    "Amazon": {"tick": "AMZN", "start_price": 120, "bought_date": date(2020, 1, 1)},
}

# Setup the initial webapp details and pull the relevant info
stock = st.selectbox('Which stock would you like to see?',
                     tuple(portfolio_dict.keys()))

tick = portfolio_dict[stock]["tick"]

col1, col2 = st.beta_columns((2))
with col1:
    start_date = st.date_input('Start Date', date(2019, 1, 1))
with col2:
    end_date = st.date_input('End Date', date.today())

df = yf.Ticker(tick)



# AMZN, CLB, CRWD, NIO, PURP, SHOP, WORK, SQ, TSLA, ZNGA

# get historical market data
hist = df.history(period="max")

# Close price
close = hist['Close'].reset_index()

close.Date = close.Date.apply(lambda x: x.strftime('%Y-%m-%d'))
close = close.loc[(close.Date >= start_date.strftime('%Y-%m-%d')) & (close.Date <= end_date.strftime('%Y-%m-%d'))]
close.Date = close.Date.apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
close.index = close.Date

close.drop('Date', axis=1, inplace=True)

st.write("Graphs for " + tick + ":")
st.line_chart(close)

close = close.reset_index()
final_df = pd.DataFrame({'Date': '', 'Close': ''}, index=[0])
chart1 = st.line_chart(x_axis=final_df.Date, y_axis=final_df.Close)
for i in range(len(close)):
    if i == 0:
        final_df = close.iloc[[i]]
    else:
        final_df = final_df.append(close.iloc[[i]])

    chart1.add_rows(final_df)


progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)
chart = st.line_chart(last_rows)

for i in range(1, 101):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    status_text.text("%i%% Complete" % i)
    chart.add_rows(new_rows)
    progress_bar.progress(i)
    last_rows = new_rows
    time.sleep(0.05)

progress_bar.empty()

