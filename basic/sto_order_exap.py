# region imports
from AlgorithmImports import *
# endregion

class DemoQuantConnectTest1(QCAlgorithm):
    
    def initialize(self):
        self.set_start_date(2022, 1, 6)
        self.set_end_date(2024, 6, 6)
        self.set_cash(5000)
        self.ticker = self.add_equity("SPY", Resolution.DAILY)
        self.nema1 = self.sma(self.ticker.symbol,50)
        self.rsi = self.RSI(self.ticker.symbol, 13, Resolution.DAILY)

        self.set_warm_up(100)


    def on_data(self, data:Slice):
        if self.is_warming_up:
            return

        rsi_value = self.rsi.current.value # add back later

        if not self.portfolio.invested:
           if self.ticker.price > self.nema1.current.value and rsi_value < 10 :
                self.market_order(self.ticker.symbol, 1)
                self.stop_market_order(self.ticker.symbol, -1, data[self.ticker.symbol].close * 0.80)
                # self.debug("Current price:"+str(self.ticker.price)+">"+" "+"MA Price:"+str(self.nema1.current.value))

        if self.portfolio.invested:
             if self.ticker.price < self.nema1.current.value and rsi_value > 90:
                self.liquidate()
                # self.debug("Current price:"+str(self.ticker.price)+"<"+" "+"MA Price:"+str(self.nema1.current.value))
        self.plot("SPY","MA100",self.nema1.current.value)
        self.plot("SPY","SPY",self.ticker.price)

    def on_order_event(self, order_event: OrderEvent):
        order = self.transactions.get_order_by_id(order_event.OrderId)
        self.debug("{0}:{1}:{3}")