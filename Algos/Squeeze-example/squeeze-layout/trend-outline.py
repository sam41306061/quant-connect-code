# region imports
from AlgorithmImports import *
# endregion

class TrendFilterHandler:
    def __init__(self, algorithm: QCAlgorithm, symbol: Symbol):
        self.algorithm = algorithm
        self.symbol = symbol

        self.indicators = {
            "ema8": algorithm.EMA(symbol, 8, Resolution.Daily),
            "ema21": algorithm.EMA(symbol, 21, Resolution.Daily),
            "ema34": algorithm.EMA(symbol, 34, Resolution.Daily),
            "sma50": algorithm.SMA(symbol, 50, Resolution.Daily),
            "sma100": algorithm.SMA(symbol, 100, Resolution.Daily),
            "sma200": algorithm.SMA(symbol, 200, Resolution.Daily),
            "rsi": algorithm.RSI(symbol, 2, MovingAverageType.Simple, Resolution.Daily),  # optional
            "stoch": algorithm.STO(symbol, 8, 3, 3, Resolution.Daily),
        }

        self.last_trend = None  # Store latest evaluation result (optional)

    def is_bullish_trend(self):
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

    def is_retracement(self):
        i = self.indicators
        if not i["stoch"].IsReady:
            return False

        retracement = (
            i["stoch"].StochK.Current.Value <= 40 and
            i["stoch"].StochD.Current.Value <= 40
        )
        return retracement

    def _indicators_ready(self):
        return all(ind.IsReady for ind in self.indicators.values())

    def update_trend(self):
        """Optional: Call this to evaluate and store latest trend status."""
        bullish = self.is_bullish_trend()
        retrace = self.is_retracement()
        self.last_trend = {"bullish": bullish, "retracement": retrace}
        return self.last_trend
