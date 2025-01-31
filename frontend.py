import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from backend_script import StockMarketAnalysis

st.title("Stock Data Analysis Capstone Project")

stock_name = st.text_input("Enter Stock Name:", "SBIN")

if 'df' not in st.session_state or st.session_state.stock_name != stock_name:
    if st.button("Get Data"):
        stock_app = StockMarketAnalysis()
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

    start_date, end_date = st.date_input(
        "Select date range", 
        [min_date, max_date], 
        min_value=min_date, 
        max_value=max_date
    )

    if start_date and end_date:
        df_filtered = df[(df.index.date >= start_date) & (df.index.date <= end_date)]
        
        if df_filtered.empty:
            st.error(f"No data available between {start_date} and {end_date}.")
        else:
            st.write("### Filtered Stock Data", df_filtered)
            fig, axes = plt.subplots(3, 1, figsize=(10, 12))
            
            up = df_filtered[df_filtered['CLOSE'] >= df_filtered['OPEN']]
            down = df_filtered[df_filtered['CLOSE'] < df_filtered['OPEN']]

            col_up = 'green'
            col_down = 'red'
            width = 0.5
            width2 = 0.1
            # Plotting up prices (when CLOSE >= OPEN)
            axes[0].bar(up.index, up['CLOSE'] - up['OPEN'], width, bottom=up['OPEN'], color=col_up)
            axes[0].bar(up.index, up['HIGH'] - up['CLOSE'], width2, bottom=up['CLOSE'], color=col_up)
            axes[0].bar(up.index, up['LOW'] - up['OPEN'], width2, bottom=up['OPEN'], color=col_up)

            # Plotting down prices (when CLOSE < OPEN)
            axes[0].bar(down.index, down['CLOSE'] - down['OPEN'], width, bottom=down['OPEN'], color=col_down)
            axes[0].bar(down.index, down['HIGH'] - down['OPEN'], width2, bottom=down['OPEN'], color=col_down)
            axes[0].bar(down.index, down['LOW'] - down['CLOSE'], width2, bottom=down['CLOSE'], color=col_down)

            # Formatting
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
            
            plt.tight_layout()
            st.pyplot(fig)
else:
    st.error("no data available")
