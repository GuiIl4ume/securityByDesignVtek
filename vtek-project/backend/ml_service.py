import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

# On simule un modèle global pour l'exemple
_model = None

def train_model(df: pd.DataFrame):
    global _model
    feature_cols = [
        "power", "torque", "weight", "aerodynamic_level", 
        "turbo_count", "millage_in_km", "zero_to_hundred"
    ]
    X = df[feature_cols]
    y = df["max_speed"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Sauvegarde du modèle (Persistence)
    joblib.dump(model, "car_speed_model.pkl")
    _model = model
    return model.score(X_test, y_test)

def predict_speed(features: list):
    global _model
    if _model is None:
        try:
            _model = joblib.load("car_speed_model.pkl")
        except:
            return None
    return _model.predict([features])[0]