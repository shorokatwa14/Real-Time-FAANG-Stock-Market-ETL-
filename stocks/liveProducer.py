import yfinance as yf
import time
import json
from confluent_kafka import Producer

def getStocksLive(tickers):
    while True:
        for ticker in tickers:
            data = yf.Ticker(ticker).history(period='1d', interval='1m')
            row = data.iloc[-1]
            row_data = {
                'ticker': ticker,
                'date': str(row.name.date()),
                'open': row['Open'],
                'high': row['High'],
                'low': row['Low'],
                'close': row['Close'],
                'volume': row['Volume']
            }
            json_data = json.dumps(row_data, indent=4)
            producer.produce('stock_data_topic', key=ticker, value=json_data, callback=delivery_report)
            producer.poll(1)  # Poll to handle delivery reports
        time.sleep(60)


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Set up Kafka producer
producer = Producer({
    'bootstrap.servers': 'localhost:9092',  # Update with your Kafka broker address
    'client.id': 'stock-producer'
})

faang = ['AAPL', 'AMZN', 'META', 'GOOGL', 'NFLX']

getStocksLive(faang)
