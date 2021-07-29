from Packages.imports_buy import *

def ema_score(row):
    ema_25 = row['ema_25']
    ema_100 = row['ema_100']
    score = (ema_25/ema_100)-1
    return score

def sma_score(row):
    sma_25 = row['sma_25']
    adj_close = row['Adj Close']
    score = (adj_close/sma_25)-1
    return score

def macd_signalline_score(row): 
    # relative change might be distorted if values near by 0
    macd = row['macd']
    signalline = row['signalline']
    adj_close = row['Adj Close']
    score = (macd/adj_close+1)-(signalline/adj_close+1)
    return score

# set weighting when close is lower lower_band or upper upper_band
def bollinger_score(row):
    lower_band = row['bollinger_lower_band']
    upper_band = row['bollinger_upper_band']
    middle_band = row['bollinger']
    adj_close = row['Adj Close']
    if (adj_close>=middle_band):
        if adj_close>=upper_band:
            score = ((adj_close/upper_band)-1)*(-1)
        else:
            score = ((adj_close/((upper_band-middle_band)*0.5+middle_band))-1)*(-1)
    else:
        if (adj_close<=lower_band):
            score = ((adj_close/lower_band)-1)*(-1)
        else:
            score = (adj_close/middle_band)-1
    return score

def rsi_score(row):
    lower_band = 30
    upper_band = 70
    middle_band = (lower_band + upper_band) / 2 
    middle_band1 = 55
    middle_band2 = 45
    outlier_factor = 1.2
    rsi = row['RSI']
    if (rsi>middle_band):
        if rsi>=upper_band:
            score = ((rsi/upper_band)-1)*(-1)*(outlier_factor)
        else:
            if rsi<middle_band1:
                score = 0
            else:
                if rsi<=62.5:
                    score = rsi/middle_band1-1
                else:
                    score = ((62.5-(rsi-62.5))/(middle_band1))-1
    else:
        if (rsi<=lower_band):
            score = ((rsi/lower_band)-1)*(-1)*(outlier_factor)
        else:
            if rsi>middle_band2:
                score = 0
            else:
                if rsi>=37.5:
                    score = (rsi/middle_band2-1)
                else:
                    score = (37.5-(rsi-37.5))/middle_band2-1
    return score

# We should check whether we give the same weighting if it hits above or lower 100/-100
def cci_score(row):
    lower_band = -100
    middle_lower_band = -50
    upper_band = 105
    middle_band = 0
    middle_upper_band = 85
    outlier_factor = 0.25
    outlier_factor1 = 2
    cci=row['RSI']

    if (cci < lower_band):
        score=(cci/lower_band)-1
    else:
        if (cci<=middle_lower_band):
            score = (cci / lower_band)-1
        elif (cci<middle_band):
            score = (((cci-lower_band)/lower_band)+1)*(-1)
        else:
            if (cci>upper_band):
                score = ((cci/upper_band)-1)*(-1)
            else:
                if(cci<=middle_upper_band):
                    score = (cci/upper_band)*outlier_factor
                else:
                    if(cci<upper_band):
                        score=(middle_upper_band-(cci-middle_upper_band))/upper_band-(middle_upper_band-(middle_upper_band-upper_band))/middle_upper_band
                    else:
                        score=0
    
    return score

## TO BE ADDED: DEAD-CAT-BOUNCE SCORE CALC  