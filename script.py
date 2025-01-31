from backend_script import stock_market_analysis


my_app = stock_market_analysis()

print(my_app.get_data('SBIN').columns)

data = my_app.get_data('SBIN')

# data = data.cel