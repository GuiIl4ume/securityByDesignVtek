import pandas as pd
# --- MODIFICATION ICI : On importe RandomForest au lieu de LinearRegression ---
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os

_model = None
MODEL_PATH = "car_speed_model.pkl"

def train_model(df: pd.DataFrame):
    global _model
    feature_cols = [
        "power", "torque", "weight", "aerodynamic_level", 
        "turbo_count", "millage_in_km", "zero_to_hundred"
    ]
    X = df[feature_cols]
    y = df["max_speed"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # --- MODIFICATION ICI : Utilisation d'un modèle plus puissant ---
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    joblib.dump(model, MODEL_PATH)
    _model = model
    
    # Le score R² devrait être bien meilleur (proche de 0.90 ou 0.95)
    return model.score(X_test, y_test)

def predict_speed(features: list):
    global _model
    if _model is None:
        if os.path.exists(MODEL_PATH):
            try:
                _model = joblib.load(MODEL_PATH)
            except:
                return None
        else:
            return None
    
    # RandomForest attend un tableau 2D, features est une liste
    return _model.predict([features])[0]