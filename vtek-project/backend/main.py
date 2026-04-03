from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import select, text
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from common.schemas import CarSchema
from backend.ml_service import predict_speed, train_model
from backend.database import get_db, init_db, CarModel, engine
from backend.security import SecurityHeadersMiddleware, AuditLoggingMiddleware, limiter
import pandas as pd


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="VTEK API", lifespan=lifespan)

# --- Supervision sécurité ---
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(AuditLoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)


@app.get("/health", tags=["Supervision"])
def health_check(db: Session = Depends(get_db)):
    """Vérifie la disponibilité du service et la connectivité à la base de données."""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception:
        raise HTTPException(status_code=503, detail="Base de données inaccessible")

@app.get("/cars", response_model=list[CarSchema])
@limiter.limit("60/minute")
def get_cars(request: Request, db: Session = Depends(get_db)):
    """Récupère les données depuis PostgreSQL"""
    cars = db.query(CarModel).all()
    return cars

@app.post("/cars/ingest")
@limiter.limit("10/minute")
def ingest_cars(request: Request, cars: list[CarSchema], db: Session = Depends(get_db)):
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
@limiter.limit("30/minute")
def predict_car_speed(request: Request, car: CarSchema):
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
@limiter.limit("5/minute")
def trigger_training(request: Request, db: Session = Depends(get_db)):
    """Entraîne le modèle sur les données en base"""
    # Lire les données via SQLAlchemy 2.0 (connection explicite, sans session.bind déprécié)
    with engine.connect() as conn:
        df = pd.read_sql(select(CarModel), conn)
    
    if df.empty:
        raise HTTPException(status_code=400, detail="Pas de données en base pour l'entraînement")
        
    score = train_model(df)
    return {"status": "trained", "r2_score": score}