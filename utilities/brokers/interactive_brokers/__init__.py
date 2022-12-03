from data_management.data_processing import prices_processing,stocks_quantity
from ib_insync import *

ib = IB()
class ib_connection:
    def __init__(self,ip,port,client_id):
        self.ip = ip
        self.port = port
        self.client_id = client_id
        #self.ib = IB()
        
        
        
    def connect(ip,port,client_id):
        
        #ib = IB()
        try:
            ib.connect(ip,port,client_id)
            print('Connection successful')
        except:
            print('Connection failed')
        return ib

        
    
    def disconnect():
        print('*'*50)
        try:
            ib.disconnect()
            print('Disconnected')
        except:
            print('Disconnection failed')
        print('*'*50)


class place_order_by_strategy:
    def __init__(self,ticker,action,order_type,quantity,limit_price,stop_price):
        self.ticker = ticker
        self.action = action
        self.order_type = order_type
        self.quantity = quantity
        self.limit_price = limit_price
        self.stop_price = stop_price
        #self.ib = ib
        
    def define_contract(ticker):
        contract = Stock(symbol=ticker,exchange='SMART',currency='USD')
        ib.qualifyContracts(contract)
        return contract

    def define_order(action,quantity,limitPrice,takeProfitPrice, stopLossPrice):
        order = ib.bracketOrder(action, quantity, limitPrice, takeProfitPrice, stopLossPrice)
        return order
    
    def place_order(contract,order,ticker):
        try:
            for ord in order:
                ib.placeOrder(contract, ord)
                ib.sleep(1)
            print('Order of {} placed'.format(ticker))
        except:
            print('Order of {} failed'.format(ticker))




class ib_data_processing:
    def __init__(self):
        pass

    def get_ib_trades_data():
        ip = '127.0.0.1'
        port = 7497
        client_id = 1
        ib_connection.connect(ip,port,client_id)
        #trades = util.df(ib.trades())
        historial_session = HistoricalSession(startDateTime='2022-09-01 00:00:00', endDateTime='2022-11-10 23:59:59')
        print(historial_session)
        #trades = util.df(ib.reqCompletedOrders(apiOnly=False))
        #trades = util.df(ib.reqPositions())
        trades = util.df(ib.executions())

        
        trades = util.df(ib.portfolio())   #muestra solo las operaciones que estan activas
        trades.to_csv('trades.csv')
        print(trades)
        ib_connection.disconnect()
        return trades

