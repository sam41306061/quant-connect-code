# region imports
from AlgorithmImports import *
# endregion

class PositionSizeHandler:

    def __init__(self, algorithm: QCAlgorithm, symbol: Symbol, atr_period: int = 13, risk_per_trade: float = 0.10):

        self.algorithm = algorithm
        self.symbol = symbol
        self.atr = algorithm.ATR(symbol, atr_period, MovingAverageType.Simple, Resolution.DAILY)
        self.risk_per_trade = risk_per_trade  # e.g., 0.10 = 10%
        self.entry_price = None


    def position_sizing(self):
            portfolio = self.algorithm.Portfolio
            symbol = self.symbol

            if not portfolio[symbol].Invested:
                if not self.atr.IsReady:
                    return

                price = self.algorithm.Securities[symbol].Price
                equity = portfolio.TotalPortfolioValue
                allocation = equity * self.risk_per_trade
                quantity = int(allocation / price)

                # check if margin is 0 before investing
                if quantity > 0:
                    self.algorithm.MarketOrder(symbol, quantity)
                    self.entry_price = price
                    self.algorithm.Debug(f"Entered {symbol} at {price} with qty {quantity}")

            else:
                current_price = self.algorithm.Securities[symbol].Price

                if self.entry_price is None:
                    return

                gain_pct = (current_price - self.entry_price) / self.entry_price

                if gain_pct >= 0.75:
                    quantity = -portfolio[symbol].Quantity
                    self.algorithm.market_order(symbol, quantity)
                    self.algorithm.Debug(f"Exited {symbol} at {current_price} with {gain_pct*100:.2f}% gain")
                    self.entry_price = None


                ##### Might Delete Later #######
                # # if gain_pct >= 2.0:
                # #     self.algorithm.market_order(symbol)
                # #     self.algorithm.log(f"{symbol}: exited at 200% gain")
                # #     # if price is greater than 150%, close position
                # # if gain_pct >= 1.5:
                # #     self.algorithm.market_order(symbol)
                # #     self.algorithm.log(f"{symbol}: exited at 150% gain")
                # # # if price is greater than 75%, close position
                # # if gain_pct >= .75:
                # #     self.algorithm.market_order(symbol)
                # #     self.algorithm.log(f"{symbol}: exited at 75% gain")
                # # # if price is greater than 75%, close position
                # if gain_pct >= .50:
                #     self.algorithm.market_order(symbol = symbol, quanity= -self.quanity[symbol])
                #     self.algorithm.log(f"{symbol}: exited at 50% gain")


            


