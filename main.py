from trading_bot import *
from data_management.get_data import *
from signals.indicators import *
from utilities.brokers.interactive_brokers import *
from utilities.create_reports.create_report import etoro_diary_report
from config import *
import os



def main():
        while True: 
            print("*** Stock Algorithmic Trading Menu ***")
            print("1. Activate a trading bot")
            print("2. Create a new report")
            print("3. Exit")
            option = input("Select an option: ")
            if option == '1':
                os.system('cls||clear')
                print("Select the bot you want to activate: ")
                print("1. Normal Bot")
                print("2. Sector Massive Analysis Bot")
                option_bot = input("Select a bot option: ")
                if option_bot == '1':
                    normal_bot.activate_bot(list_of_stocks,temporality,loss,profit,capital,tema_short_period,tema_long_period,tema_trend_period,rsi_period,rsi_umbral,adx_period,adx_umbral)
                elif option_bot == '2':
                    sector_massive_analysis_df=sector_analysis_bot.activate_sector_analysis_bot(sector_temporality,temporality,loss,profit,tema_short_period,tema_long_period,tema_trend_period,rsi_period,rsi_umbral,adx_umbral,adx_period)
                    try:
                        sector_analysis_bot.append_new_stocks_to_sheets(index,sector_massive_analysis_df,strategy,pl_ratio,database_name,month,temporality,tema_short_period,tema_long_period,tema_trend_period,rsi_period,rsi_umbral,adx_period,adx_umbral,sector_temporality)
                        print(sector_massive_analysis_df)
                    except:
                        print("Error appending new stocks to the database")
            elif option == '2':
                etoro_diary_report.create_daily_report(daily_date,month_etoro,week)
            elif option == '3':
                break


if __name__ == '__main__':
    main()
    