# region imports
from AlgorithmImports import *
# endregion

# region imports
from AlgorithmImports import *
# endregion

class StopLossManager:
    def __init__(self, algorithm: QCAlgorithm, symbol: Symbol):
        self.algorithm = algorithm
        self.symbol = symbol
        self.stop_ticket = None
        self.trailing_active = False
        self.trailing_buffer = 0.3  # e.g., ATR or fixed value below current price

    def set_stop_loss(self, entry_price: float, stop_distance: float):
        """
        Places a hard stop-loss based on entry price and stop distance
        """
        stop_price = entry_price - stop_distance
        quantity = self.algorithm.portfolio[self.symbol].Quantity

        if self.stop_ticket:
            self.algorithm.Transactions.CancelOrder(self.stop_ticket.OrderId)

        self.stop_ticket = self.algorithm.StopLossManager(self.symbol, -quantity, stop_price)
        self.algorithm.Debug(f"Stop-loss placed at {stop_price}")

    def activate_trailing_stop(self, buffer: float):
        """
        Switch to trailing stop mode (e.g., after breakeven)
        """
        self.trailing_active = True
        self.trailing_buffer = buffer

    def update_trailing_stop(self):
        """
        Updates stop-loss to trail below highest price
        """
        if not self.trailing_active or self.stop_ticket is None:
            return

        quantity = self.algorithm.Portfolio[self.symbol].Quantity
        current_price = self.algorithm.Securities[self.symbol].Price
        new_stop_price = current_price - self.trailing_buffer

        # Only update if new stop is higher than the old one
        if new_stop_price > self.stop_ticket.Get(OrderField.StopPrice):
            # Cancel and replace stop
            self.algorithm.Transactions.CancelOrder(self.stop_ticket.OrderId)
            self.stop_ticket = self.algorithm.StopMarketOrder(self.symbol, -quantity, new_stop_price)
            self.algorithm.Debug(f"Trailing stop updated to {new_stop_price}")

    def remove_stop(self):
        if self.stop_ticket:
            self.algorithm.Transactions.CancelOrder(self.stop_ticket.OrderId)
            self.algorithm.Debug("Stop-loss removed")
            self.stop_ticket = None
            self.trailing_active = False
