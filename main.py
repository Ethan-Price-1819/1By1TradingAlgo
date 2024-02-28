# region imports
from AlgorithmImports import *
# endregion

class MeasuredMagentaCobra(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2022, 1, 15)
        self.SetEndDate(2022, 10, 15)
        self.SetCash(10000)
        spy = self.AddEquity("SPY",Resolution.Daily)
        spy.SetDataNormalizationMode(DataNormalizationMode.Raw)
        self.spy = spy.Symbol
        self.SetBenchmark("SPY")

        self.entryPrice = 0
        self.period = timedelta(1)
        self.nextEntryTime = self.Time

    def OnData(self, data):
        if not self.spy in data:
            return
        price = data[self.spy].Close

        if not self.Portfolio.Invested:
            if self.nextEntryTime <= self.Time:
                self.SetHoldings(self.spy,.1)
                self.Log("BUY SPY @" + str(price))
                self.entryPrice = price
        elif self.entryPrice * 1.01 < price or self.entryPrice * .99 > price:
            self.Liquidate()
            self.Log("SELL SPY @" + str(price))
            self.nextEntryTime = self.Time + self.period
