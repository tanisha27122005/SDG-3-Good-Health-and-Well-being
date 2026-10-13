import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "wellness_model.joblib")

def generate_educational_dataset(n_samples=1000):
    np.random.seed(42)
    sleep = np.random.normal(7.0, 1.2, n_samples).clip(3.0, 12.0)
    stress = np.random.randint(1, 11, n_samples)
    energy = np.random.randint(1, 11, n_samples)
    social = np.random.randint(1, 11, n_samples)
    
    score_metric = (sleep * 0.4) - (stress * 0.5) + (energy * 0.4) + (social * 0.3)
    categories = []
    for val in score_metric:
        if val < 2.0:
            categories.append(0)
        elif val < 5.5:
            categories.append(1)
        else:
            categories.append(2)
            
    df = pd.DataFrame({
        "sleep": sleep,
        "stress": stress,
        "energy": energy,
        "social": social,
        "category": categories
    })
    return df

def train_and_save_model():
    os.makedirs(MODEL_DIR, exist_ok=True)
    df = generate_educational_dataset()
    
    X = df[["sleep", "stress", "energy", "social"]]
    y = df["category"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Model Training Complete. Educational Test Accuracy: {acc:.4f}")
    
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_and_save_model()
