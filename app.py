import streamlit as st
import pandas as pd
from dashboard.visualisation import afficher_dashboard
from form.formulaire import afficher_formulaire

# --- Configuration de la page ---
st.set_page_config(page_title="Univers des données", layout="wide")
st.title("🏘️ Bienvenue dans l'univers des données")
st.markdown("Explorez, téléchargez, visualisez et évaluez.")

# --- Menu de navigation ---
menu = st.sidebar.radio("Navigation", [
    "Scraper les données (nettoyées)",
    "Télécharger les données brutes",
    "Visualiser le dashboard",
    "Donner votre avis"
])

# --- Fichiers de données ---
fichiers_bruts = {
    "Appartements à louer": "data/expat_dkr_app_a_louer.xlsx",
    "Appartements meublés": "data/expat_dkr_app_meubles.xlsx",
    "Terrains à vendre": "data/expat_dkr_terrain_a_vendre.xlsx"
}

fichiers_nettoyes = {
    "Appartements meublés": "data/expat_dkr_app_meubles.csv",
    "Terrains à vendre": "data/expat_dkr_terrain_a_vendre.csv",
    "Appartements à louer": "data/expat_dkr_app_a_louer.csv"
}

# --- Scraper les données (à partir des fichiers existants) ---
if menu == "Scraper les données (nettoyées)":
    st.header("Extraire les données disponibles")

    categorie = st.selectbox("Choisissez une catégorie :", list(fichiers_nettoyes.keys()))
    nb_lignes = st.slider("Nombre d'annonces à extraire :", min_value=1, max_value=100, value=10)

    fichier = fichiers_nettoyes[categorie]

    try:
        df = pd.read_csv(fichier)
        extrait = df.head(nb_lignes)

        st.download_button(
            label=f"⬇️ Télécharger les {nb_lignes} premières annonces",
            data=extrait.to_csv(index=False).encode("utf-8"),
            file_name=f"{categorie.lower().replace(' ', '_')}_{nb_lignes}_annonces.csv",
            mime="text/csv"
        )
    except FileNotFoundError:
        st.error(f"Le fichier {fichier} est introuvable. Lancez `run_scraper.py` depuis votre machine pour le générer.")

# --- Téléchargement des données brutes ---
elif menu == "Télécharger les données brutes":
    st.header("Téléchargement des données brutes")
    st.markdown("Téléchargez les fichiers originaux au format `.csv` extraits avec Web Scraper.")
    for titre, chemin in fichiers_bruts.items():
        df = pd.read_excel(chemin)
        st.download_button(
            label=f"Télécharger : {titre}",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name=chemin.replace("data/", "").replace(".xlsx", ".csv"),
            mime="text/csv"
        )

# --- Visualisation Dashboard ---
elif menu == "Visualiser le dashboard":
    st.header("Dashboard des données nettoyées")
    choix = st.selectbox("Sélectionnez une catégorie :", list(fichiers_nettoyes.keys()))
    df = pd.read_csv(fichiers_nettoyes[choix])
    afficher_dashboard(df, choix)

# --- Évaluation de l'application ---
elif menu == "Donner votre avis":
    st.header("Donnez votre avis")
    afficher_formulaire()
