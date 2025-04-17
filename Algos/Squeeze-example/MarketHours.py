#region imports
from AlgorithmImports import *
#endregion

class MarketHours:
    def __init__(self, algorithm, symbol):
        self.algorithm = algorithm
        self.hours = algorithm.Securities[symbol].Exchange.Hours

    def get_CurrentOpen(self):
        return self.hours.GetNextMarketOpen(self.algorithm.Time, False)

    def get_CurrentClose(self):
        return self.hours.GetNextMarketClose(self.get_CurrentOpen(), False)