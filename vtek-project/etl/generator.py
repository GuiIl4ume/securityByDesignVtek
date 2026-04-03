import requests
import time
import os
import numpy as np
from random import randint, uniform, choice
from common.constants import MODELS_PER_BRANDS, MODEL_SPECS
from common.schemas import CarSchema

# Récupération de l'URL de l'API depuis les variables d'environnement Docker
API_URL = os.getenv("API_URL", "http://backend:8000")

def generate_car_data() -> dict:
    """Génère un dictionnaire représentant une voiture aléatoire"""
    manufacturer = choice(list(MODELS_PER_BRANDS.keys()))
    model = choice(MODELS_PER_BRANDS[manufacturer])
    spec = MODEL_SPECS[model]

    # Année réaliste
    year = randint(1998, 2025)

    # Puissance réaliste par modèle
    power = randint(*spec["power"])
    # Légère tendance à la hausse de puissance avec les années
    power = int(power * (1 + (year - 2010) * 0.006))

    # Poids réaliste avec petite variance
    mean_weight = (spec["weight"][0] + spec["weight"][1]) / 2
    weight = int(np.random.normal(mean_weight, 60))
    weight = min(max(weight, spec["weight"][0]), spec["weight"][1])

    # Type de carburant
    fuel_type = choice(spec["fuel_types"])

    # Aérodynamisme (Cx)
    aerodynamic_level = round(uniform(*spec["cx"]), 3)

    # Couple réaliste lié à la puissance
    if fuel_type == "Diesel":
        torque = int(power * uniform(1.4, 1.8))
    else:
        torque = int(power * uniform(1.1, 1.4))

    # Consommation
    if fuel_type == "Gasoline":
        fuel_efficiency = round(5.5 + (weight / 1000) * 2.2, 1)
    elif fuel_type == "Diesel":
        fuel_efficiency = round(4.3 + (weight / 1000) * 1.9, 1)
    elif fuel_type == "Electric":
        # kWh/100 km équivalent
        fuel_efficiency = round(15 + (weight / 1000) * 4, 1)
    else:  # Hybrid
        fuel_efficiency = round(4.5 + (weight / 1000) * 1.8, 1)

    # Vitesse max réaliste
    max_speed = int(150 + power * 0.45 - aerodynamic_level * 80)
    max_speed = min(max_speed, 480)

    # 0–100 réaliste
    power_to_weight = power / weight
    zero_to_hundred = round(9.5 - power_to_weight * 140, 2)
    zero_to_hundred = max(zero_to_hundred, 2.3)

    # Turbo
    if fuel_type in ("Electric",):
        turbo_count = 0
    elif fuel_type == "Diesel":
        turbo_count = 1 if power < 250 else 2
    else:  # essence / hybrid
        if power < 120:
            turbo_count = 0
        elif power < 250:
            turbo_count = 1
        else:
            turbo_count = randint(1, 3)

    # Kilométrage
    age = 2024 - year
    if age > 0:
        millage_in_km = int(max(0, np.random.normal(age * 15000, 5000)))
    else:
        millage_in_km = 0

    # Transmission
    if manufacturer in ("Ferrari", "Bugatti", "Koenigsegg"):
        transmission_type = choice(["Automatic"])
    else:
        transmission_type = choice(["Manual", "Automatic"])

    # Portes
    if manufacturer in ("Ferrari", "Bugatti", "Koenigsegg"):
        doors_number = 2
    else:
        doors_number = choice([3, 5])

    return {
        "manufacturer": manufacturer,
        "model": model,
        "year": year,
        "power": power,
        "torque": torque,
        "max_speed": max_speed,
        "fuel_efficiency": fuel_efficiency,
        "fuel_type": fuel_type,
        "doors_number": doors_number,
        "weight": weight,
        "aerodynamic_level": aerodynamic_level,
        "turbo_count": turbo_count,
        "millage_in_km": millage_in_km,
        "zero_to_hundred": zero_to_hundred,
        "transmission_type": transmission_type,
        "is_started": False
    }

def run_etl_job():
    print("⏳ Attente du démarrage du backend...")
    time.sleep(5)  # Petit délai pour laisser le temps au backend de démarrer

    print("🚀 Démarrage de la génération de données...")
    
    # Génération d'un lot de 100 voitures
    data_batch = [generate_car_data() for _ in range(100)]
    
    try:
        # Envoi des données au backend via l'API (timeout 30s)
        response = requests.post(f"{API_URL}/cars/ingest", json=data_batch, timeout=30)
        if response.status_code == 200:
            print(f"✅ Succès : {len(data_batch)} véhicules insérés via l'API.")
        else:
            print(f"❌ Erreur API : {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Erreur de connexion au backend : {e}")

if __name__ == "__main__":
    run_etl_job()