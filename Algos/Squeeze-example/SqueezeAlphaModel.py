#region imports
from AlgorithmImports import *
from TTMSqueezePro import TTMSqueezePro
from MarketHours import MarketHours
# endregion

class SqueezeAlphaModel(AlphaModel):
    algorithm = None

    def __init__(self, algorithm, ticker, option):
        self.ticker = ticker
        self.option = option
        self.algorithm = algorithm
        self.symbol = algorithm.AddEquity(self.ticker, resolution = Resolution.Daily)
        self.marketHours = MarketHours(self.algorithm, self.ticker)

        # indicators
        self.squeeze = TTMSqueezePro("Squeeze", length = 20)
        algorithm.RegisterIndicator(self.ticker, self.squeeze, Resolution.Daily)
        # history = self.algorithm.History(self.symbol.Symbol, 21, Resolution.Daily)
        # self.squeeze.Warmup(history.loc[self.ticker])
        # TODO: think about warming up the indicator: https://www.quantconnect.com/docs/v2/writing-algorithms/indicators/manual-indicators
        # self.algorithm.SetWarmUp(TimeSpan.FromDays(60))
        self.algorithm.WarmUpIndicator(self.ticker, self.squeeze, Resolution.Daily)

        self.indicators = {
            'Squeeze' : self.squeeze
        }
        self.algorithm.benchmark.AddIndicators(self.indicators)

    def Update(self, algorithm, data):
        insights = []
        if self.ticker not in data.Keys: return insights

        if algorithm.IsWarmingUp: return insights
        if not self.squeeze.IsReady: return insights

        # reset your indicators when splits and dividends occur.
        # If a split or dividend occurs, the data in your indicators becomes invalid because it doesn't account for the price adjustments that the split or dividend causes.
        if data.Splits.ContainsKey(self.ticker) or data.Dividends.ContainsKey(self.ticker):
            # Reset the indicator
            self.squeeze.Reset()
        self.algorithm.Log("Squeeze: {}".format(self.squeeze.Current.Value))
        self.algorithm.benchmark.PrintBenchmark()

        return insights
