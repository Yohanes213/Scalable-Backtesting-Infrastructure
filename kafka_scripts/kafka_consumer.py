from kafka import KafkaConsumer
import json
import sys
import os
import logging
def consume_backtest_request():
    consumer = KafkaConsumer(
        'backend_requests',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest',
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )

    for message in consumer:
        name = message.value['name']
        start_date = message.value['start_date']
        end_date = message.value['end_date']
        strategy = message.value['strategy']
        params = message.value['params']
        start_cash = message.value['start_cash']
        comm = message.value['comm']

        yield name, strategy, start_date, end_date, params, start_cash, comm


def consume_backtest_results():
    consumer = KafkaConsumer(
        'backtest_results',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest',
        # consumer_timeout_ms=30000,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        
    )

    for message in consumer:
        metrics = message.value['metrics']

        return metrics
    
