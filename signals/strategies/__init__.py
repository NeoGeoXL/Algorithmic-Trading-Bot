from signals.indicators import *
from signals.conditionals import *
from data_management.data_processing import moving_averages_processing
import pandas as pd



class three_temas_plus_rsi:
    def __init__(self,data,entry_signal):
        self.data = data
        self.entry_signal = entry_signal
    
    def trading_signal(data,tema_short_period,tema_long_period,tema_trend_period,rsi_period,rsi_umbral,adx_period,adx_umbral):

        #Calculate the 3 temas 
        tema_short=moving_averages.tema(data['Close'],tema_short_period)   
        tema_long=moving_averages.tema(data['Close'],tema_long_period)   
        tema_trend=moving_averages.tema(data['Close'],tema_trend_period) 


        conditions_df=pd.DataFrame(data['Close'])

        # 1 Condition: Pricipal Trend, price above or below the trend
        data['Trend'] = tema_trend
        first_condition = data[['Close','Trend']].apply(lambda x: moving_averages_conditionals.temas_principal_trend_condition(*x), axis=1)
        conditions_df['Condition 1'] = first_condition

        # 2 Condition: Tema short is above tema long or tema long is above tema trend
        delta_temas = moving_averages_processing.delta_temas(tema_short,tema_long)
        data['Delta_temas']=delta_temas
        second_condition = data['Delta_temas'].apply(moving_averages_conditionals.temas_second_trend_condition)
        conditions_df['Condition 2'] = second_condition

        # 3 Condition: RSI is above 50 or below 50
        
        data['RSI'] = relative_strength_index.rsi(data,rsi_period)
        rsi = data['RSI'].iloc[-1]
        third_condition = data['RSI'].apply(rsi_conditionals.rsi_condition,args=(rsi_umbral,))
        conditions_df['Condition 3'] = third_condition

        # Get only the last value from the conditions dataframe
        entry_signal = conditions_df.iloc[-1:,:]
        
        # Get the trend measure parameters

        # Get adx value
        adx = average_directional_index.calculate_adx(data,adx_period)
        data['Adx'] = adx
        adx_value = data['Adx'].iloc[-1]

        # Get delta strength values
        delta_strength_1, delta_strength_2 = delta_strength.calculate_delta_strength(data,tema_short,tema_long,tema_trend)
        ds1_value = delta_strength_1.iloc[-1]
        ds2_value = delta_strength_2.iloc[-1]
        indicators_values = pd.DataFrame({'RSI':rsi,'ADX':adx_value,'DS1':ds1_value,'DS2':ds2_value},index=[0])

        return entry_signal,indicators_values


