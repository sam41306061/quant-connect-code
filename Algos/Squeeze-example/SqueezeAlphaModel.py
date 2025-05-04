#region imports
from AlgorithmImports import *
from TTMSqueezePro import TTMSqueezePro
from SqueezeAlphaModel import SqueezeAlphaModel
from Benchmark import Benchmark
# endregion

class AddAlphaModelAlgorithm(QCAlgorithm):
    def Initialize(self):
        ''' Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''
        # self.SetStartDate(2012, 2, 4)  # Set Start Date
        # self.SetEndDate(2020, 31, 7)    # Set End Date
        self.SetStartDate(2021, 7, 1)  # Set Start Date
        self.SetEndDate(2021, 9, 1)    # Set End Date

        self.SetCash(100_000)          # Set Strategy Cash
        # Set settings and account setup
        self.UniverseSettings.Resolution = Resolution.Daily
        self.UniverseSettings.FillForward = False
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin) # Set InteractiveBrokers Brokerage model

        # Main variables
        self.ticker = "TSLA"
        self.benchmark = Benchmark(self, self.ticker)
        self.option = Symbol.Create(self.ticker, SecurityType.Option, Market.USA, f"?{self.ticker}")

        # Squeeze model
        self.SetAlpha(SqueezeAlphaModel(self, self.ticker, self.option))
