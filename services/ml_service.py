import os
import joblib
import pandas as pd
from train_model import MODEL_PATH, generate_educational_dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None

def evaluate_model_metrics():
    df = generate_educational_dataset()
    X = df[["sleep", "stress", "energy", "social"]]
    y = df["category"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = load_model()
    if not model:
        return None
    
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, preds, average='weighted', zero_division=0)
    cm = confusion_matrix(y_test, preds)
    
    return {
        "accuracy": acc,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "confusion_matrix": cm,
        "feature_importances": dict(zip(["sleep", "stress", "energy", "social"], model.feature_importances_))
    }
