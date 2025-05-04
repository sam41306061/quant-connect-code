# region imports
from AlgorithmImports import *
# endregion

class StopLossHandler:
    def __init__(self, algorithm: QCAlgorithm, symbol: Symbol):

        self.algorithm = algorithm
        self.symbol = symbol
        self.stop_ticket = None
        self.trailing_active = False
    
    def set_stop_loss(self, entry: float, stop_distance: 0.20):
        """
        Places a hard stop-loss based on entry price and stop distance
        """
        stop_price = entry - stop_distance
        quanitiy = self.algorithm.portfolio[symbol].quantity
        
        if self.quanitiy.close > self.stop_price:
            self.market_order(symbol, quanitiy = -self.portfolio[symbol].quanity)


    def remove_stop(self):
        if self.stop_ticket:
            self.algorithm.Transactions.CancelOrder(self.stop_ticket.OrderId)
            self.algorithm.Debug("Stop-loss removed")
            self.stop_ticket = None
            self.trailing_active = False
        


