import joblib
import os
import pandas as pd

class Predictor:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'performance_model.pkl')
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
        else:
            self.model = None

    def predict(self, avg_hours, tasks_completed, missed_deadlines, consistency, sleep_hours):
        if not self.model:
            return 0, 0
        
        data = pd.DataFrame([{
            'avg_hours': avg_hours,
            'tasks_completed': tasks_completed,
            'missed_deadlines': missed_deadlines,
            'consistency': consistency,
            'sleep_hours': sleep_hours
        }])
        
        prediction = self.model.predict(data)[0]
        # Random confidence for simulation (usually between 85-98%)
        import random
        confidence = random.uniform(85, 98)
        
        return round(prediction, 2), round(confidence, 1)
