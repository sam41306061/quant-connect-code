#region imports
from AlgorithmImports import *
from System.Drawing import Color
#endregion

class Benchmark:

    def __init__(self, algo, underlying,  shares = 100, indicators = {}):
        self.algo = algo
        self.underlying = underlying

        self.tradingChart = Chart('Trade Plot')

        self.sqz = Chart('Squeeze')
        self.sqz.AddSeries(Series('No SQZ', SeriesType.Scatter, '', Color.Green, ScatterMarkerSymbol.Circle))
        self.sqz.AddSeries(Series('Low SQZ', SeriesType.Scatter, '', Color.Black, ScatterMarkerSymbol.Circle))
        self.sqz.AddSeries(Series('Mid SQZ', SeriesType.Scatter, '', Color.Red, ScatterMarkerSymbol.Circle))
        self.sqz.AddSeries(Series('High SQZ', SeriesType.Scatter, '', Color.Orange, ScatterMarkerSymbol.Circle))
        
        self.sqz.AddSeries(Series('UP Bull MOM', SeriesType.Bar, '', Color.Aqua))
        self.sqz.AddSeries(Series('DOWN Bull MOM', SeriesType.Bar, '', Color.Blue))
        self.sqz.AddSeries(Series('DOWN Bear MOM', SeriesType.Bar, '', Color.Red))
        self.sqz.AddSeries(Series('UP Bear MOM', SeriesType.Bar, '', Color.Yellow))
        self.algo.AddChart(self.sqz)

        self.tradingChart.AddSeries(Series('Price', SeriesType.Line, '$', Color.White))
        self.algo.AddChart(self.tradingChart)

        self.AddIndicators(indicators)

        self.resample = datetime.min
        self.resamplePeriod = (self.algo.EndDate - self.algo.StartDate) / 2000

    def AddIndicators(self, indicators):
        self.indicators = indicators
        for name, _i in indicators.items():
            self.algo.AddChart(Chart(name))

    def PrintBenchmark(self):
        if self.algo.Time <= self.resample: return

        self.resample = self.algo.Time  + self.resamplePeriod
        self.__PrintIndicators()

    def __PrintIndicators(self):
        ''' Prints the indicators array values to the Trade Plot chart.  '''
        for name, indicator in self.indicators.items():
            if name == 'Squeeze':
                self.__PlotSqueeze(indicator)
            else:
                self.algo.PlotIndicator(name, indicator)

    def __PlotSqueeze(self, indicator):
        if indicator.MomentumHistogramColor() == Color.Aqua:
            self.algo.Plot('Squeeze', 'UP Bull MOM', indicator.Current.Value)
        elif indicator.MomentumHistogramColor() == Color.Blue:
            self.algo.Plot('Squeeze', 'DOWN Bull MOM', indicator.Current.Value)
        elif indicator.MomentumHistogramColor() == Color.Red:
            self.algo.Plot('Squeeze', 'DOWN Bear MOM', indicator.Current.Value)
        elif indicator.MomentumHistogramColor() == Color.Yellow:
            self.algo.Plot('Squeeze', 'UP Bear MOM', indicator.Current.Value)

        if indicator.Squeeze == 0:
            self.algo.Plot('Squeeze', 'No SQZ', 0)
        elif indicator.Squeeze == 1:
            self.algo.Plot('Squeeze', 'Low SQZ', 0)
        elif indicator.Squeeze == 2:
            self.algo.Plot('Squeeze', 'Mid SQZ', 0)
        elif indicator.Squeeze == 3:
            self.algo.Plot('Squeeze', 'High SQZ', 0)
