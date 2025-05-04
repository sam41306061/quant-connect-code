class PositionSizeHandler:

    def __init__(self, algorithm: QCAlgorithm, symbol: Symbol, atr_period: int = 13, risk_per_trade: float = 0.10):

        self.algorithm = algorithm
        self.symbol = symbol
        self.atr = algorithm.ATR(symbol, atr_period, MovingAverageType.Simple, Resolution.DAILY)
        self.risk_per_trade = risk_per_trade  # e.g., 0.10 = 10%


    def position_sizing(self):
        portfolio = self.algorithm.portfolio
        symbol = self.symbol

        # if not currenlty invested in symbol 
        if self.portfolio[symbol].invested == False:
            self.atr.is_ready
            price = self.algorithm.securities[symbol].price
            equity = self.algorithm.portfolio[symbol]
            allocation = equity * position_sizing
            quanity = int(allocation / price)

            self.market_order(symbol, quanity)
            self.entry_price = price 
            self.log(f"Entered {symbol} at {price} with qty {quanity}")

        # If currently invested in position 
        else:
            # check exit levels 
            current_price = self.algorithm.securities[symbol].price

            if self.entry_price is None:
                return 
            
            gain_pct = (current_price - self.entry_price) / self.entry_price
            
            # if price is greater than 200%, close position 
            if gain_pct >= 2.0:
                self.algorithm.market_order(symbol)
                self.algorithm.log(f"{symbol}: exited at 200% gain")
            # if price is greater than 150%, close position
            if gain_pct >= 1.5:
                self.algorithm.market_order(symbol)
                self.algorithm.log(f"{symbol}: exited at 150% gain")
            # if price is greater than 75%, close position
            if gain_pct >= .75:
                self.algorithm.market_order(symbol)
                self.algorithm.log(f"{symbol}: exited at 75% gain")
            # if price is greater than 75%, close position
            if gain_pct >= .50:
                self.algorithm.market_order(symbol)
                self.algorithm.log(f"{symbol}: exited at 50% gain")