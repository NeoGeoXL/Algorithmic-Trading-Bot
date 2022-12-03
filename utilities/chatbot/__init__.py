import telegram

telegram_token = '5404103281:AAHBBDrYFDyHgHyxInL0ss3Gqtnbqlh7GvE'

class telegram_notifications:
    def __init__(self,stock,action,price,stop_loss,take_profit):
        self.stock = stock
        self.action = action
        self.price = price
        self.stop_loss = stop_loss
        self.take_profit = take_profit
    
    def send_message(stock,action,price,stop_loss,take_profit):
        
        bot = telegram.Bot(token=telegram_token)

        text='\U0001F4CC'+' '+'Stock Symbol :' +' '+ stock + \
        '\n'+ '\n'+ \
        '\U0001F4C9'+' '+'Operation Action: '+ ' '+ action + \
        '\n'+ '\n' + \
        '\U0001F4B0'+' '+'Price: ' + ' ' +'$'+str(price) + \
        '\n'+ '\n' + \
        '\U0001F534'+' '+'Stop loss: ' + ' ' +'$'+str(stop_loss) + \
        '\n'+ '\n' + \
        '\U0001F7E2'+' '+'Take profit: ' + ' ' +'$'+str(take_profit) 

        bot.send_message(chat_id='@stock_trading_signals1', text=text)