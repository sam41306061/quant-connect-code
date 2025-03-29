# region imports
from AlgorithmImports import *
# endregion

class GeekyOrangeHamster(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2023, 6, 6)  # Set Start Date
        self.SetEndDate(2023,6,6)
        self.SetCash(5000)  # Set Strategy Cash
        self.ticker=self.AddEquity("SPY", Resolution.Minute)
        self.newma=self.SMA(self.ticker.Symbol,100)
        self.rsi=self.RSI(self.ticker.Symbol,14, Resolution.Minute)
        self.newma30=None
        self.Consolidate(self.ticker.Symbol,timedelta(minutes=30),self.OnDataConsolidated)

        self.SetWarmup(100)
        self.lastTradeTime=None

    def OnData(self, data: Slice):
        pass
    
    def OnDataConsolidated(self,bar):
        self.currentbar=bar
        self.Plot("30min Chart","Close",self.currentbar.Close)

        if self.newma30 is None:
            self.newma30=self.SMA(self.ticker.Symbol,30)
        else:
            self.newma30.Update(bar.EndTime,bar.Close)

        if self.newma30.IsReady:
            ma30_value=self.newma30.Current.Value
            self.Plot("30min Chart","30min MA",ma30_value)
        
        if self.newma30 is not None and self.newma30.IsReady:
            currentBarEndTime = self.currentbar.EndTime
            if self.lastTradeTime is not None and currentBarEndTime-self.lastTradeTime < timedelta(minutes=30):
                return

            ma30_value=self.newma30.Current.Value
            close_price=self.currentbar.Close

            if close_price>ma30_value and self.newma30 is not None:
                self.SetHoldings(self.ticker.Symbol,1.0)
                self.Debug("Buy signal")
                self.lastTradeTime=currentBarEndTime

            if close_price<ma30_value:
                self.Liquidate(self.ticker.Symbol)
                self.Debug("Sell signal")
                self.lastTradeTime=currentBarEndTime