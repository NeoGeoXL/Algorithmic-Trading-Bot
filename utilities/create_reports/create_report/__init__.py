import gspread
import pathlib
from utilities.brokers.etoro import etoro_data_processing
import pandas as pd
from fpdf import FPDF
from utilities.create_reports.graphics import *
from ib_insync import *
from utilities.brokers.interactive_brokers import ib_connection
pd.options.mode.chained_assignment = None  # default='warn'


class etoro_diary_report:
    def __init__():
        pass
    
    def get_sheets_daily_data(daily_date,month,week):
        sa = etoro_data_processing.connect_to_google_sheet()
        wks = etoro_data_processing.open_worksheet(sa,month,week)
        total_data = etoro_data_processing.get_all_values(wks)
        total_data = pd.DataFrame(total_data)
        total_data.rename(columns=total_data.iloc[0], inplace = True)
        total_data = total_data.drop(total_data.index[0])
        total_data = total_data.reset_index()
        total_data = total_data.drop(columns='index')
        daily_data = total_data[total_data['Open Operation Date'] == daily_date]
        #Formating strings data
        numeric_data = ['Initial Price','Final Price','Stop Loss','Take Profit','Profit','Loss','Etoro Spread']
        string_columns = ['Stock','Action','Profit:Loss','Temporality','Strategy','Win o Loss','Notes']
        daily_data[string_columns]=daily_data[string_columns].apply(lambda x: x.astype('string'))
        daily_data[numeric_data]=daily_data[numeric_data].apply(pd.to_numeric, errors='coerce', axis=1)
        #daily_data['Open Operation Date'] = pd.to_datetime(daily_data['Open Operation Date'])
        #daily_data['Close Operation Date'] = pd.to_datetime(daily_data['Close Operation Date'])
        return daily_data


    def create_daily_graphs(daily_date,month,week):
        data=etoro_diary_report.get_sheets_daily_data(daily_date,month,week)
        total_money = round(etoro_diary_graphs.total_win_money(data),2)
        etoro_diary_graphs.pnl_by_stock_graph(data)
        etoro_diary_graphs.bar_operations_distribution(data)
        etoro_diary_graphs.pie_distribution_operations(data)
        etoro_diary_graphs.long_short_bar_distribution(data)
        total_money = round(etoro_diary_graphs.total_win_money(data),2)
        return total_money

    def create_daily_report(daily_date,month,week):
        
        total_money = etoro_diary_report.create_daily_graphs(daily_date,month,week)
        width=210
        height=297

        CURRENT_DIR = pathlib.Path.cwd()
        DAILY_REPORTS_DIR = CURRENT_DIR.joinpath('./','reports','etoro','daily')
        DAILY_GRAPHS_DIR = CURRENT_DIR.joinpath('./','utilities','create_reports','daily_graphs')
        pdf = FPDF('P', 'mm', 'A4')
        pdf.add_page()
        pdf.image(str(DAILY_GRAPHS_DIR.joinpath('logo.png')), 0, 0,width,height/6)
        pdf.set_font("Arial", size=20, style='B')
        pdf.set_xy(10, 60)
        pdf.cell(200, 10, txt= f"Daily Report of {daily_date}", ln=1, align="L")
        pdf.set_font("Arial", size=15)
        pdf.cell(200, 10, txt= "", ln=1, align="C")
        pdf.set_xy(10, 70)
        if total_money > 0:
            pdf.cell(200,10, txt= "This day you won: ${}".format(abs(total_money)), align="L")
        else:
            pdf.cell(200,10, txt= "This day you lost: ${}".format(abs(total_money)), align="L")
        pdf.image(f'{DAILY_GRAPHS_DIR}/pnl_by_stock.png', x=10, y=85, w=200)
        pdf.image(f'{DAILY_GRAPHS_DIR}/bar_operations_distribution.png', x=10, y=190, w=200)
        
        pdf.add_page()
        pdf.image(f'{DAILY_GRAPHS_DIR}/pie_distribution_operations.png', x=5, y=20, w=200)
    
        pdf.image(f'{DAILY_GRAPHS_DIR}/long_short_bar_distribution.png', x=5, y=120, w=200)
        
        format_date = daily_date.replace('/','-')
        pdf.output(DAILY_REPORTS_DIR.joinpath('Daily Report {}.pdf'.format(format_date)))



class ib_diary_report:
    def __init__():
        pass

    def get_ib_data():
        pass

