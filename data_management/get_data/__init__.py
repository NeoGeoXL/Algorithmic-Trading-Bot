from pandas_datareader import data as pdr
import yfinance as yf
from datetime import datetime, timedelta
import pathlib
import pandas as pd
import random

class ticker_data:

    def __init__(self, temporality, ticker):
        self.temporality = temporality
        self.ticker = ticker

    def get_ticker_data(temporality,ticker):

        yf.pdr_override()
        actual_date = datetime.now()
        five_days_date = actual_date - timedelta(days=5) 
        ten_days_date = actual_date - timedelta(days=10)
        twenty_days_date = actual_date - timedelta(days=20)
        

        
        if temporality == '1m':
            try:
                data = pdr.get_data_yahoo(ticker, start = five_days_date, end=datetime.now(), interval="1m")
                return data
            except:
                print('Error getting data from Yahoo Finance')
                return None
        elif temporality == '5m':
            try:
                data = pdr.get_data_yahoo(ticker, start = five_days_date, end=datetime.now(), interval="5m")
                return data
            except:
                print('Error getting data from Yahoo Finance')
                return None
        elif temporality == '15m':
            try:
                data = pdr.get_data_yahoo(ticker, start = five_days_date, end=datetime.now(), interval="15m")
                return data
            except:
                print('Error getting data from Yahoo Finance')
                return None

        elif temporality == '30m':
            try:
                data = pdr.get_data_yahoo(ticker, start = ten_days_date, end=datetime.now(), interval="30m")
                return data
            except:
                print('Error getting data from Yahoo Finance')
                return None

        elif temporality == '1h':
            try:
                data = pdr.get_data_yahoo(ticker, start = twenty_days_date, end=datetime.now(), interval="1h")
                return data
            except:
                print('Error getting data from Yahoo Finance')
                return None
        elif temporality == '1d':
            try:
                data = pdr.get_data_yahoo(ticker, start = twenty_days_date, end=datetime.now(), interval="1d")
                return data
            except:
                print('Error getting data from Yahoo Finance')
                return None
        else:
            warning = '\n' +'*'*30 +' '+ 'No stock information'+' '+ '*'*30 + '\n' 
            return warning 
        

class sectors_data_processing:
    def __init__(self,sector):
        self.sector = sector
    
    def get_sector_data():
        CURRENT_DIR = pathlib.Path.cwd()
        INPUT_DATA_DIR = CURRENT_DIR.joinpath('./','data_management','data','input_data')
        INPUT_DATA_DIR = str(INPUT_DATA_DIR)       
        markets_sectors_df = pd.read_csv(INPUT_DATA_DIR + '\market_sectors_data.csv')
        Bigger_than_cero_markets_df = markets_sectors_df[markets_sectors_df['Market Cap'] > 0.00]
        us_markets_df = Bigger_than_cero_markets_df[Bigger_than_cero_markets_df['Country'] == 'United States']
        us_market_sectors_df = us_markets_df[['Symbol', 'Name','% Change', 'Market Cap', 'Volume', 'Sector', 'Industry']]
        return us_market_sectors_df
    
    def filter_by_sector_list(sector):
        us_market_sectors_df = sectors_data_processing.get_sector_data()
        sector_df = us_market_sectors_df[us_market_sectors_df['Sector'] == sector]
        sectors_list = sector_df['Symbol'].tolist()
        return sectors_list

    def filter_by_sector_and_percentile(sector,percentile):
        us_market_sectors_df = sectors_data_processing.get_sector_data()
        sector_df = us_market_sectors_df[us_market_sectors_df['Sector'] == sector]
        sector_df = sector_df[sector_df['Market Cap'] > sector_df['Market Cap'].quantile(percentile)]
        sector_df = sector_df[sector_df['Volume'] > sector_df['Volume'].quantile(percentile)]
        return sector_df

    def filter_sector_df(sector):
        us_market_sectors_df = sectors_data_processing.get_sector_data()
        sector_df = us_market_sectors_df[us_market_sectors_df['Sector'] == sector]
        return sector_df
    
    def all_sectors_data_list(percentile):
        
        industrials_sector_df = sectors_data_processing.filter_by_sector_and_percentile('Industrials',percentile)
        industrial_list = industrials_sector_df['Symbol'].tolist()
        healthcare_sector_df = sectors_data_processing.filter_by_sector_and_percentile('Health Care',percentile)
        healthcare_list = healthcare_sector_df['Symbol'].tolist()
        real_state_sector = sectors_data_processing.filter_by_sector_and_percentile('Real Estate',percentile)
        real_state_list = real_state_sector['Symbol'].tolist()
        consumer_discretionary_sector = sectors_data_processing.filter_by_sector_and_percentile('Consumer Discretionary',percentile)
        consumer_discretionary_list = consumer_discretionary_sector['Symbol'].tolist()
        finance_sector = sectors_data_processing.filter_by_sector_and_percentile('Finance',percentile)
        finance_list = finance_sector['Symbol'].tolist()
        techology_sector = sectors_data_processing.filter_by_sector_and_percentile('Technology',percentile)
        techology_list = techology_sector['Symbol'].tolist()
        consumer_staples_sector = sectors_data_processing.filter_by_sector_and_percentile('Consumer Staples',percentile)
        consumer_staples_list = consumer_staples_sector['Symbol'].tolist()
        miscellaneous_sector =sectors_data_processing. filter_by_sector_and_percentile('Miscellaneous',percentile)
        miscellaneous_list = miscellaneous_sector['Symbol'].tolist()
        utilities_sector = sectors_data_processing.filter_by_sector_and_percentile('Utilities',percentile)
        utilities_list = utilities_sector['Symbol'].tolist()
        telecommunications_sector = sectors_data_processing.filter_by_sector_and_percentile('Telecommunications Services',percentile)
        telecommunications_list = telecommunications_sector['Symbol'].tolist()
        energy_sector = sectors_data_processing.filter_by_sector_and_percentile('Energy',percentile)
        energy_list = energy_sector['Symbol'].tolist()
        basic_materials_sector =sectors_data_processing.filter_by_sector_and_percentile('Basic Materials',percentile)
        basic_materials_list = basic_materials_sector['Symbol'].tolist()
      
        all_sectors_list = []
        all_sectors_list = industrial_list + healthcare_list + real_state_list + consumer_discretionary_list + finance_list + techology_list + consumer_staples_list + miscellaneous_list + utilities_list + telecommunications_list + energy_list + basic_materials_list
        all_sectors_list = random.sample(all_sectors_list,len(all_sectors_list))   
        return all_sectors_list
        


class sp500_data_processing:
    def __init__(self,sector):
        self.sector = sector
    
    def get_sp500_data():
        CURRENT_DIR = pathlib.Path.cwd()
        INPUT_DATA_DIR = CURRENT_DIR.joinpath('./','data','input_data')
        INPUT_DATA_DIR = str(INPUT_DATA_DIR)       
        sp500_stocks_df = pd.read_csv(INPUT_DATA_DIR + '\SP500.csv')
        #sp500_tickers_list = sp500_stocks_df['Symbol'].tolist()
        #sp500_tickers_string_list = [str(i) for i in sp500_tickers_list]
        return sp500_stocks_df

    def filter_sp500_data_by_sector(sector):
        sp500_stocks_df = sp500_data_processing.get_sp500_data()
        sp500_sector_new_df = sp500_stocks_df[sp500_stocks_df['Sector'].str.contains(sector)]
        print(sp500_sector_new_df)
        sp500_sector_tickers_list = sp500_sector_new_df['Symbol'].tolist()
        print(sp500_sector_tickers_list)
        return sp500_sector_tickers_list






class index_sectors_data:
    def __init__(self,sector,temporality):
        self.sector = sector
        self.temporality = temporality

    def get_index_sector_change(temporality,sector):
        sector_data = ticker_data.get_ticker_data(temporality,sector)
        sector_data['Change'] = sector_data['Close'].diff()
        sector_data['Change %'] = sector_data['Close'].div(sector_data['Close'].shift(1)).sub(1).mul(100)
        sector_change = sector_data['Change'].iloc[-1]
        sector_change = round(sector_change,2)
        sector_change_percent = sector_data['Change %'].iloc[-1]
        sector_change_percent = round(sector_change_percent,2)
        
        return sector_change,sector_change_percent
    
    def index_sector_information(temporality):
            ''' 
                Energy: ^GSPE
                Materials: ^SP500-15
                Industrials: ^SP500-20
                Consumer Discretionary: ^SP500-25
                Consumer Staples: ^SP500-30
                Health Care: ^SP500-35
                Financials: ^SP500-40
                Information Technology: ^SP500-45
                Telecommunication Services: ^SP500-50
                Utilities: ^SP500-55
                Real Estate: ^SP500-60
            '''
            
            #sector_index_list = ['^GSPE','^SP500-15','^SP500-20','^SP500-25','^SP500-30','^SP500-35','^SP500-40','^SP500-45','^SP500-50','^SP500-55','^SP500-60']
            sector_index_dict = {'Energy':'^GSPE','Materials':'^SP500-15','Industrials':'^SP500-20','Consumer Discretionary':'^SP500-25','Consumer Staples':'^SP500-30','Health Care':'^SP500-35','Financials':'^SP500-40','Information Technology':'^SP500-45','Telecommunication Services':'^SP500-50','Utilities':'^SP500-55','Real Estate':'^SP500-60'}
            
            sector_index_data = pd.DataFrame.from_dict(sector_index_dict,orient='index').reset_index()
            sector_index_data.columns = ['Sector','Symbol']

            for sector in sector_index_data['Symbol']:
                sector_change,sector_change_percent = index_sectors_data.get_index_sector_change(temporality,sector)
                sector_index_data.loc[sector_index_data['Symbol'] == sector,'Change $'] = sector_change
                sector_index_data.loc[sector_index_data['Symbol'] == sector,'Change %'] = sector_change_percent
            sector_index_data_sorted = sector_index_data.sort_values(by='Change %',ascending=False)
            return sector_index_data_sorted

    def sector_name_ticker(sector_index_data):
        sector_name = sector_index_data['Sector'].iat[0]
        sector_symbol = sector_index_data['Symbol'].iat[0]
        sector_change = sector_index_data['Change $'].iat[0]
        sector_change_percent = sector_index_data['Change %'].iat[0]
        return sector_name,sector_symbol,sector_change,sector_change_percent

            
        
        
        
        
    
