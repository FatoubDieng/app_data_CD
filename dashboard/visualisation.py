import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re

def nettoyer_colonne_numerique(serie):
    def nettoyer_valeur(val):
        if pd.isna(val):
            return np.nan
        val = str(val)
        val = re.sub(r'[^\d.,]', '', val)     # Supprimer tout sauf chiffres, , et .
        val = val.replace(',', '.')           # Convertir virgule en point
        try:
            return float(val)
        except:
            return np.nan
    return serie.apply(nettoyer_valeur)

def afficher_dashboard(df: pd.DataFrame, titre: str):
    st.subheader(f"📊 Dashboard - {titre}")

    colonnes_numeriques = {
        "prix": "Distribution des prix (F CFA)",
        "superficie": "Distribution des superficies (m²)"
    }

    colonnes_valides = []

    for col, label in colonnes_numeriques.items():
        if col in df.columns:
            cleaned_col = nettoyer_colonne_numerique(df[col])
            if cleaned_col.notna().sum() > 0:
                df[col] = cleaned_col
                colonnes_valides.append((col, label))
            else:
                st.warning(f" `La colonne '{col}' ne contient pas de données numériques valides.")

    if colonnes_valides:
        st.write("Visualisations")
        cols = st.columns(len(colonnes_valides))
        for (col, label), c in zip(colonnes_valides, cols):
            with c:
                fig, ax = plt.subplots()
                df[col].dropna().plot.hist(bins=20, ax=ax, color="skyblue", edgecolor="black")
                ax.set_title(label)
                ax.set_xlabel(f"{col.capitalize()} ({'F CFA' if col == 'prix' else 'm²'})")
                ax.set_ylabel("Fréquence")
                fig.tight_layout()
                st.pyplot(fig)
    else:
        st.info("Aucune colonne exploitable pour les graphiques.")

    st.write("# Aperçu des données")
    st.dataframe(df.head(50))
