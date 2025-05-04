# region imports
from AlgorithmImports import *
# endregion

class PositionSizeHandler:
    def __init__(self, algorithm: QCAlgorithm, symbol: Symbol, atr_period: int = 14, risk_per_trade: float = 0.05):
        self.algorithm = algorithm
        self.symbol = symbol
        self.atr = algorithm.ATR(symbol, atr_period, MovingAverageType.Simple, Resolution.DAILY)
        self.risk_per_trade = risk_per_trade  # e.g., 0.05 = 5%

    def is_ready(self):
        return self.atr.IsReady and self.symbol in self.algorithm.Securities

    def get_atr(self):
        return self.atr.Current.Value if self.atr.IsReady else None

    def get_position_size(self, stop_multiple: float = 1.5) -> int:
        """
        Calculates position size based on ATR * stop_multiple
        """
        if not self.is_ready():
            return 0

        price = self.algorithm.Securities[self.symbol].Price
        atr = self.get_atr()
        stop_distance = atr * stop_multiple
        capital_to_risk = self.algorithm.Portfolio.TotalPortfolioValue * self.risk_per_trade

        if stop_distance == 0:
            return 0

        position_size = int(capital_to_risk / stop_distance)
        return max(position_size, 0)

