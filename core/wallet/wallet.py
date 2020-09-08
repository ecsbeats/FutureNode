# Wallet operations
from . import balance


def save(wallet):
    wallet.save()


def sell(wallet):
    crypto_balance = wallet.crypto_balance
    cash_balance = balance.crypto_to_cash(crypto_balance)
    wallet.crypto_balance = 0
    wallet.cash_balance += cash_balance

def buy(wallet):
    cash_balance = wallet.cash_balance
    crypto_balance = balance.cash_to_crypto(cash_balance)
    wallet.cash_balance = 0
    wallet.crypto_balance += crypto_balance

def send_cash(wallet, amount=0):
    wallet.cash_balance += amount


def send_crypto(wallet, amount=0):
    wallet.crypto_balance += amount
