# region imports
from AlgorithmImports import *
# endregion

class MeasuredYellowGreenLemur(QCAlgorithm):

    def initialize(self):

        # Set start date
        self.set_start_date(2022, 3, 1)

        # Set cash
        self.set_cash(100000)

        # List of stocks/ETFs
        list_of_tickers = ["AAPL","NVDA","MSFT","AVGO","CRM","ORCL","CSCO","IBM","ACN","ADBE","NOW","TXN",
        "QCOM","PLTR","INTU","AMD","AMAT","PANW","ADI","MU","INTC","LRCX","ANET","KLAC","TER","TRMB","JBL","FFIV","WDC",
        "ZBRA","GEN","FSLR","AKAM","JNPR","EPAM","SWKS","ENPH","LLY", "UNH", "JNJ", "ABBV", "MRK", "ABT", "TMO", "ISRG", "AMGN", "DHR",
            "PFE", "SYK", "BSX", "BMY", "VRTX", "GILD", "MDT", "ELV", "CI", "ZTS",
            "MCK", "REGN", "CVS", "BDX", "HCA", "EW", "COR", "A", "GEHC", "RMD"]

        # List to store symbols
        self.symbols_list = []

        # Loop through list
        for ticker in list_of_tickers:

            # Register
            equity = self.add_equity(ticker, Resolution.DAILY)

            # Store symbol
            self.symbols_list.append(equity.symbol)

        # Trailing stop loss dictionary
        self.TSL_dictionary = {}

    def on_data(self, data: Slice):

        # Loop
        for symbol in self.symbols_list:

            # If not invested
            if self.portfolio[symbol].invested == False:

                # If AAPL
                if symbol.value == "JNPR":

                    # Short 10 shares
                    self.market_order(symbol = symbol, quantity = -10, tag = "Entering short position")

                # Else
                else:

                    # Long 10 shares
                    self.market_order(symbol = symbol, quantity = 10, tag = "Entering long position")

            # If invested
            else:

                # If symbol not in TSL dictionary
                if symbol not in self.TSL_dictionary:

                    # Add
                    self.TSL_dictionary[symbol] = self.portfolio[symbol].average_price

                # If long
                if self.portfolio[symbol].is_long:

                    # If current price above TSLL of symbol
                    if self.securities[symbol].close > self.TSL_dictionary[symbol]:

                        # Update
                        self.TSL_dictionary[symbol] = self.securities[symbol].close

                        # If current price greater than average price by take profit %
                        if self.securities[symbol].close > self.portfolio[symbol].average_price * 1.5:

                            # Sell
                            self.market_order(symbol = symbol, quantity = -self.portfolio[symbol].quantity, tag = "Long take profit")

                            # Remove from TSL dictionary
                            self.TSL_dictionary.pop(symbol)
                    
                    # If current price less than TSLL of symbol by stop loss %
                    elif self.securities[symbol].close < self.TSL_dictionary[symbol] * 0.8:

                        # Sell
                        self.market_order(symbol = symbol, quantity = -self.portfolio[symbol].quantity, tag = "Long TSL")

                        # Remove from TSL dictionary
                        self.TSL_dictionary.pop(symbol)
            
                # If short
                elif self.portfolio[symbol].is_short:

                    # If current price less than TSLL of symbol
                    if self.securities[symbol].close < self.TSL_dictionary[symbol]:

                        # Update
                        self.TSL_dictionary[symbol] = self.securities[symbol].close

                        # If current price lower than average price by take profit %
                        if self.securities[symbol].close < self.portfolio[symbol].average_price * 0.95:

                            # Sell
                            self.market_order(symbol = symbol, quantity = -self.portfolio[symbol].quantity, tag = "Short take profit")

                            # Remove from TSL dictionary
                            self.TSL_dictionary.pop(symbol)
                    
                    # If current price greater than TSLL of symbol by stop loss %
                    elif self.securities[symbol].close > self.TSL_dictionary[symbol] * 1.05:

                        # Sell
                        self.market_order(symbol = symbol, quantity = -self.portfolio[symbol].quantity, tag = "Short TSL")

                        # Remove from TSL dictionary
                        self.TSL_dictionary.pop(symbol)

