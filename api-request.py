from datetime import date
from jugaad_data.nse import bhavcopy_save, bhavcopy_fo_save, stock_df

# Download bhavcopy
# bhavcopy_save(date(2023,1,7), "./")

df = stock_df(symbol="SBIN", from_date=date(2019,1,1),
            to_date=date(2020,1,30), series="EQ")

print(df)