from django.contrib.auth.models import User
from django.db import models


class Wallet(models.Model):
    id = models.IntegerField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto_balance = models.IntegerField(null=True)
    cash_balance = models.IntegerField(null=True)

    def __repr__(self):
        return "<Owner: %s, Crypto Balance: %s, Cash Balance: %s>"\
            .format(self.owner, self.crypto_balance, self.cash_balance)
