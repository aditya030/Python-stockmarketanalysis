from datetime import date, datetime
from jugaad_data.nse import stock_df
import pandas as pd
import matplotlib.pyplot as plt
import time

from functools import wraps



class StockMarketAnalysis:
    def __init__(self):
        self.stock_data = None
        
    def log_execution_time(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
           start_time = time.time()
           print(f"Executing {func.__name__}...")
           result = func(*args, **kwargs)
           end_time = time.time()
           print(f"{func.__name__} executed in {end_time - start_time:.2f} seconds.")
           return result
        return wrapper
   
    

    @staticmethod
    def get_user_input():
        try:
            stock_name = input("Enter the stock symbol: ").strip()
            start_date = input("Enter the start date (YYYY-MM-DD): ").strip()
            end_date = input("Enter the end date (YYYY-MM-DD): ").strip()

            # Validate and parse dates
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

            if start_date > end_date:
                raise ValueError("Start date cannot be after the end date.")

            return stock_name, start_date, end_date

        except ValueError as e:
            print(f"Invalid input: {e}")
            return None, None, None
        
    @log_execution_time
    @staticmethod
    def fetch_data(self, stock_name):
        try:
            df = stock_df(symbol=stock_name, from_date=date(2019,1,1),
                    to_date=date(2020,1,30), series="EQ")
            if df.empty:
                print("No data found for this stock.")
                return None
            return df
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    @staticmethod
    def clean_data(df):
        # Check for missing values
        if df.isnull().values.any():
            print("Missing values detected. Dropping null values...")
            df = df.dropna()

        # Ensure 'DATE' column is in datetime format
        if not pd.api.types.is_datetime64_any_dtype(df["DATE"]):
            df["DATE"] = pd.to_datetime(df["DATE"])

        return df

    @staticmethod
    def handle_weekend_or_holiday(date):
        if date.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
            raise ValueError(f"{date} falls on a weekend. Please enter a weekday.")
        return True

   
    @log_execution_time
    def analyze_stock(self):
        stock_name, start_date, end_date = self.get_user_input()
        if not (stock_name and start_date and end_date):
            return

    
        try:
            self.handle_weekend_or_holiday(start_date)
            self.handle_weekend_or_holiday(end_date)
        except ValueError as e:
            print(f"Input error: {e}")
            return

      
        self.stock_data = self.fetch_data(stock_name, start_date, end_date)
        if self.stock_data is None:
            return
        self.stock_data = self.clean_data(self.stock_data)

      
        print(f"\nStock Data Summary for {stock_name}:")
        print(self.stock_data.describe())

       


if __name__ == "__main__":
    app = StockMarketAnalysis()
    app.analyze_stock()
