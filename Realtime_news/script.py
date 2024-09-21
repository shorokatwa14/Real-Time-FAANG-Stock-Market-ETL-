# -*- coding: utf-8 -*-

import yfinance as yf
import requests
import json
import csv
import schedule
import time
import glob
from datetime import datetime

def download_faang_news(faang_tickers):
    for ticker in faang_tickers:
        stock = yf.Ticker(ticker)
        news = stock.news
        with open('{}_news.json'.format(ticker), 'w', encoding='utf-8') as f:
            json.dump(news, f, indent=4, ensure_ascii=False)

def convert_json_to_csv():
    json_files = glob.glob('*.json')
    
    # Adding a timestamp column
    with open('/home/student/flume/input/merged_news1.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'relatedTickers', 'publisher', 'date']  # Added 'date'
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for json_file in json_files:
            with open(json_file, 'r', encoding='utf-8') as f:
                news_data = json.load(f)

                # Get the current date
                current_date = datetime.now().strftime('%Y-%m-%d')

                for article in news_data:
                    if isinstance(article, dict):
                        writer.writerow({
                            'title': article.get('title', ''),
                            'relatedTickers': ','.join(article.get('relatedTickers', [])),
                            'publisher': article.get('publisher', ''),
                            'date': current_date  # Add current date to each row
                        })
    print("done")

# القائمة الرئيسية لأسهم FAANG
faang = ['AAPL', 'AMZN', 'META', 'GOOGL', 'NFLX']
def job():
    download_faang_news(faang)
    convert_json_to_csv()

schedule.every(5).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(300)  # Wait for 5 minutes before checking again

