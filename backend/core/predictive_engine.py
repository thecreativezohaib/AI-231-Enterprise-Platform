import pandas as pd
from prophet import Prophet
import xgboost as xgb
import numpy as np

class PredictiveOperationsEngine:
    def __init__(self):
        self.xgb_model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
        self.is_trained = False

    def predict_capacity_exhaustion(self, historical_data: pd.DataFrame):
        # historical_data requires 'ds' (datetime) and 'y' (metric, e.g., CPU/Memory)
        if len(historical_data) < 10:
            return {"status": "insufficient data"}
        
        m = Prophet(daily_seasonality=True)
        m.fit(historical_data)
        
        future = m.make_future_dataframe(periods=24, freq='H')
        forecast = m.predict(future)
        
        # Check if any future prediction exceeds 95% capacity
        exhaustion_points = forecast[forecast['yhat'] > 95.0]
        if not exhaustion_points.empty:
            return {
                "risk": "HIGH",
                "exhaustion_predicted_at": str(exhaustion_points.iloc[0]['ds']),
                "max_predicted_load": float(exhaustion_points['yhat'].max())
            }
        return {"risk": "LOW", "message": "Capacity stable for next 24 hours"}

    def predict_equipment_failure(self, features: np.ndarray):
        # Features: [temperature, latency, vibration, age]
        if not self.is_trained:
            # Mock training for demonstration
            X_mock = np.random.rand(100, 4) * 100
            y_mock = np.random.randint(0, 2, 100)
            self.xgb_model.fit(X_mock, y_mock)
            self.is_trained = True
            
        prob = self.xgb_model.predict_proba([features])[0][1]
        return {"failure_probability": float(prob)}

predictive_engine = PredictiveOperationsEngine()
