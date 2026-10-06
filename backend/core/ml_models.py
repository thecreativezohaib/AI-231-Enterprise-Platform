import numpy as np
from sklearn.ensemble import IsolationForest
import pickle
import os

class AnomalyDetector:
    def __init__(self, model_path="anomaly_model.pkl"):
        self.model_path = model_path
        self.model = IsolationForest(contamination=0.05, random_state=42)
        self.is_trained = False

    def train(self, data: np.ndarray):
        # data shape: (n_samples, n_features)
        self.model.fit(data)
        self.is_trained = True
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
            
    def load(self):
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            self.is_trained = True

    def predict(self, features: list):
        if not self.is_trained:
            self.load()
        if not self.is_trained:
            return 1 # Normal by default if no model
        # features: [cpu_usage, memory_usage, temperature, network_latency]
        pred = self.model.predict([features])
        # IF returns 1 for normal, -1 for anomaly.
        return pred[0]

anomaly_detector = AnomalyDetector()
