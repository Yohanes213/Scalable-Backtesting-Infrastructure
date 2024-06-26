from __future__ import (absolute_import, division, print_function, unicode_literals)
import datetime
import os.path
import backtrader as bt

class RsiStrategy(bt.Strategy):

    params = (
        ('rsi_period', 14),
        ('oversold', 30),
        ('overbought', 70),
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.rsi = bt.indicators.RelativeStrengthIndex(period=self.params.rsi_period)
        self.order = None
        self.buyprice = None
        self.dataclose = self.datas[0].close

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        
        if order.status in [order.Completed]:
            
            if order.isbuy():
                self.log('Buy created Price: %.2f, Cost: %.2f'%
                     (order.executed.price,
                      order.executed.value))
                
                self.buyprice = order.executed.price
            else:
                self.log('Sell created Price: %.2f, Cost: %.2f'%
                     (order.executed.price,
                      order.executed.value))
                self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.order('Order Cancled/margin/rejected')
            self.order = None

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])
        if not self.position:
            if self.rsi < self.params.oversold:
                self.log('Buy Create, %.2f' % self.dataclose[0])
                self.buy()

        else:
            if self.rsi > self.params.overbought:
                self.log('Sell Create, %.2f' % self.dataclose[0])
                self.sell()


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(RsiStrategy, rsi_period=15, oversold=30, overbought=70)
    datapath = 'data/BTC-USD.csv'
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2023, 6, 18),
        todate=datetime.datetime(2024, 6, 18),
        reverse=False
    )
    cerebro.adddata(data)
    cerebro.broker.setcash(100000)
    print(f"Starting Portfolio Value: {cerebro.broker.getvalue()}")
    cerebro.run()
    print(f"Ending Portfolio Value: {cerebro.broker.getvalue()}")
