from Packages.imports_buy import *

def calc_ema(df):
    ema_25 = 25
    df_ema_25 = df['Adj Close'].ewm(span=ema_25, adjust=False).mean()

    ema_100 = 100
    df_ema_100 = df['Adj Close'].ewm(span=ema_100, adjust=False).mean()

    return df_ema_25, df_ema_100

def calc_sma(df):
    sma_25 = 25
    df_sma_25 = df['Adj Close'].rolling(window=sma_25).mean()

    sma_100 = 100
    df_sma_100 = df['Adj Close'].rolling(window=sma_100).mean()

    return df_sma_25, df_sma_100

def calc_bollinger(df):
    bollinger_avg = 20

    short_avg_ma = df['Adj Close'].rolling(window=bollinger_avg).mean()
    short_avg_std = df['Adj Close'].rolling(window=bollinger_avg).std()

    bollinger = df['Adj Close'].ewm(span=bollinger_avg, adjust=False).mean()
    bollinger_lower_band = short_avg_ma - (short_avg_std *2)
    bollinger_upper_band = short_avg_ma + (short_avg_std *2)

    return bollinger, bollinger_lower_band, bollinger_upper_band

def calc_macd_signalline(df):
    ema_short = 12
    ema_long = 26
    signalline_span = 9

    df_ema_short = df['Adj Close'].ewm(span=ema_short, adjust=False).mean()
    df_ema_long = df['Adj Close'].ewm(span=ema_long, adjust=False).mean()
    macd = df_ema_short - df_ema_long
    signalline = macd.ewm(span=signalline_span, adjust=False).mean()

    return macd, signalline

def calc_rsi(df, n=14):
    delta = df['Adj Close'].diff()
    dUp, dDown = delta.copy(), delta.copy()
    dUp[dUp < 0] = 0
    dDown[dDown > 0] = 0

    # Calculate the EWMA
    RolUp = dUp.ewm(span=n).mean()
    RolDown = dDown.abs().ewm(span=n).mean()

    # Calculate the RSI based on EWMA
    RS = RolUp / RolDown
    RSI = 100 - (100/(1+RS))

    # Calculate the SMA
    roll_up2 = dUp.rolling(n).mean()
    roll_down2 = dDown.abs().rolling(n).mean()

    # Calculate the RSI based on SMA
    RS2 = roll_up2 / roll_down2
    RSI2 = 100.0 - (100.0 / (1.0 + RS2))

    own_RSI=(RSI+RSI2)/2
    return own_RSI

def calc_cci(df, n=14, constant=0.015):
    tippingPrice = (df['High'] + df['Low'] + df['Adj Close']) / 3
    tippingPrice_mean = tippingPrice.rolling(n).mean()
    tippingPrice_std = tippingPrice.rolling(n).std()
    
    CCI = pd.Series((tippingPrice - tippingPrice_mean) / (constant * tippingPrice_std)) 
    return CCI

### To Be Adjusted

def calc_obv(df, n = 20):
    i = 0
    OBV = [0]

    while i < df.index[-1]:
        if df.loc[i + 1, 'Adj Close'] - df.loc[i, 'Adj Close'] > 0:
            OBV.append(df.loc[i + 1, 'Volume'])
        if df.loc[i + 1, 'Adj Close'] - df.loc[i, 'Adj Close'] == 0:
            OBV.append(0)
        if df.loc[i + 1, 'Adj Close'] - df.loc[i, 'Adj Close'] < 0:
            OBV.append(-df.loc[i + 1, 'Volume'])
        i = i + 1
    OBV = pd.Series(OBV)
    OBV_ma = pd.Series(OBV.rolling(n, min_periods=n).mean())

    return OBV_ma

# To be adjusted ASAP
def calculate_dead_cat_bounce_v2(df):
  set_freq = '2D'

  df['body_mid'] = (df['Adj Close'] + df['Open'])/2

  pct_change_close = df['body_mid'].pct_change(freq=set_freq, fill_method='ffill')
  pct_change_close.dropna(inplace=True)

  dead_cat_bounce = np.where((df.signalline > df.macd) &
                            ((pct_change_close >= 0.05) | (pct_change_close <= -0.05)) &
                            ((df.Open < df.bollinger_lower_band)|(df.Close < df.bollinger_lower_band)),
                            True, False)

  df['dead_cat_bounce'] = dead_cat_bounce
  del df['body_mid']

  return df
