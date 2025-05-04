# region imports
from AlgorithmImports import *
# endregion

class MeasuredYellowGreenLemur(QCAlgorithm):

    def initialize(self):

        # Set start date
        self.set_start_date(2022, 3, 1)

        # Set cash
        self.set_cash(1000000)

        # List of stocks/ETFs
        list_of_tickers = ["AAPL","GOOG","SPY"]

        # List to store symbols
        self.symbols_list = []

        # Loop through list
        for ticker in list_of_tickers:

            # Register
            equity = self.add_equity(ticker, Resolution.Minute)

            # Store symbol
            self.symbols_list.append(equity.symbol)

    def on_data(self, data: Slice):

        # Loop
        for symbol in self.symbols_list:

            # If not invested
            if self.portfolio[symbol].invested == False:

                # If AAPL
                if symbol.value == "AAPL":

                    # Short 10 shares
                    self.market_order(symbol = symbol, quantity = -10)

                # Else
                else:

                    # Long 10 shares
                    self.market_order(symbol = symbol, quantity = 10)

            # If invested
            else:

                # If short
                if self.portfolio[symbol].is_short == True:

                    # If current price greater than average price by stop loss percent
                    if self.securities[symbol].close > self.portfolio[symbol].average_price * 1.05:

                        # Sell
                        self.market_order(symbol = symbol, quantity = -self.portfolio[symbol].quantity)

                # If long
                elif self.portfolio[symbol].is_long == True:

                    # If current price less than average price by stop loss percent
                    if self.securities[symbol].close < self.portfolio[symbol].average_price * 0.95:

                        # Sell
                        self.market_order(symbol = symbol, quantity = -self.portfolio[symbol].quantity)