from AlgorithmImports import *

class BullishStrategy(QCAlgorithm):
    def Initialize(self):
        self.start = self.SetStartDate(2020, 1, 1)
        self.end = self.SetEndDate(2025, 1, 1)
        self.SetCash(5000)  # Starting cash balance
        self.tickers = ["AAPL","NVDA","MSFT","AVGO","CRM","ORCL","CSCO","IBM","ACN","ADBE","NOW","TXN",
        "QCOM","PLTR","INTU","AMD","AMAT","PANW","ADI","MU","INTC","LRCX","ANET","KLAC",
        "CRWD","APH","MSI","SNPS","FTNT","CDNS","ROP","ADSK","WDAY","NXPI","TEL","FICO",
        "CTSH","GLW","IT","MCHP","DELL","MPWR","HPQ","ANSS","KEYS","TYL","HPE","GDDY"
        "TDY","CDW","STX","SMCI","NTAP","ON","VRSN","PTC","TER","TRMB","JBL","FFIV","WDC",
        "ZBRA","GEN","FSLR","AKAM","JNPR","EPAM","SWKS","ENPH"]  # Add more stocks
        self.symbols = []
        self.indicators = {}

        for ticker in self.tickers:
            symbol = self.AddEquity(ticker, Resolution.Daily).Symbol
            self.symbols.append(symbol)
        
         # Store indicators for each symbol
            self.indicators[symbol] = {
                "ema8": self.EMA(symbol, 8, Resolution.Daily),
                "ema21": self.EMA(symbol, 21, Resolution.Daily),
                "ema34": self.EMA(symbol, 34, Resolution.Daily),
                "sma50": self.SMA(symbol, 50, Resolution.Daily),
                "sma100": self.SMA(symbol, 100, Resolution.Daily),
                "sma200": self.SMA(symbol, 200, Resolution.Daily),
                "rsi": self.RSI(symbol, 2, MovingAverageType.Simple, Resolution.Daily),
                "stoch": self.STO(symbol, 8, 3, 3, Resolution.Daily),
            }

    def OnData(self, data):
        for symbol in self.symbols:
            if symbol not in data:
                continue  # Skip if no data for this stock

            price = self.Securities[symbol].Price
            indicators = self.indicators[symbol]

            # Ensure indicators are ready
            if not indicators["ema8"].IsReady or not indicators["sma200"].IsReady:
                continue  

            # Entry conditions
            ema_sma_trend = (
                indicators["ema8"].Current.Value > indicators["ema21"].Current.Value and
                indicators["ema21"].Current.Value > indicators["ema34"].Current.Value and
                indicators["ema34"].Current.Value > indicators["sma50"].Current.Value and
                indicators["sma50"].Current.Value > indicators["sma100"].Current.Value and
                indicators["sma100"].Current.Value > indicators["sma200"].Current.Value
            )

            retracement_stochas = (
                indicators["stoch"].StochK.Current.Value <= 40 and
                indicators["stoch"].StochD.Current.Value <= 40
            )
            retracement_rsi = indicators["rsi"].Current.Value <= 10
            pullback_entry = price <= indicators["ema21"].Current.Value or price <= indicators["ema34"].Current.Value

            # Buy condition
            if ema_sma_trend and retracement_stochas and retracement_rsi and pullback_entry:
                self.SetHoldings(symbol, 0.1)  # Invest 10% of portfolio in each position
            


    def OnEndOfDay(self):
        self.Debug(f"End of day cash: {self.Portfolio.Cash}")
        self.Debug(f"Orders placed {self.SetHoldings}")