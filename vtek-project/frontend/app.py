import streamlit as st
import pandas as pd
import requests
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Configuration de l'API
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("VTEK - Dashboard Automobile")

# --- BLOC D'ENTRAÎNEMENT (NOUVEAU) ---
# Ce bloc permet d'entraîner le modèle si ce n'est pas encore fait
st.markdown("### Administration du Modèle IA")
col_train, col_status = st.columns([1, 2])
with col_train:
    if st.button("🧠 Entraîner le modèle"):
        try:
            with st.spinner("Entraînement en cours sur les données actuelles..."):
                # Appel à l'endpoint d'entraînement
                res = requests.post(f"{API_URL}/model/train")
                
                if res.status_code == 200:
                    r2_score = res.json().get('r2_score')
                    st.success(f"Modèle entraîné avec succès ! (Précision R²: {r2_score:.4f})")
                else:
                    st.error(f"Erreur d'entraînement : {res.text}")
        except Exception as e:
            st.error(f"Erreur de connexion au backend : {e}")
# --------------------------------------

# 1. Récupération des données
try:
    response = requests.get(f"{API_URL}/cars")
    if response.status_code == 200:
        cars_data = response.json()
        df = pd.DataFrame(cars_data)
    else:
        st.error(f"Erreur API ({response.status_code})")
        df = pd.DataFrame()
except Exception as e:
    st.error(f"Impossible de contacter l'API Backend : {e}")
    df = pd.DataFrame()

if not df.empty:
    # 2. Statistiques
    st.subheader("Statistiques descriptives")
    st.write(df[["power", "weight", "max_speed"]].describe())

    # 3. Matrice de corrélation
    if st.checkbox("Afficher la matrice de corrélation"):
        st.subheader("Analyse de corrélation")
        # Encodage simple pour la visualisation
        df_corr = pd.get_dummies(df, columns=["manufacturer", "fuel_type"], drop_first=True)
        corr = df_corr.corr(numeric_only=True)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

    # 4. Formulaire de prédiction
    st.markdown("---")
    st.subheader("🏎️ Simulateur de Vitesse Max")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        power = st.number_input("Puissance (ch)", 60, 1500, 150)
    with col2:
        weight = st.number_input("Poids (kg)", 500, 3000, 1300)
    with col3:
        aero = st.slider("Aérodynamisme (Cx)", 0.20, 0.45, 0.30)
    
    if st.button("Prédire la vitesse"):
        # Payload factice pour l'exemple (seuls power/weight/aero comptent vraiment pour ce modèle simple)
        payload = {
            "manufacturer": "Unknown", "model": "Unknown", "year": 2024,
            "power": power, "torque": 250, "max_speed": 0, "fuel_efficiency": 5.0,
            "fuel_type": "Gasoline", "doors_number": 5, "weight": weight,
            "aerodynamic_level": aero, "turbo_count": 1, "millage_in_km": 0,
            "zero_to_hundred": 8.0, "transmission_type": "Manual", "is_started": False
        }
        
        try:
            res = requests.post(f"{API_URL}/predict/max_speed", json=payload)
            if res.status_code == 200:
                speed = res.json()['predicted_max_speed']
                st.success(f"🚀 Vitesse estimée : **{speed:.1f} km/h**")
            elif res.status_code == 503:
                st.warning("⚠️ Le modèle n'est pas encore entraîné. Cliquez sur le bouton 'Entraîner le modèle' ci-dessus.")
            else:
                st.error(f"Erreur lors de la prédiction : {res.text}")
        except Exception as e:
            st.error(f"Erreur de connexion : {e}")

else:
    st.info("Aucune donnée disponible. Attendez que l'ETL termine son travail ou vérifiez les logs.")