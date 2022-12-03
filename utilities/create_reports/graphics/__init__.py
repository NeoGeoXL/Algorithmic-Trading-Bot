import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pathlib


CURRENT_DIR = pathlib.Path.cwd()
DAILY_GRAPHS_DIR = CURRENT_DIR.joinpath('./','utilities','create_reports','daily_graphs')

win_loss_palette =['green','red']
long_short_palette =['cyan','orange']
class etoro_diary_graphs:
    def __init__(self,data):
        self.data = data
    def pnl_by_stock_graph(data):
        nan_value = float("NaN")
        data.replace("", nan_value, inplace=True)
        data.dropna(how='all', axis=1, inplace=True)
        loss_money = data['Loss']*-1
        fig, ax = plt.subplots(figsize=(10,5))
        ax = sns.barplot(x='Stock', y='Profit', data=data, color='green')
        ax = sns.barplot(x='Stock', y=loss_money, data=data, color='red')
        ax.set_title("Profits and Loss by Stock Day Operation",fontsize=15)
        ax.set_xlabel('Stock')
        ax.set_ylabel('Loss/Profit')
        plt.savefig(DAILY_GRAPHS_DIR.joinpath('pnl_by_stock.png'))


    
    def bar_operations_distribution(data):
        profit_total = data['Profit'].sum()
        loss_total = data['Loss'].sum()
        total_money = pd.DataFrame({'Win/Loss':['Win Money','Loss Money'],'Total':[profit_total,loss_total]})
        nan_value = float("NaN")
        data.replace("", nan_value, inplace=True)
        data.dropna(how='all', axis=1, inplace=True)
        fig, ax = plt.subplots(figsize=(10,5),nrows=1,ncols=2)
        ax[0] = sns.countplot(data=data,x='Win o Loss', ax=ax[0], palette=win_loss_palette,order=['Win','Loss'])
        ax[0].set_xlabel('Win/Loss')
        ax[0].set_ylabel('Total of Operations')
        ax[0].bar_label(ax[0].containers[0], label_type='edge')
        #ax[1] = plt.pie(total_money['Total'],labels=total_money['Win/Loss'],autopct='%1.1f%%',colors=win_loss_palette)
        ax[1] = sns.barplot(data=total_money,x='Win/Loss',y='Total',ax=ax[1],palette=win_loss_palette)
        ax[1].set_xlabel('Win/Loss')
        ax[1].set_ylabel('USD')
        ax[1].bar_label(ax[1].containers[0], label_type='edge')
        fig.suptitle('Bar distribution of Win/Loss Operations',fontsize=15)
        plt.savefig(DAILY_GRAPHS_DIR.joinpath('bar_operations_distribution.png'))
        
        

        
    def pie_distribution_operations(data):
        profit_total = data['Profit'].sum()
        loss_total = data['Loss'].sum()
        total_money = pd.DataFrame({'Win/Loss':['Win Money','Loss Money'],'Total':[profit_total,loss_total]})
        nan_value = float("NaN")
        data.replace("", nan_value, inplace=True)
        data.dropna(how='all', axis=1, inplace=True)
        buy_count=0
        sell_count=0
        for i in data['Action']:
            if i == 'BUY':
                buy_count += 1
            elif i == 'SELL':
                sell_count += 1
        buy_sell_df = pd.DataFrame({'Action':['Long','Short'],'Total':[buy_count,sell_count]})
        fig = plt.subplots(figsize=(10,5))
        ax1 = plt.subplot2grid((1,2),(0,0))
        plt.pie(total_money['Total'],labels=total_money['Win/Loss'],autopct='%1.1f%%',colors=win_loss_palette)
        ax2 = plt.subplot2grid((1,2),(0,1))
        plt.pie(buy_sell_df['Total'],labels=buy_sell_df['Action'],autopct='%1.1f%%',colors=long_short_palette)
        plt.suptitle('Pie distribution of Daily Operations',fontsize=15)
        plt.savefig(DAILY_GRAPHS_DIR.joinpath('pie_distribution_operations.png'))

    
    def long_short_bar_distribution(data):
        data_long = data[data['Action'] == 'BUY']
        profit_total_long = data_long['Profit'].sum()
        loss_total_long = data_long['Loss'].sum()
        total_money_long = pd.DataFrame({'Win/Loss':['Profit','Loss'],'Total':[profit_total_long,loss_total_long]})

        data_short = data[data['Action'] == 'SELL']

        profit_total_short = data_short['Profit'].sum()
        loss_total_short = data_short['Loss'].sum()
        total_money_short = pd.DataFrame({'Win/Loss':['Profit','Loss'],'Total':[profit_total_short,loss_total_short]})

        fig, ax = plt.subplots(figsize=(10,5),nrows=1,ncols=2)
        ax[0] = sns.barplot(data=total_money_long,x='Win/Loss',y='Total',ax=ax[0],palette=win_loss_palette)
        ax[0].set_title('Long Operations',fontsize=10)

        ax[0].set_ylabel('Total USD')
        ax[0].bar_label(ax[0].containers[0], label_type='edge')
        ax[1] = sns.barplot(data=total_money_short,x='Win/Loss',y='Total',ax=ax[1],palette=win_loss_palette)
        ax[1].set_title('Short Operations',fontsize=10)
   
        ax[1].set_ylabel('Total USD')
        ax[1].bar_label(ax[1].containers[0], label_type='edge')
        fig.suptitle('Profit and Loss of Long and Short Daily Operations \n \n',fontsize=15)
        plt.tight_layout()
        plt.savefig(DAILY_GRAPHS_DIR.joinpath('long_short_bar_distribution.png'))

        




    def total_win_money(data):
        profit_total = data['Profit'].sum()
        loss_total = data['Loss'].sum()
        total = profit_total - loss_total
        return total





class etoro_weekly_graphs:
    def __init__(self,data):
        self.data = data
    def weekly_profit_graph(data):
        sns.set_style("whitegrid")
        sns.set_context("paper")
        sns.set_palette("tab10")
        sns.set_color_codes("pastel")
        plt.figure(figsize=(20, 10))
        plt.title("Etoro Diary")
        plt.xlabel("Date")
        plt.ylabel("Profit")
        plt.plot(data['Open Operation Date'], data['Profit'])
        plt.show()

        