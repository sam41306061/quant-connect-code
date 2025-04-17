# region imports
from AlgorithmImports import *
# endregion

class AdaptableRedOrangeHorse(QCAlgorithm):

    def initialize(self):

        # Set Start Date
        self.set_start_date(2021, 1, 1)

        # Set cash
        self.set_cash(100000)

        # Add AAPL
        self.AAPL_symbol = self.add_equity("AAPL", Resolution.DAILY).symbol

        # Past data store
        self.past_data = []

    def on_data(self, data: Slice):

        # Store
        self.past_data.append(self.securities[self.AAPL_symbol].close - self.securities[self.AAPL_symbol].open)

        # If not invested
        if self.portfolio[self.AAPL_symbol].invested == False:
            
            # If stored 2 and above
            if len(self.past_data) > 2:

                # If 3 red bars
                if (
                    
                    self.past_data[-3] < 0 and

                    self.past_data[-2] < 0 and

                    self.past_data[-1] < 0

                    ):

                    # Quantity
                    quantity = int(self.portfolio.cash / self.securities[self.AAPL_symbol].close)

                    # Buy
                    self.market_order(symbol = self.AAPL_symbol, quantity = quantity)

        
        # Else
        else:

            # If 10% and above average price
            if self.securities[self.AAPL_symbol].close > self.portfolio[self.AAPL_symbol].average_price * 1.1:
                
                # #AAPL current price
                AAPL_current = self.securities[self.AAPL_symbol].close

                # #Avearage price that we bought apple at
                Average_AAPL_entry_price = self.portfolio[self.AAPL_symbol].average_price

                # # main string 
                main_string = "AAPL current price: " + str(AAPL_current)+ "AAPL average price: "  + str(Average_AAPL_entry_price )

                self.log(main_string)

                # Sell
                self.market_order(symbol = self.AAPL_symbol, quantity = -self.portfolio[self.AAPL_symbol].quantity)