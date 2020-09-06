# Bitcoin price retrieval and conversions
import requests

API_URL = "https://api.coindesk.com/v1/bpi/currentprice.json"


def get_price():
    req = requests.get(API_URL).json()
    raw_rate = req['bpi']['USD']['rate']
    formatted_rate = float(raw_rate.replace(",", ""))
    return formatted_rate


def cash_to_crypto(balance):
    price = get_price()
    return balance / price


def crypto_to_cash(balance):
    price = get_price()
    return balance * price
