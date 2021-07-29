from Packages.imports_buy import *
from Indicators.Calculate_Indicators import *

def calc_indicators(df):
  df['ema_25'], df['ema_100'] = calc_ema(df)
  
  df['sma_25'], df['sma_100'] = calc_sma(df)

  df['bollinger'], df['bollinger_lower_band'], df['bollinger_upper_band'] = calc_bollinger(df)

  df['macd'], df['signalline'] = calc_macd_signalline(df)

  df['RSI'] = calc_rsi(df)

  df['CCI'] = calc_cci(df)

  # df['OBV_MA'] = calc_obv(df)
   
  df = calculate_dead_cat_bounce_v2(df)

  return df