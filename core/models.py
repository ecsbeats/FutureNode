from django.contrib.auth.models import User
from django.db import models


class Wallet(models.Model):
    crypto_balance = models.IntegerField(default=0, null=True)
    cash_balance = models.IntegerField(default=0, null=True)

    def __repr__(self):
        return "<Crypto Balance: %s, Cash Balance: %s>"\
            .format(self.crypto_balance, self.cash_balance)
