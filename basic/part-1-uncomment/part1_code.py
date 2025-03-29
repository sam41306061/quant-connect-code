# region imports
from AlgorithmImports import *
# endregion

class GeekyOrangeHamster(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2006, 1, 4)  # Set Start Date
        self.SetEndDate(2023,6,6)
        self.SetCash(5000)  # Set Strategy Cash
        self.ticker=self.AddEquity("SPY", Resolution.Daily)
        self.newma=self.SMA(self.ticker.Symbol,100)
        self.rsi=self.RSI(self.ticker.Symbol,14, Resolution.Daily)

        self.SetWarmup(100)
        

    def OnData(self, data: Slice):
        if self.IsWarmingUp:
            return

        rsi_value=self.rsi.Current.Value  

        if not self.Portfolio.Invested:
            if self.ticker.Price>self.newma.Current.Value:
                self.SetHoldings(self.ticker.Symbol, 1)
                self.Debug("We are entering because Current Price is. "+str(self.ticker.Price)+ "  > than MA" + str(self.newma.Current.Value))
                #self.StopMarketOrder(self.ticker.Symbol, -1, self.Securities[self.ticker.Symbol].Close*0.90)
        
        if self.Portfolio.Invested:
            if self.ticker.Price<(self.Portfolio[self.ticker.Symbol].AveragePrice)*0.90:
                self.Liquidate()
        if self.Portfolio.Invested:
            if self.ticker.Price>(self.Portfolio[self.ticker.Symbol].AveragePrice)*1.30:
                self.Liquidate()
        
        if self.Portfolio.Invested:
            if self.ticker.Price<self.newma.Current.Value:
                self.Liquidate()
                self.Debug("We are exiting because Current Price is   "+str(self.ticker.Price)+ "  < than MA" + str(self.newma.Current.Value))
        self.Debug("Number of shares"+str(self.Portfolio[self.ticker.Symbol].Quantity)+ "@Price" + str(self.Portfolio[self.ticker.Symbol].AveragePrice))
        self.Plot("SPY","MA30",self.newma.Current.Value)
        self.Plot("SPY","SPY",self.ticker.Price)

    def OnOrderEvent(self, orderEvent):
        order=self.Transactions.GetOrderById(orderEvent.OrderId)
        self.Log("{0}: {1}: {2}:".format(self.Time,order.Type,orderEvent))