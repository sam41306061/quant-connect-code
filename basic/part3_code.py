# region imports
from AlgorithmImports import *
# endregion

class RetrospectiveRedJackal(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2023, 1, 6)  # Set Start Date
        self.SetEndDate(2023, 6, 6)
        self.SetCash(100000)  # Set Strategy Cash
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.SelectionFilter)
        self.UniverseSettings.Leverage=2
        #self.SetSecurityInitializer(lambda x: x.SetFeeModel(ConstantFeeModel(0)))

    def SelectionFilter(self, coarse):
        sortedvol = sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)
        filtered=[x.Symbol for x in sortedvol if x.Price>50]
        return filtered[:10]

    def OnSecuritiesChanged(self, changes):
        self.changes=changes
        self.Log(f"Onsecuritieschanged({self.Time}):: {changes}")

        for security in changes.RemovedSecurities:
            if security.Invested:
                self.Liquidate(security.Symbol)
        
        for security in changes.AddedSecurities:
            if not security.Invested:
                self.SetHoldings(security.Symbol,0.12)