# Predicts bitcoin in real time
from core.wallet import balance
import numpy as np
import pandas as pd
from scipy import integrate
import time
import threading
from sklearn.svm import SVR


class PredictEngine:
    def __init__(self):
        self.current_entries = []
        self.predicted_entries = []
        self.entries = []
        self.loaded_register = []
        self.creating_entries = False
        self.running = False
        self.accepting_stream = False
        self.logging = False

    def start(self, prediction_offset=5, logging=False):
        self.logging = logging
        self.engine_thread = threading.Thread(target=self.run, args=(prediction_offset,))
        self.engine_thread.start()

    def run(self, prediction_offset=5):
        self.running = True
        self.creating_entries = True
        prediction_offset *= 2
        entries_thread = threading.Thread(target=self.create_entries)
        entries_thread.start()
        self.log("[INFO] Create Entries thread has started")
        prediction_thread = threading.Thread(target=self.predict, args=(prediction_offset,))
        prediction_thread.start()
        self.log("[INFO] Prediction thread has started")
        while self.running:
            if len(self.current_entries) >= prediction_offset:
                self.load_register(self.current_entries, prediction_offset)
                self.current_entries = []
    
    def log(self, message):
        if self.logging:
            print(message)

    def stop(self):
        self.running = False
        self.creating_entries = False
        self.accepting_stream = False

    def reset(self):
        self.__init__()

    def predict(self, prediction_offset):
        while self.running:
            if len(self.loaded_register) >= prediction_offset:
                self.log("[INFO] Calculating Prediction")
                X = np.array(self.loaded_register)[:int(prediction_offset / 2)]
                X = X.reshape(-1, 1)
                y = np.roll(X.reshape(1, -1)[0], int(prediction_offset / 2) * -1)
                k = SVR(kernel='rbf', C=1e3, gamma=0.00001)
                self.log("[INFO] Training SVM")
                k.fit(X, y)
                prediction = k.predict([X[-1]])
                self.log("[INFO] Prediction DONE")
                self.predicted_entries.append(prediction)
                self.loaded_register = []

    def load_register(self, load, prediction_offset):
        filtered_load = load[-prediction_offset:]
        self.loaded_register = filtered_load

    def create_entries(self):
        try:
            while self.creating_entries:
                self.log("[INFO] Request has started")
                current_price = balance.get_data_price()
                self.current_entries.append(current_price)
                self.entries.append(current_price)
                self.log("[INFO] Waiting for next request")
                time.sleep(2)
            self.log("[INFO] Create Entries thread has ended")
        finally:
            self.log("[INFO] Create Entries thread has ended")
