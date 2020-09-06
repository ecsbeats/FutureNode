# Predicts bitcoin in real time
from core.wallet import balance
import numpy as np
import pandas as pd
import time
import threading
from sklearn.svm import SVR


class PredictEngine:
    def __init__(self):
        self.current_entries = []
        self.predicted_entries = []
        self.loaded_register = []
        self.creating_entries = False
        self.running = False
        self.accepting_stream = False

    def run(self, prediction_offset=5):
        self.running = True
        self.creating_entries = True
        prediction_offset *= 2
        entries_thread = threading.Thread(target=self.create_entries)
        entries_thread.start()
        while self.running:
            if len(self.current_entries) >= prediction_offset:
                self.load_register(self.current_entries, prediction_offset)
                self.predict(prediction_offset)
                self.current_entries = []

    def stop(self):
        self.running = False
        self.creating_entries = False
        self.accepting_stream = False

    def reset(self):
        self.__init__()

    def predict(self, prediction_offset):
        while self.running:
            if len(self.loaded_register) >= prediction_offset:
                X = np.array(self.loaded_register)
                y = np.roll(X, prediction_offset / 2)
                k = SVR(kernal='rbf', C=1e3, gamma=0.00001)
                k.fit(X, y)

    def load_register(self, load, prediction_offset):
        filtered_load = load[-prediction_offset:]
        self.loaded_register = filtered_load

    def create_entries(self):
        try:
            while self.creating_entries:
                current_price = balance.get_price()
                self.current_entries.append(current_price)
                time.sleep(1)
        finally:
            print("[INFO] Create Entries thread has ended")


test_engine = PredictEngine()
test_engine.run()
