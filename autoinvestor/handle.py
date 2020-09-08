from core.wallet import balance
from core.wallet import wallet
from autoinvestor.prediction import PredictEngine
from autoinvestor.logic import data_handler
from core.models import Wallet
import threading
import time

class Main:
    def __init__(self):
        self.wallet_id = None
        self.entries = []
        self.predicted_entry = None
        self.running = False
        self.wallet = None

    def run(self, prediction_offset=2):
        self.running = True
        self.engine = PredictEngine()
        self.engine.start(prediction_offset=prediction_offset)
        print("Initializing...")
        time.sleep(5)
        run_thread = threading.Thread(target=self.running_thread)
        run_thread.start()

    def stop(self):
        self.running = False
        self.engine.stop()

    def get_info(self):
        return {"cash_balance": self.wallet.cash_balance, "crypto_balance": self.wallet.crypto_balance, "last_5_entries": self.engine.entries[-5:]}

    def running_thread(self):
        while self.running == True:
            time.sleep(3)
            self.predicted_entry = self.engine.predicted_entries[-1]
            if self.predicted_entry is not None:
                self.handle_code(data_handler(self.engine.entries, self.engine.predicted_entries[-1]))

            else:
                self.handle_code(data_handler(self.engine.entries))

    def handle_code(self, code):
        if code == -1:
            wallet.buy(self.wallet)
            wallet.save(self.wallet)
        elif code == 1:
            wallet.sell(self.wallet)
            wallet.save(self.wallet)
        else:
            wallet.save(self.wallet)
            pass
    def create_wallet(self):
        new_wallet = Wallet()
        self.wallet_id = new_wallet.id
        self.wallet = new_wallet
        wallet.send_crypto(self.wallet, 1)
        self.wallet.save()

mc = Main()
mc.create_wallet()
mt = threading.Thread(target=mc.run)
mt.start()
time.sleep(5)
print("Starting cycle")
while True:
    time.sleep(10)
    print(mc.get_info())
