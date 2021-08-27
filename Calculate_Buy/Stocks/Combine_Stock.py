from Packages.imports_buy import *
from Indicators.Combine_Indicators import *

def combine_stocks_today(id_list, start, calc):

  ts = TimeSeries(key='AXUYKPP8SFQ1MAB7', output_format='pandas')  
  start_date = start
  df_list = []

  for id in id_list:
    data, meta_data = ts.get_daily_adjusted(symbol=id, outputsize='full') # Change outputsize to 'compact' and only receive data from the last 100 days
    data = data.sort_index(ascending=True)
    data['stock_id'] = id

    delete_values = ['6. volume', '7. dividend amount', '8. split coefficient']
    for column in delete_values:
        del data[column]

    # Resize df and rename columns appropriately
    stock = data[start_date:].copy()
    stock.columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'stock_id']

    # calc indicators for every stock if parameter is set to true
    if calc:
      stock = calc_indicators(stock) 

    # drop unnecessary rows with NaN values
    stock.dropna(inplace=True) 
    df_list.append(stock)

  df_complete = pd.concat(df_list)
  
  return df_complete

def combine_stocks_Xdays_ago(id_list, start, period, calc):

  ts = TimeSeries(key='AXUYKPP8SFQ1MAB7', output_format='pandas')  
  start_date = start
  df_list = []

  for id in id_list:
    data, meta_data = ts.get_daily_adjusted(symbol=id, outputsize='full') # Change outputsize to 'compact' and only receive data from the last 100 days
    data = data.sort_index(ascending=True)
    data['stock_id'] = id
    
    delete_values = ['6. volume', '7. dividend amount', '8. split coefficient']
    for column in delete_values:
        del data[column]

    # Resize df and rename columns appropriately
    date_Xdays_ago = date.today() + timedelta(days=-period)
    stock = data[start_date:date_Xdays_ago].copy()
    stock.columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'stock_id']

    # calc indicators for every stock
    if calc:
      stock = calc_indicators(stock) 

    # drop unnecessary rows with NaN values
    stock.dropna(inplace=True) 
    df_list.append(stock)

  df_complete = pd.concat(df_list)
  
  return df_complete