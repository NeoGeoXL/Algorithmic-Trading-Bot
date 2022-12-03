from data_management.get_data import *
from signals.strategies import *
from data_management.data_processing import prices_processing,stocks_quantity
from utilities.chatbot import telegram_notifications
from utilities.brokers.interactive_brokers import *
from ib_insync import *
from utilities.brokers.etoro import etoro_data_processing
from signals.conditionals import *
import pandas as pd

ip = '127.0.0.1'
port = 7497
client_id = 1


class normal_bot:
    def __init__(self,temporality,ticker,loss,profit,capital):
        self.temporality = temporality
        self.ticker = ticker
        self.loss = loss
        self.profit = profit
        self.capital = capital


    def activate_bot(list_of_tickers,temporality,loss,profit,capital,tema_short_period,tema_long_period,tema_trend_period,rsi_period,rsi_umbral,adx_period,adx_umbral):

        print('*'*50)
        ib_connection.connect(ip,port,client_id)  
        for ticker in list_of_tickers:
            try: 
                data = ticker_data.get_ticker_data(temporality,ticker) 
                entry_signal, indicators_values= three_temas_plus_rsi.trading_signal(data,tema_short_period,tema_long_period,tema_trend_period,rsi_period,rsi_umbral,adx_period,adx_umbral)
                print(entry_signal)
                condition_long_1,condition_long_2,condition_long_3 = three_temas_plus_rsi_conditionals.boolean_long_operation(entry_signal)   
                condition_short_1,condition_short_2,condition_short_3 = three_temas_plus_rsi_conditionals.boolean_short_operation(entry_signal)
                if condition_long_1==True & condition_long_2 == True & condition_long_3 == True:
                    print(condition_long_1,condition_long_2,condition_long_3)
                    market_price = prices_processing.market_price(entry_signal)
                    stop_loss_long = prices_processing.stop_loss_long(market_price,loss)
                    take_profit_long = prices_processing.take_profit_long(market_price,profit)
                    action = 'BUY'
                    quantity =1  #stocks_quantity.quantity(capital,market_price)
                    telegram_notifications.send_message(ticker,action,market_price,stop_loss_long,take_profit_long)
                    contract=place_order_by_strategy.define_contract(ticker)
                    order = place_order_by_strategy.define_order(action,quantity,market_price,take_profit_long,stop_loss_long)
                    place_order_by_strategy.place_order(contract,order,ticker)
                    print('*'*50)
                elif condition_short_1 == True & condition_short_2 == True & condition_short_3 == True:
                    print(condition_short_1,condition_short_2,condition_short_3)
                    market_price = prices_processing.market_price(entry_signal)
                    stop_loss_short = prices_processing.stop_loss_short(market_price,loss)
                    take_profit_short = prices_processing.take_profit_short(market_price,profit)
                    action = 'SELL'
                    quantity =1  #stocks_quantity.quantity(capital,market_price)
                    print('*'*50)
                    telegram_notifications.send_message(ticker,action,market_price,stop_loss_short,take_profit_short)
                    contract=place_order_by_strategy.define_contract(ticker)
            except:
                print('Error processing data for ticker: ',ticker)

class massive_analysis_bot:
    def __init__(self,temporality,list_of_tickers,loss,profit,capital):
        self.temporality = temporality
        self.list_of_tickers = list_of_tickers
        self.loss = loss
        self.profit = profit
        self.capital = capital
    
    def activate_massive_bot(temporality,tickers_df,sector_change,sector_change_percent,loss,profit,tema_short_period,tema_long_period,tema_trend_period,rsi_period,rsi_umbral,adx_umbral,adx_period):
        massive_analysis_df = pd.DataFrame(columns=['Ticker','Action','Market Price','Stop Loss','Take Profit','RSI','ADX','DS1','DS2','Sector','Industry','Sector Change $','Sector Change %'])
        list_of_tickers = tickers_df['Symbol'].tolist()
        print('Total stocks to analyze'+ ' ' + str(len(list_of_tickers)))
        for ticker in list_of_tickers:
            try:
                data = ticker_data.get_ticker_data(temporality,ticker)
                entry_signal, indicators_values= three_temas_plus_rsi.trading_signal(data,tema_short_period,tema_long_period,tema_trend_period,rsi_period,rsi_umbral,adx_umbral,adx_period)
                print(ticker)
                condition_long_1,condition_long_2,condition_long_3 = three_temas_plus_rsi_conditionals.boolean_long_operation(entry_signal)   
                condition_short_1,condition_short_2,condition_short_3 = three_temas_plus_rsi_conditionals.boolean_short_operation(entry_signal)
                if condition_long_1==True & condition_long_2 == True & condition_long_3 == True:
                    market_price = prices_processing.market_price(entry_signal)
                    stop_loss_long = prices_processing.stop_loss_long(market_price,loss)
                    take_profit_long = prices_processing.take_profit_long(market_price,profit)
                    action = 'BUY'
                    rsi = round(indicators_values['RSI'].iat[0])
                    adx = round(indicators_values['ADX'].iat[0])
                    ds1 = round(indicators_values['DS1'].iat[0])
                    ds2 = round(indicators_values['DS2'].iat[0])
                    sector_ticker = tickers_df.loc[tickers_df['Symbol'] == ticker, 'Sector'].iloc[0]
                    industry_ticker = tickers_df.loc[tickers_df['Symbol'] == ticker, 'Industry'].iloc[0]
                    if adx >= adx_umbral:
                        new_row = pd.DataFrame({'Ticker':ticker,'Action':action,'Market Price':market_price,'Stop Loss':stop_loss_long,'Take Profit':take_profit_long,'RSI':rsi,'ADX':adx,'DS1':ds1,'DS2':ds2,'Sector':sector_ticker,'Industry':industry_ticker,'Sector Change $':sector_change,'Sector Change %':sector_change_percent},index=[0])
                        massive_analysis_df = pd.concat([new_row,massive_analysis_df[:]],ignore_index=True).reset_index(drop=True)
                elif condition_short_1 == True & condition_short_2 == True & condition_short_3 == True:
                    market_price = prices_processing.market_price(entry_signal)
                    stop_loss_short = prices_processing.stop_loss_short(market_price,loss)
                    take_profit_short = prices_processing.take_profit_short(market_price,profit)
                    action = 'SELL'
                    rsi = round(indicators_values['RSI'].iat[0])
                    adx = round(indicators_values['ADX'].iat[0])
                    ds1 = round(indicators_values['DS1'].iat[0])
                    ds2 = round(indicators_values['DS2'].iat[0])
                    sector_ticker = tickers_df.loc[tickers_df['Symbol'] == ticker, 'Sector'].iloc[0]
                    industry_ticker = tickers_df.loc[tickers_df['Symbol'] == ticker, 'Industry'].iloc[0]
                    if adx >= adx_umbral:
                        new_row = pd.DataFrame({'Ticker':ticker,'Action':action,'Market Price':market_price,'Stop Loss':stop_loss_short,'Take Profit':take_profit_short,'RSI':rsi,'ADX':adx,'DS1':ds1,'DS2':ds2,'Sector':sector_ticker,'Industry':industry_ticker,'Sector Change $':sector_change,'Sector Change %':sector_change_percent},index=[0])
                        massive_analysis_df = pd.concat([new_row,massive_analysis_df[:]],ignore_index=True).reset_index(drop=True)
                else:
                    print('No trading signal')
                #Sorting by tema short and tema long distance
                massive_analysis_df_sorted = massive_analysis_df.sort_values(by=['DS1'],ascending=False).reset_index(drop=True)
            except:
                print('Error processing ticker')
                print('*'*50)                
        return massive_analysis_df_sorted

    def append_new_stocks_to_sheets(index,massive_analysis_df_sorted,strategy,pl_ratio,month,week,temporality):
        new_df= massive_analysis_df_sorted.head(index)
        sa=etoro_data_processing.connect_to_google_sheet()
        wks = etoro_data_processing.open_worksheet(sa,month,week)
        for i in range(len(new_df)):
            ticker = new_df['Ticker'].iloc[i]
            action = new_df['Action'].iloc[i]
            market_price = new_df['Market Price'].iloc[i]
            stop_loss = new_df['Stop Loss'].iloc[i]
            take_profit = new_df['Take Profit'].iloc[i]
            data = etoro_data_processing.create_operation_data_list(ticker,action,market_price,stop_loss,take_profit,pl_ratio,strategy,temporality)
            etoro_data_processing.append_operation_data(wks,data)
    
class massive_analysis_bot_tws:
    def __init__(self,index,massive_analysis_df_sorted):
        self.index = index
        self.massive_analysis_df_sorted = massive_analysis_df_sorted

    def activate_massive_bot_tws(index,massive_analysis_df_sorted):
        new_df= massive_analysis_df_sorted.head(index)
        ib_connection.connect(ip,port,client_id) 
        for i in range(len(new_df)):
            ticker = new_df['Ticker'].iloc[i]
            action = new_df['Action'].iloc[i]
            market_price = new_df['Market Price'].iloc[i]
            stop_loss = new_df['Stop Loss'].iloc[i]
            take_profit = new_df['Take Profit'].iloc[i]
            quantity = 1 
            try: 
                contract=place_order_by_strategy.define_contract(ticker)
                order = place_order_by_strategy.define_order(action,quantity,market_price,take_profit,stop_loss)
                place_order_by_strategy.place_order(contract,order,ticker)
            except:
                print('Error placing order')
                print('*'*50)
        ib_connection.disconnect()
        
class sector_analysis_bot:
    def __init__(self,sector,sector_temporality):
        self.sector = sector
        self.sector_temporality = sector_temporality
        
    def activate_sector_analysis_bot(sector_temporality,stock_temporality,loss,profit,tema_short_period,tema_long_period,tema_trend_period,rsi_period,rsi_umbral,adx_umbral,adx_period):
        
        sectors_index_data=index_sectors_data.index_sector_information(sector_temporality)  #best_sector_to_invest
        print(sectors_index_data)
        sector_name,sector_symbol,sector_change,sector_change_percent = index_sectors_data.sector_name_ticker(sectors_index_data)
        print(sector_name)
        data = ticker_data.get_ticker_data(sector_temporality,sector_symbol)
        entry_signal, indicators_values= three_temas_plus_rsi.trading_signal(data,tema_short_period,tema_long_period,tema_trend_period,rsi_period,rsi_umbral,adx_umbral,adx_period)
        #print(entry_signal)
        condition_long_1,condition_long_2,condition_long_3 = three_temas_plus_rsi_conditionals.boolean_long_operation(entry_signal)   
        condition_short_1,condition_short_2,condition_short_3 = three_temas_plus_rsi_conditionals.boolean_short_operation(entry_signal) 
        #massive_analysis_df_sorted = pd.DataFrame()
        if condition_long_1 == True & condition_long_2 == True & condition_long_3 == True:
            #sector_list=sectors_data_processing.filter_by_sector_list(sector_name)
            #print(sector_list)
            sector_df=sectors_data_processing.filter_sector_df(sector_name)
            try:
                massive_analysis_df_sorted=massive_analysis_bot.activate_massive_bot(stock_temporality,sector_df,sector_change,sector_change_percent,loss,profit,tema_short_period,tema_long_period,tema_trend_period,rsi_period,rsi_umbral,adx_umbral,adx_period)
                #massive_analysis_df_sorted_buy = massive_analysis_df_sorted[massive_analysis_df_sorted['Action']=='BUY'
                return massive_analysis_df_sorted 
            except:
                print('Error processing sector and order')
                print('*'*50)         
        elif condition_short_1 == True & condition_short_2 == True & condition_short_3 == True:
            #sector_list=sectors_data_processing.filter_by_sector_list(sector_name)
            #print(sector_list)
            sector_df=sectors_data_processing.filter_sector_df(sector_name)
            try:
                massive_analysis_df_sorted=massive_analysis_bot.activate_massive_bot(stock_temporality,sector_df,sector_change,sector_change_percent,loss,profit,tema_short_period,tema_long_period,tema_trend_period,rsi_period,rsi_umbral,adx_umbral,adx_period)
                #massive_analysis_df_sorted_buy = massive_analysis_df_sorted[massive_analysis_df_sorted['Action']=='BUY'
                return massive_analysis_df_sorted 
            except:
                print('Error processing sector and order')
                print('*'*50)         
        else:
            print('No trading signal')
            return 2
    def append_new_stocks_to_sheets(index,sector_massive_analysis_df,strategy,pl_ratio,database_name,month,temporality,tema_short_period,tema_long_period,tema_trend_period,rsi_period,rsi_umbral,adx_period,adx_umbral,sector_temporality):
        new_df= sector_massive_analysis_df.head(index)
        sa=etoro_data_processing.connect_to_google_sheet()
        wks = etoro_data_processing.open_worksheet(sa,database_name,month)
        for i in range(len(new_df)):
            ticker = new_df['Ticker'].iloc[i]
            action = new_df['Action'].iloc[i]
            market_price = new_df['Market Price'].iloc[i]
            stop_loss = new_df['Stop Loss'].iloc[i]
            take_profit = new_df['Take Profit'].iloc[i]
            rsi = new_df['RSI'].iloc[i]
            adx = new_df['ADX'].iloc[i]
            ds1  = new_df['DS1'].iloc[i]
            ds2  = new_df['DS2'].iloc[i]
            sector = new_df['Sector'].iloc[i]
            industry = new_df['Industry'].iloc[i]
            sector_change = new_df['Sector Change $'].iloc[i]
            sector_change_percent = new_df['Sector Change %'].iloc[i]


            data = etoro_data_processing.create_massive_sector_operation_data_list(ticker,action,market_price,stop_loss,take_profit,pl_ratio,strategy,temporality,tema_short_period,tema_long_period,tema_trend_period,rsi_period,rsi_umbral,adx_period,adx_umbral,sector_temporality,rsi,adx,ds1,ds2,sector,industry,sector_change,sector_change_percent)
            etoro_data_processing.append_operation_data(wks,data)

