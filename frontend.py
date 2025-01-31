import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from backend_script import StockMarketAnalysis

st.title("Stock Data Analysis Capstone Project")

stock_name = st.text_input("Enter Stock Name:", "SBIN")
stock_app = StockMarketAnalysis()

if 'df' not in st.session_state or st.session_state.stock_name != stock_name:
    if st.button("Get Data"):
        st.session_state.df = stock_app.fetch_data(stock_name)
        st.session_state.df = stock_app.clean_data(st.session_state.df)
        st.session_state.stock_name = stock_name  

if 'df' in st.session_state and not st.session_state.df.empty:
    df = st.session_state.df

    if 'DATE' in df.columns:
        df['DATE'] = pd.to_datetime(df['DATE'])
    if 'DATE' in df.columns:
        df.set_index('DATE', inplace=True)

    min_date = df.index.min().date()
    max_date = df.index.max().date()
    start_date = min_date
    end_date = max_date

    try:
        start_date, end_date = st.date_input(
            "Select date range", 
            [min_date, max_date], 
            min_value=min_date, 
            max_value=max_date
        )
    except ValueError as e:
        st.warning(f'Enter the second date!')


    if start_date and end_date:
        df_filtered = df[(df.index.date >= start_date) & (df.index.date <= end_date)]
        
        if df_filtered.empty:
            st.error(f"No data available between {start_date} and {end_date}.")
        else:
            st.write("### Stock Data", df_filtered)

            df_with_daily_change = stock_app.calulate_daily_percentage_change(df_filtered)
            st.write("### Daily Percentage Change", df_with_daily_change[['OPEN', 'CLOSE', 'Daily_%_change']])

            volatility = stock_app.calculate_volatility(df_with_daily_change)
            st.write(f"### Volatility: {volatility:.2f}%")

            avg_close = stock_app.group_and_average(df_filtered).round(2)
            st.write("### Average Close Price by",stock_name," ", avg_close)

            fig, axes = plt.subplots(3, 1, figsize=(10, 12))
            

            # candlestick plot (referred from gfg)
            up = df_filtered[df_filtered['CLOSE'] >= df_filtered['OPEN']]
            down = df_filtered[df_filtered['CLOSE'] < df_filtered['OPEN']]

            col_up = 'green'
            col_down = 'red'
            width = 0.5
            width2 = 0.1
            axes[0].bar(up.index, up['CLOSE'] - up['OPEN'], width, bottom=up['OPEN'], color=col_up)
            axes[0].bar(up.index, up['HIGH'] - up['CLOSE'], width2, bottom=up['CLOSE'], color=col_up)
            axes[0].bar(up.index, up['LOW'] - up['OPEN'], width2, bottom=up['OPEN'], color=col_up)

            axes[0].bar(down.index, down['CLOSE'] - down['OPEN'], width, bottom=down['OPEN'], color=col_down)
            axes[0].bar(down.index, down['HIGH'] - down['OPEN'], width2, bottom=down['OPEN'], color=col_down)
            axes[0].bar(down.index, down['LOW'] - down['CLOSE'], width2, bottom=down['CLOSE'], color=col_down)

            axes[0].set_title("Candlestick Chart - Open vs Close Prices")
            axes[0].set_ylabel("Price")
            axes[0].tick_params(axis='x', rotation=30)

            
            axes[1].plot(df_filtered.index, df_filtered['HIGH'], color='blue', label='High', linewidth=1)
            axes[1].plot(df_filtered.index, df_filtered['LOW'], color='orange', label='Low', linewidth=1)
            axes[1].set_title("High and Low Prices")
            axes[1].legend()
            axes[1].set_ylabel("Price")
            
            axes[2].bar(df_filtered.index, df_filtered['VOLUME'], color='gray')
            axes[2].set_title("Trading Volume")
            axes[2].set_ylabel("Volume")
            
            plt.subplots_adjust(hspace=10)
            plt.tight_layout()
            st.pyplot(fig)
else:
    st.error("No data available")
