import streamlit as st
import pandas as pd
import requests
import seaborn as sns
import matplotlib.pyplot as plt
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("VTEK - Dashboard Automobile")

# 1. Récupération des données
try:
    response = requests.get(f"{API_URL}/cars")
    cars_data = response.json()
    df = pd.DataFrame(cars_data)
except:
    st.error("Impossible de contacter l'API Backend")
    df = pd.DataFrame()

if not df.empty:
    # 2. Statistiques (remplace vos print())
    st.subheader("Statistiques descriptives")
    st.write(df[["power", "weight", "max_speed"]].describe())

    # 3. Matrice de corrélation (Votre code seaborn adapté)
    if st.checkbox("Afficher la matrice de corrélation"):
        st.subheader("Analyse de corrélation")
        df_corr = pd.get_dummies(df, columns=["manufacturer", "fuel_type"], drop_first=True)
        corr = df_corr.corr(numeric_only=True)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

    # 4. Formulaire de prédiction (Appelle l'API)
    st.subheader("Simulateur de Vitesse Max")
    col1, col2 = st.columns(2)
    with col1:
        power = st.number_input("Puissance (ch)", 60, 1500, 150)
        weight = st.number_input("Poids (kg)", 500, 3000, 1300)
    
    if st.button("Prédire la vitesse"):
        # On construit un payload factice pour l'appel API
        # (Dans un vrai cas, on remplirait tout le formulaire)
        payload = {
            "manufacturer": "Unknown", "model": "Unknown", "year": 2024,
            "power": power, "torque": 250, "max_speed": 0, "fuel_efficiency": 5.0,
            "fuel_type": "Gasoline", "doors_number": 5, "weight": weight,
            "aerodynamic_level": 0.3, "turbo_count": 1, "millage_in_km": 0,
            "zero_to_hundred": 8.0, "transmission_type": "Manual", "is_started": False
        }
        res = requests.post(f"{API_URL}/predict/max_speed", json=payload)
        if res.status_code == 200:
            speed = res.json()['predicted_max_speed']
            st.success(f"Vitesse estimée : {speed:.2f} km/h")
        else:
            st.error("Erreur lors de la prédiction")
else:
    st.warning("Aucune donnée disponible. L'ETL a-t-il tourné ?")