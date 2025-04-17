
from AlgorithmImports import *

class BullishSqueezeTrade(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2020,1,1)
        self.set_end_date(2024,12,31)
        self.set_cash(5000)
    
        # Define your symbols
        symbols = ["SPY", "AAPL", "GOOGL"]  # Add your desired symbols
        
        # Create dictionaries to store indicators
        self._195_minute = {}
        self._hour = {}
        self._daily = {}
        self._weekly = {}
        self._monthly = {}
        self._sm = {}
        self._ema8 = {}
        self._ema21 = {}
        self._ema34 = {}
        self._sma50 = {}
        self._sma100 = {}
        self._sma200 = {}
        self._rsi = {}
        self._sto = {}
        self._psar = {}
    
        # Initialize indicators for each symbol
        for symbol in symbols:
            # 195 minute
            self._195_minute[symbol] = self.add_equity(symbol, Resolution.MINUTE).symbol
            # Hour
            self._hour[symbol] = self.add_equity(symbol, Resolution.HOUR).symbol
            # Daily
            self._daily[symbol] = self.add_equity(symbol, Resolution.DAILY).symbol
            
            # Weekly consolidator
            self._weekly[symbol] = self.add_equity(symbol, Resolution.DAILY).symbol
            self._weekly_consolidator = TradeBarConsolidator(7, timedelta(days=7))
            self._weekly_consolidator.data_consolidated += self.weekly_bar_handler
            self.subscription_manager.add_consolidator(self._weekly[symbol], self._weekly_consolidator)
            
            # Monthly consolidator
            self._monthly[symbol] = self.add_equity(symbol, Resolution.DAILY).symbol
            self._monthly_consolidator = TradeBarConsolidator(30, timedelta(days=30))
            self._monthly_consolidator.data_consolidated += self.monthly_bar_handler
            self.subscription_manager.add_consolidator(self._monthly[symbol], self._monthly_consolidator)
            
            # SqueezeMomentum indicator
            self._sm[symbol] = self.sm(symbol, 20, 2, 20, 1.5)
            
            # EMAs
            self._ema8[symbol] = self.EMA(symbol, 8, Resolution.Daily)
            self._ema21[symbol] = self.EMA(symbol, 21, Resolution.Daily)
            self._ema34[symbol] = self.EMA(symbol, 34, Resolution.Daily)
            self._sma50[symbol] = self.SMA(symbol, 50, Resolution.Daily)
            self._sma100[symbol] = self.SMA(symbol, 100, Resolution.Daily)
            self._sma200[symbol] = self.SMA(symbol, 200, Resolution.Daily)
            
            # RSI and Stochastics
            self._rsi[symbol] = self.RSI(symbol, 2, MovingAverageType.Simple, Resolution.Daily)
            self._sto[symbol] = self.STO(symbol, 8, 3, 3, Resolution.Daily)
            self._psar[symbol] = self.psar(symbol, 0.02, 0.02, 0.2)
    
        self.set_warm_up(60, Resolution.DAILY)  # 60 days warm up period


    def weekly_bar_handler(self, consolidated):
        symbol = consolidated.Symbol
        self.debug(f"Weekly bar handler: {symbol}, Price: {consolidated.Close}")
    
    def monthly_bar_handler(self, consolidated):
        symbol = consolidated.Symbol
        self.debug(f"Monthly bar handler: {symbol}, Price: {consolidated.Close}")

    def on_data(self, slice):
        if self.is_warming_up:
            self.debug(f"Warming up.. {self.is_warming_up}")
            self.debug(f"Received new data slice with{len(slice.Keys)} symbols")
            return
        




    # def on_data(self, slice):
    # if self.is_warming_up:
    #     self.debug(f"Warming up... {self.is_warming_up}")
    #     return
        
    # # Log basic information about the incoming data
    # self.debug(f"Received new data slice with {len(slice.Keys)} symbols")
    
    # # Process each symbol individually
    # for symbol in slice.Keys:
    #     bar = slice.Bars[symbol]
    #     self.debug(f"Symbol: {symbol}, "
    #               f"Price: {bar.Close}, "
    #               f"Volume: {bar.Volume}, "
    #               f"Time: {self.Time}")

    # # Also log consolidator status if needed
    # if hasattr(self, '_weekly_consolidator'):
    #     self.debug(f"Weekly consolidator count: {self._weekly_consolidator.ConsolidatorCount}")
    # if hasattr(self, '_monthly_consolidator'):
    #     self.debug(f"Monthly consolidator count: {self._monthly_consolidator.ConsolidatorCount}")







    def check_squeeze_conditions(self):
        pass
        self.debug("Made it down to the squeeze condition check")
    
    def check_trend_conditions(self):
        pass
        self.debug("Made it down to the trend condtions check")

    def check_momentum_conditions(self):
        pass
        self.debug("Made it down to the momentum check ")