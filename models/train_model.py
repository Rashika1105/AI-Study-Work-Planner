import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib
import os

def generate_synthetic_data(n_samples=1000):
    np.random.seed(42)
    # Average daily hours (2 - 14)
    avg_hours = np.random.uniform(2, 14, n_samples)
    # Tasks completed (0 - 10)
    tasks_completed = np.random.randint(0, 11, n_samples)
    # Missed deadlines (0 - 5)
    missed_deadlines = np.random.randint(0, 6, n_samples)
    # Consistency rate (0.1 - 1.0)
    consistency = np.random.uniform(0.1, 1.0, n_samples)
    # Sleep hours (4 - 10)
    sleep_hours = np.random.uniform(4, 10, n_samples)
    
    # Target: Performance Score (0 - 100)
    # Logic: More hours, more tasks, higher consistency, more sleep -> higher score
    # More missed deadlines -> lower score
    score = (avg_hours * 5) + (tasks_completed * 4) - (missed_deadlines * 5) + (consistency * 10) + (sleep_hours * 2)
    # Normalize to 0-100 and add some noise
    score = (score - score.min()) / (score.max() - score.min()) * 100
    score += np.random.normal(0, 2, n_samples)
    score = np.clip(score, 0, 100)
    
    df = pd.DataFrame({
        'avg_hours': avg_hours,
        'tasks_completed': tasks_completed,
        'missed_deadlines': missed_deadlines,
        'consistency': consistency,
        'sleep_hours': sleep_hours,
        'performance_score': score
    })
    return df

def train_and_save_model():
    print("Generating synthetic data...")
    df = generate_synthetic_data()
    
    X = df[['avg_hours', 'tasks_completed', 'missed_deadlines', 'consistency', 'sleep_hours']]
    y = df['performance_score']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"Model Mean Absolute Error: {mae:.2f}")
    
    # Ensure directory exists
    model_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)))
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        
    model_path = os.path.join(model_dir, 'performance_model.pkl')
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == '__main__':
    train_and_save_model()
