from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# L'URL doit être fournie via variable d'environnement — aucun fallback avec credentials
DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Définition de la table SQL à partir de votre modèle métier
class CarModel(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    manufacturer = Column(String)
    model = Column(String)
    year = Column(Integer)
    power = Column(Integer)
    torque = Column(Integer)
    max_speed = Column(Integer)
    fuel_efficiency = Column(Float)
    fuel_type = Column(String)
    doors_number = Column(Integer)
    weight = Column(Integer)
    aerodynamic_level = Column(Float)
    turbo_count = Column(Integer)
    millage_in_km = Column(Integer)
    zero_to_hundred = Column(Float)
    transmission_type = Column(String)
    is_started = Column(Boolean, default=False)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()