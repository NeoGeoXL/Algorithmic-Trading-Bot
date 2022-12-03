import gspread
import pathlib
import datetime as dt
import pandas as pd


class etoro_data_processing:
    def __init__(self,sa,month,week,wks,data,ticker,action,initial_price,stop_loss,take_profit,ratio,strategy,temporality):
        self.sa = sa
        self.month = month
        self.week = week
        self.wks = wks
        self.data = data
        self.ticker = ticker
        self.action = action
        self.initial_price = initial_price
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.ratio = ratio
        self.strategy = strategy
        self.temporality = temporality
    
    def create_operation_data_list(ticker,action,initial_price,stop_loss,take_profit,ratio,strategy,temporality):
        
        now=dt.datetime.now()
        open_operation_date=now.strftime("%d/%m/%Y")
        final_price = ''
        close_operation_date =''
        win_loss = ''
        profit = ''
        loss= ''
        etoro_spread = ''
        notes = ''
        data = [[ticker,action,initial_price,open_operation_date,final_price,close_operation_date,
        stop_loss,take_profit,ratio,temporality,strategy,win_loss,profit,loss,etoro_spread,notes]]
        return data


    def create_massive_sector_operation_data_list(ticker,action,market_price,stop_loss,take_profit,pl_ratio,strategy,temporality,tema_short_period,tema_long_period,tema_trend_period,rsi_period,rsi_umbral,adx_period,adx_umbral,sector_temporality,rsi,adx,ds1,ds2,sector,industry,sector_change,sector_change_percent):
        
        now=dt.datetime.now()
        open_operation_date=now.strftime("%d/%m/%Y")
        final_price = ''
        close_operation_date =''
        win_loss = ''
        profit = ''
        loss= ''
        etoro_spread = ''
        notes = ''
        data = [[ticker,action,market_price,open_operation_date,final_price,close_operation_date,
        stop_loss,take_profit,pl_ratio,temporality,strategy,win_loss,profit,loss,etoro_spread,notes,
        tema_short_period,tema_long_period,tema_trend_period,rsi_period,rsi_umbral,rsi,adx,adx_period,adx_umbral,
        ds1,ds2,sector,sector_temporality,sector_change,sector_change_percent,industry]]
        return data

    def connect_to_google_sheet():
        CURRENT_DIR = pathlib.Path.cwd()
        KEY_DIR = CURRENT_DIR.joinpath('./','utilities','brokers','etoro','key')
        sa = gspread.service_account(filename=KEY_DIR.joinpath('service_account.json'))
        return sa

    def open_worksheet(sa,database_name,month):
        sheet = sa.open(database_name)
        wks = sheet.worksheet(month)
        return wks

    def get_all_values(wks):
        raw_data =wks.get_all_values()
        df = pd.DataFrame(raw_data)
        return df

    def append_operation_data(wks,data):
        wks.append_row(data[0])
        

    