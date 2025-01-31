import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from backend_script import StockMarketAnalysis

st.title("Stock Data Analysis")

# User input for stock name
stock_name = st.text_input("Enter Stock Name:", "RELIANCE")

# Cache the stock data fetching process only if stock data is not already loaded
if 'df' not in st.session_state or st.session_state.stock_name != stock_name:
    if st.button("Get Data"):
        stock_app = StockMarketAnalysis()
        st.session_state.df = stock_app.fetch_data(stock_name)
        st.session_state.df = stock_app.clean_data(st.session_state.df)
        st.session_state.stock_name = stock_name  # Save the stock name for session

if 'df' in st.session_state and not st.session_state.df.empty:
    df = st.session_state.df

    if 'DATE' in df.columns:
        df['DATE'] = pd.to_datetime(df['DATE'])
    if 'DATE' in df.columns:
        df.set_index('DATE', inplace=True)

    # Get min and max date for user selection
    min_date = df.index.min().date()
    max_date = df.index.max().date()

    # Ask the user to select date range
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
            
            axes[0].bar(df_filtered.index, df_filtered['CLOSE'] - df_filtered['OPEN'], bottom=df_filtered['OPEN'], 
                        color=['green' if c >= o else 'red' for c, o in zip(df_filtered['CLOSE'], df_filtered['OPEN'])], width=0.5)
            axes[0].set_title("Open vs Close Prices")
            axes[0].set_ylabel("Price")
            
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
    st.error("No data available. Please enter a valid stock name and click 'Get Data'.")
