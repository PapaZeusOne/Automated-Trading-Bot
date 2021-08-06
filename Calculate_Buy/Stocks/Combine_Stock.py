from Packages.imports_buy import *
from Indicators.Combine_Indicators import *

def combine_stocks_today(id_list):

  ts = TimeSeries(key='AXUYKPP8SFQ1MAB7', output_format='pandas')  
  start_date = '2020-7-28'
  df_list = []

  for id in id_list:
    data, meta_data = ts.get_daily_adjusted(symbol=id, outputsize='full') # Change outputsize to 'compact' and only receive data from the last 100 days
    data = data.sort_index(ascending=True)
    data['stock_id'] = id
    
    del data['6. volume']
    del data['7. dividend amount']
    del data['8. split coefficient']

    # Resize df and rename columns appropriately
    stock = data[start_date:].copy()
    stock.columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'stock_id']

    # calc indicators for every stock
    stock = calc_indicators(stock)
    stock['pct_change'] = stock['Adj Close'].pct_change(periods=14, fill_method='ffill')
 

    # drop unnecessary rows with NaN values
    stock.dropna(inplace=True) 
    df_list.append(stock)

  df_complete = pd.concat(df_list)
  
  return df_complete

def combine_stocks_14d_ago(id_list):

  ts = TimeSeries(key='AXUYKPP8SFQ1MAB7', output_format='pandas')  
  start_date = '2020-7-28'
  df_list = []

  for id in id_list:
    data, meta_data = ts.get_daily_adjusted(symbol=id, outputsize='full') # Change outputsize to 'compact' and only receive data from the last 100 days
    data = data.sort_index(ascending=True)
    data['stock_id'] = id
    
    del data['6. volume']
    del data['7. dividend amount']
    del data['8. split coefficient']

    # Resize df and rename columns appropriately
    date_15d_ago = date.today() + timedelta(days=-15)
    stock = data[start_date:date_15d_ago].copy()
    stock.columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'stock_id']

    # calc indicators for every stock
    stock = calc_indicators(stock) 

    period = 14
    stock['pct_change'] = stock['Adj Close'].pct_change(periods=period, fill_method='ffill')
    #stock = stock.iloc[::period, :]

    # drop unnecessary rows with NaN values
    stock.dropna(inplace=True) 
    df_list.append(stock)

  df_complete = pd.concat(df_list)
  
  return df_complete