import pandas as pd
from signals.indicators import *
from data_management.data_processing import *

class moving_averages():

    def __init__(self,data,close, m_ema,):
        self.data = data
        self.close = close
        self.m_ema = m_ema

    def ema(close,m_ema):
        ema=close.ewm(span=m_ema, adjust=False).mean()
        return ema

    def tema(close,m_ema):
        ema1=moving_averages.ema(close,m_ema)
        ema2=moving_averages.ema(ema1,m_ema)
        ema3=moving_averages.ema(ema2,m_ema)
        tema=(3*ema1)-(3*ema2)+ema3
        return tema
           
class relative_strength_index():

    def __init__(self,data,rsi_window):
        self.data = data
        self.rsi_window = rsi_window
     
    def rsi(data,rsi_window):
        pd.options.mode.chained_assignment = None  # default='warn'
        price=data['Close']
        data['Price Diff'] = price.diff(1)
        data = data[['Close','Price Diff']]
        data['gain'] = data['Price Diff'].clip(lower=0).round(2)
        data['loss'] = data['Price Diff'].clip(upper=0).abs().round(2)
        # Get initial Averages
        window_length=rsi_window
        data['avg_gain'] = data['gain'].rolling(window=window_length, min_periods=window_length).mean()[:window_length+1]
        data['avg_loss'] = data['loss'].rolling(window=window_length, min_periods=window_length).mean()[:window_length+1]
        # Get WMS averages
        # Average Gains
        for i, row in enumerate(data['avg_gain'].iloc[window_length+1:]):
            data['avg_gain'].iloc[i + window_length + 1] =\
                (data['avg_gain'].iloc[i + window_length] *
                (window_length - 1) +
                data['gain'].iloc[i + window_length + 1])\
                / window_length
        # Average Losses
        for i, row in enumerate(data['avg_loss'].iloc[window_length+1:]):
            data['avg_loss'].iloc[i + window_length + 1] =\
                (data['avg_loss'].iloc[i + window_length] *
                (window_length - 1) +
                data['loss'].iloc[i + window_length + 1])\
                / window_length
        rs = data['avg_gain'] / data['avg_loss']
        rsi = 100 - (100 / (1.0 + rs))
        return rsi


class momentum:
    def __init__(self,data,period):
        self.data = data
        self.period = period
    
    def calculate_momentum(data,period):
        momentum = data['Close'].diff(period)
        return momentum



class average_directional_index:
    def __init__(self,data,period):
        self.data = data
        self.period = period

    def calculate_adx(data,period):
        high=data['High']
        low=data['Low']
        close=data['Close']

        plus_dm = high.diff()
        minus_dm = low.diff()
        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm > 0] = 0

        tr1 = pd.DataFrame(high - low)
        tr2 = pd.DataFrame(abs(high - close.shift(1)))
        tr3 = pd.DataFrame(abs(low - close.shift(1)))
        frames = [tr1, tr2, tr3]
        tr = pd.concat(frames, axis = 1, join = 'inner').max(axis = 1)
        atr = tr.rolling(period).mean()   #using a simple MA for simple calculation of ATR

        plus_di = 100 * (plus_dm.ewm(alpha = 1/period).mean() / atr)
        minus_di = abs(100 * (minus_dm.ewm(alpha = 1/period).mean() / atr))

        dx = (abs(plus_di - minus_di) / abs(plus_di + minus_di)) * 100
        adx = ((dx.shift(1) * (period - 1)) + dx) / period
        adx_smooth = adx.ewm(alpha = 1/period).mean()

        return adx_smooth   #plus_di, minus_di



class delta_strength:
        
        def __init__(self,data):
            self.data = data
        
        def calculate_delta_strength(data,tema_short,tema_long,tema_trend):   
            delta_strength_1 = abs((tema_short - tema_long)*100)       #DS1: TEMA short - TEMA long         
            delta_strength_2 = abs((tema_long - tema_trend)*100)       #DS2: TEMA long - TEMA trend
            return delta_strength_1, delta_strength_2
        

            

        
        