from Packages.imports_buy import *
from Calculate_Score import *

def relative_score(row):
    r = row
    stock = row['stock_id']

    ema_scr = ema_score(r)
    macd_signalline_scr = macd_signalline_score(r)
    bollinger_scr = bollinger_score(r)
    sma_scr = sma_score(r)
    rsi_scr = rsi_score(r)
    cci_scr = cci_score(r)

    score = ema_scr + (macd_signalline_scr*5) + bollinger_scr + sma_scr + rsi_scr + cci_scr
    print(stock, ema_scr, (macd_signalline_scr*5), bollinger_scr, sma_scr, rsi_scr, cci_scr, score, '\n')
    return score