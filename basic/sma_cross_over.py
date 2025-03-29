# region imports
from AlgorithmImports import *
# endregion

class Magnificent7(QCAlgorithm):
    def initialize(self):
        self.set_start_date(2020, 11, 10)
        self.set_cash(100000)
        
        # Add AAPL with daily resolution
        self._symbolAA = self.add_equity("AAPL", Resolution.DAILY)
        
        # Create two moving averages
        self._shortMA = SimpleMovingAverage(50)  # Short-term MA
        self._longMA = SimpleMovingAverage(200)  # Long-term MA
        
        # Register indicators for automatic updates
        self.register_indicator(self._symbolAA.Symbol, self._shortMA, Resolution.DAILY)
        self.register_indicator(self._symbolAA.Symbol, self._longMA, Resolution.DAILY)
        
        # Set benchmark
        self.SetBenchmark("SPY")

    def on_data(self, slice: Slice):
        # Get the current bar
        bar = slice.bars.get(self._symbolAA.Symbol)
        if bar is None:
            return

        # Check if both moving averages are ready
        if not (self._shortMA.is_ready and self._longMA.is_ready):
            return

        # Plot both moving averages
        self.plot("MovingAverages", "ShortMA", self._shortMA.current.value)
        self.plot("MovingAverages", "LongMA", self._longMA.current.value)
        self.plot("MovingAverages", "Price", bar.Close)

        # Trading logic
        if not self.portfolio.invested:
            # Buy when short MA crosses above long MA
            if self._shortMA.current.value > self._longMA.current.value:
                self.set_holdings("AAPL", 1)
                self.debug("Buying AAPL: Price={}".format(bar.Close))
        else:
            # Sell when short MA crosses below long MA
            if self._shortMA.current.value < self._longMA.current.value:
                self.set_holdings("AAPL", 0)
                self.debug("Selling AAPL: Price={}".format(bar.Close))