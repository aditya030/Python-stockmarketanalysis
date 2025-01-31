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

            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

            if start_date > end_date:
                raise ValueError("Start date cannot be after the end date.")

            return stock_name, start_date, end_date

        except ValueError as e:
            print(f"Invalid input: {e}")
            return None, None, None

    @log_execution_time
    def fetch_data(self, stock_name, start_date = date(2019,1,1), end_date = date(2020, 1, 1)):
        try:
            df = stock_df(symbol=stock_name, from_date=start_date, to_date=end_date, series="EQ")
            if df.empty:
                print("No data found for this stock.")
                return None
            
            data = pd.DataFrame(df)
            data.to_csv(stock_name+'.csv', index=False)
            return df
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    @staticmethod
    def clean_data(df):
        if df.isnull().values.any():
            print("Missing values detected. Dropping null values...")
            df = df.dropna()

        if not pd.api.types.is_datetime64_any_dtype(df["DATE"]):
            df["DATE"] = pd.to_datetime(df["DATE"])

        return df

    @staticmethod
    def handle_weekend_or_holiday(date):
        if date.weekday() >= 5:
            raise ValueError(f"{date} falls on a weekend. Please enter a weekday.")
        return True

    @staticmethod  
    def calulate_daily_percentage_change(df):
        df['Daily_change_%'] = df['CLOSE'].pct_change() * 100
        return df

    @staticmethod  
    def calculate_volatility(df):
        volatility = df['Daily_Change_%'].std()
        return volatility

    @staticmethod   
    def group_and_average(df):
        return df.groupby('SYMBOL', as_index = False)['CLOSE'].mean().rename(columns={'CLOSE': 'Avg_Close'})

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

        self.stock_data = self.calculate_daily_percentage_change(self.stock_data)
        volatility = self.calculate_volatility(self.stock_data)

        print(f"\nStock Data Summary for {stock_name}:")
        print(self.stock_data.describe())

        print(f"\nVolatility for {stock_name}: {volatility:.2f}%")

        plt.figure(figsize=(10, 5))
        plt.plot(self.stock_data['DATE'], self.stock_data['CLOSE'], label=f'{stock_name} Closing Prices')
        plt.title(f'{stock_name} Closing Prices')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.legend()
        plt.show()


if __name__ == "__main__":
    app = StockMarketAnalysis()
    app.analyze_stock()
