from __future__ import (absolute_import, division, print_function, unicode_literals)
import datetime
import os.path
import backtrader as bt


class MacdStrategy(bt.Strategy):

    params = (
        ('fast_period', 12),
        ('slow_period', 26),
        ('signal_period', 9),
        ('comm', 0.0),
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None

        self.macd = bt.indicators.MACD(self.datas[0], period_me1=self.params.fast_period, 
                                       period_me2=self.params.slow_period, 
                                       period_signal=self.params.signal_period)

    def notify_order(self, order):

        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('Buy created Price: %.2f, Cost: %.2f, Commission: %.2f'%
                     (order.executed.price,
                      order.executed.value,
                      order.executed.comm))
                
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log('Sell created Price: %.2f, Cost: %.2f, Commission: %.2f'%
                     (order.executed.price,
                      order.executed.value,
                      order.executed.comm))
                
                self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.order('Order Cancled/margin/rejected')
            self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log(f'TRADE PROFIT, GROSS {trade.pnl}, NET {trade.pnlcomm}')

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])
        if self.order:
            return

        if not self.position:
            if self.macd.macd[0] > self.macd.signal[0]:
                self.log('Buy Create, %.2f' % self.dataclose[0])
                self.order = self.buy()
        else:
            if self.macd.macd[0] < self.macd.signal[0]:
                self.log('Sell Create, %.2f' % self.dataclose[0])
                self.order = self.sell()

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MacdStrategy, fast_period=12, slow_period=26, signal_period=9, comm=0.001)
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