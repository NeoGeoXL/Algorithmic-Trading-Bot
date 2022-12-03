import pandas as pd

class moving_averages_processing:
    def __init__(self,tema_short,tema_long):
        self.tema_short = tema_short
        self.tema_long = tema_long

    def delta_temas(tema_short, tema_long):
        delta=tema_short-tema_long
        return delta



        

class prices_processing:
    def __init__(self,profit,loss,entry_signal):
        self.profit = profit
        self.loss = loss
        self.entry_signal = entry_signal
    
    def market_price(entry_signal):
        market_price= round(entry_signal['Close'].iat[0],2)
        return market_price

    def stop_loss_long(price,loss):
        stop_loss_long = round(price -(price*loss),2)
        return stop_loss_long

    def stop_loss_short(price,loss):
        stop_loss_long = round(price + (price*loss),2)
        return stop_loss_long
    
    def take_profit_long(price,profit):
        take_profit_long = round(price + (price*profit),2)
        return take_profit_long
    
    def take_profit_short(price,profit):
        take_profit_short = round(price - (price*profit),2)
        return take_profit_short
    
class stocks_quantity:
    def __init__(self,price,invest_capital):
        self.price = price
        self.invest_capital = invest_capital
    
    def quantity(price,invest_capital):
        quantity = round(invest_capital/price,2)
        return quantity
    