# Bitcoin price retrieval and conversions
import requests
import pandas as pd
import numpy as np
import os
import threading
from pathlib import Path
import time

API_URL = "https://api.coindesk.com/v1/bpi/currentprice.json"
FOLDER = BASE_DIR = Path(__file__).resolve().parent

# Demo Vars (Comment out if using real-time)
cycle_value = 0
df = pd.read_csv(os.path.join(FOLDER, 'demo.csv'))
prices = np.array(df.drop(['AlsoPrice'], 1))
prices = prices.reshape(len(prices))
cycling = False


def get_price():
    req = requests.get(API_URL).json()
    raw_rate = req['bpi']['USD']['rate']
    formatted_rate = float(raw_rate.replace(",", ""))
    return formatted_rate


def get_data_price():
    global cycle_value
    global prices
    try:
        return prices[cycle_value]
    except IndexError:
        cycle_value = 0
        return get_data_price()


def price_cycle():
    global cycle_value
    global prices
    global cycling
    cycling = True
    while cycling:
        if cycle_value >= len(prices):
            cycle_value = 0
        cycle_value += 1
        time.sleep(1)


def stop():
    global cycling
    cycling = False


def cash_to_crypto(balance):
    price = get_data_price()
    return balance / price


def crypto_to_cash(balance):
    price = get_data_price()
    return balance * price


# Create thread for demo db cycle (Comment out if doing real-time)
cycle_thread = threading.Thread(target=price_cycle)
cycle_thread.start()
