from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from common.schemas import CarSchema
from backend.ml_service import predict_speed, train_model
from backend.database import get_db, init_db, CarModel, engine
import pandas as pd


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="VTEK API", lifespan=lifespan)

@app.get("/cars", response_model=list[CarSchema])
def get_cars(db: Session = Depends(get_db)):
    """Récupère les données depuis PostgreSQL"""
    cars = db.query(CarModel).all()
    return cars

@app.post("/cars/ingest")
def ingest_cars(cars: list[CarSchema], db: Session = Depends(get_db)):
    """Endpoint ETL : insère les données en base"""
    try:
        new_cars = [CarModel(**car.model_dump()) for car in cars]
        db.add_all(new_cars)
        db.commit()
        return {"status": "success", "count": len(cars)}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erreur lors de l'ingestion des données")

@app.post("/predict/max_speed")
def predict_car_speed(car: CarSchema):
    """Prédiction ML (inchangé)"""
    features = [
        car.power, car.torque, car.weight, car.aerodynamic_level,
        car.turbo_count, car.millage_in_km, car.zero_to_hundred
    ]
    prediction = predict_speed(features)
    if prediction is None:
        raise HTTPException(status_code=503, detail="Modèle non entraîné")
    return {"predicted_max_speed": prediction}

@app.post("/model/train")
def trigger_training(db: Session = Depends(get_db)):
    """Entraîne le modèle sur les données en base"""
    # Lire les données via SQLAlchemy 2.0 (connection explicite, sans session.bind déprécié)
    with engine.connect() as conn:
        df = pd.read_sql(select(CarModel), conn)
    
    if df.empty:
        raise HTTPException(status_code=400, detail="Pas de données en base pour l'entraînement")
        
    score = train_model(df)
    return {"status": "trained", "r2_score": score}