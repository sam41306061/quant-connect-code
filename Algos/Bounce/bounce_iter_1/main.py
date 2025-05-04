# region imports
from AlgorithmImports import *
from indicators.trend_handler import *
from indicators.momentum_handler import *
from custom_sectors.sectors import *
from risk_controls.position_sizing import * 
from risk_controls.stop_loss import *
# endregion


class BullishStrategy(QCAlgorithm):
    def Initialize(self):
        self.set_start_date(2022, 1, 1)
        self.set_end_date(2025, 2, 28)
        self.set_cash(10000)

        # Create handlers properly
        self.sector_handler = SectorHandler()
        self.trend_handler = {}
        self.momentum_handler = {}
        self.position_sizing = {}
        self.set_stop_loss = {}
        self.symbols = []

        # Now populate symbols (just one sector for example)
        for ticker in self.sector_handler.sectors["HealthCare"]:
            symbol = self.add_equity(ticker, Resolution.DAILY).Symbol
            self.symbols.append(symbol)
            self.trend_handler[symbol] = TrendHandler(self, symbol)
            self.momentum_handler[symbol] = MomentumHandler(self, symbol)
            self.position_sizing[symbol] = PositionSizeHandler(self, symbol)

    def OnData(self, data: Slice):
        for symbol in self.symbols:
            if symbol not in data or not data[symbol]:
                continue
            
            trend_handler = self.trend_handler.get(symbol)
            momentum_handler = self.momentum_handler.get(symbol)
            position_sizing = self.position_sizing.get(symbol)

            if not trend_handler or not momentum_handler or not position_sizing:
                continue

            if trend_handler.is_bullish_trend and momentum_handler.identify_pull_back():
                self.Debug(f"Identified a clear entry to the position on {symbol}")
                position_sizing.position_sizing() 
