import pandas as pd

class moving_averages_conditionals():
    def __init__(self,delta):
        self.delta = delta 
    
    def temas_principal_trend_condition(close,trend): 
        if close >= trend:
            return 'Bull'
        elif close < trend:
            return 'Bear'
        else:
            return 'Vacio'

    def temas_second_trend_condition(delta):   
        if delta >= 0:
            return  'Bull'
        elif delta < 0:
            return  'Bear'
        else:
            return 'Vacio'

class rsi_conditionals():
    
    def __init__(self,rsi):
        self.rsi = rsi

    def rsi_condition(rsi,rsi_umbral):
        #rsi_umbral = 50
        if rsi >= rsi_umbral:
            return 'Bull'
        elif rsi < rsi_umbral:
            return 'Bear'
        else:
            return 'Vacio'

#The next class transforms the entry signal data from Bull or Bear to True or False

class three_temas_plus_rsi_conditionals:
    def __init__(self,entry_signal):
        self.entry_signal = entry_signal
    
    def boolean_long_operation(entry_signal):
        #boolean_conditions = three_temas_plus_rsi_conditionals.boolean_transform_long_conditions(entry_signal)
        condition_long_1 = entry_signal['Condition 1'].apply(lambda x: True if (x=='Bull') else False).iat[0]
        condition_long_2 = entry_signal['Condition 2'].apply(lambda x: True if (x=='Bull') else False).iat[0]
        condition_long_3 = entry_signal['Condition 3'].apply(lambda x: True if (x=='Bull') else False).iat[0]
        return condition_long_1,condition_long_2,condition_long_3


    def boolean_short_operation(entry_signal):
        #boolean_conditions = three_temas_plus_rsi_conditionals.boolean_transform_long_conditions(entry_signal)
        condition_short_1 = entry_signal['Condition 1'].apply(lambda x: True if (x=='Bear') else False).iat[0]
        condition_short_2 = entry_signal['Condition 2'].apply(lambda x: True if (x=='Bear') else False).iat[0]
        condition_short_3 = entry_signal['Condition 3'].apply(lambda x: True if (x=='Bear') else False).iat[0]
        return condition_short_1,condition_short_2,condition_short_3



