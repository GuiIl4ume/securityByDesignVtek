from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Récupération de l'URL de la DB depuis les variables d'environnement (Security by Design)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://vtek_user:secure_password@db:5432/vtek_db")

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