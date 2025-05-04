# region imports
from AlgorithmImports import *
# endregion

class MeasuredYellowGreenLemur(QCAlgorithm):

    def initialize(self):

        # Set Start Date
        self.set_start_date(2022, 12, 9)

        # Set Strategy Cash
        self.set_cash(100000)

        # Add AAPL
        add_AAPL = self.add_equity("AAPL", Resolution.Daily)

        # Get AAPL symbol
        self.AAPL_symbol = add_AAPL.symbol

        # Create global list to store AAPL data
        self.AAPL_data = []

    def on_data(self, data: Slice):

        # Store AAPL close price
        self.AAPL_data.append(self.securities[self.AAPL_symbol].close)

    