# region imports
from AlgorithmImports import *
# endregion

class TrendHandler:

    def __init__(self, algorithm: QCAlgorithm, symbol: Symbol):
        self.algorithm = algorithm
        self.symbol = symbol

        self.indicators = {
                "ema8": self.algorithm.ema(symbol, 8, Resolution.DAILY),
                "ema21": self.algorithm.ema(symbol, 21, Resolution.DAILY),
                "ema34": self.algorithm.ema(symbol, 34, Resolution.DAILY),
                "sma50": self.algorithm.sma(symbol, 50, Resolution.DAILY),
                "sma100": self.algorithm.sma(symbol, 100, Resolution.DAILY),
                "sma200": self.algorithm.sma(symbol, 200, Resolution.DAILY),
                "rsi": self.algorithm.rsi(symbol, 2, MovingAverageType.SIMPLE, Resolution.DAILY),
                "stoch": self.algorithm.sto(symbol, 8, 3, 3, Resolution.DAILY),
            }
        self.last_trend = None

    def is_bullish_trend(self, symbols):
        # check if indicators are not ready
        if not self._indicators_ready():
            return False

        i = self.indicators
        bullish = (
            i["ema8"].Current.Value > i["ema21"].Current.Value and
            i["ema21"].Current.Value > i["ema34"].Current.Value and
            i["ema34"].Current.Value > i["sma50"].Current.Value and
            i["sma50"].Current.Value > i["sma100"].Current.Value and
            i["sma100"].Current.Value > i["sma200"].Current.Value
        )
        return bullish

    def is_retracement_stochs(self):
       
        i = self.indicators
        
        if not i["stoch"].IsReady:
            return False

        retracement_stochs = (
            i["stoch"].StochK.Current.Value <= 40 and
            i["stoch"].StochD.Current.Value <= 40
        )
        return retracement_stochs
        self.log(f"returning rsi{retracement_stochs}")

    def is_retracement_rsi(self):
        i = self.indicators
        
        if not i["rsi"].IsReady:
            return False
        
        retracement_rsi = (
            i["rsi"].rsi.Current.Value <= 10
        )
        return retracement_rsi
        self.log(f"returning rsi{retracement_rsi}")

    def _indicators_ready(self):
        return all(ind.IsReady for ind in self.indicators.values())


