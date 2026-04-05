import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Engie - Analyse de Consommation",
    page_icon="⚡",
    layout="wide"
)

# ── Chargement rapide des données pour les métriques ──────────────────────────
@st.cache_data
def load_data():
    df1 = pd.read_csv('data/pdl_1.csv')
    df2 = pd.read_csv('data/pdl_2.csv')
    df1['timestamp'] = pd.to_datetime(df1['timestamp'], utc=True).dt.tz_convert(None)
    df2['timestamp'] = pd.to_datetime(df2['timestamp'], utc=True).dt.tz_convert(None)
    return df1, df2

df1, df2 = load_data()

# ── En-tête ───────────────────────────────────────────────────────────────────
col_logo, col_titre = st.columns([1, 4])
with col_logo:
    st.image("image/engie.png", width=160)
with col_titre:
    st.title("Application d'Analyse de Consommation Énergétique")

st.divider()

# ── Métriques clés ────────────────────────────────────────────────────────────
st.subheader("Vue d'ensemble des données")

total1 = df1['value'].sum()
total2 = df2['value'].sum()
nb_mesures = len(df1) + len(df2)
date_min = df1['timestamp'].min().strftime("%d/%m/%Y")
date_max = df1['timestamp'].max().strftime("%d/%m/%Y")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Consommation totale — Point 1", f"{total1:,.0f} kWh".replace(",", " "))
m2.metric("Consommation totale — Point 2", f"{total2:,.0f} kWh".replace(",", " "))
m3.metric("Nombre de relevés", f"{nb_mesures:,}".replace(",", " "))
m4.metric("Période couverte", f"{date_min} → {date_max}")

st.divider()

# ── Contexte ──────────────────────────────────────────────────────────────────
st.subheader("Contexte du projet")
st.write(
    "On considère la consommation de **deux points de consommation** appartenant à un même site. "
    "L'objectif est d'effectuer une analyse approfondie de la consommation du site à travers **3 axes analytiques**, "
    "chacun composé d'un graphique et d'un commentaire mettant en évidence une observation pertinente. "
    "Un modèle de **Machine Learning (XGBoost)** est également développé pour prédire la consommation future."
)

# ── Axes d'analyse ────────────────────────────────────────────────────────────
st.subheader("Les axes d'analyse")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.info(
        "**📊 Axe 1 — Comparaison annuelle**\n\n"
        "Comparaison de la consommation mensuelle de **2023 vs 2022** pour identifier les tendances et écarts."
    )
with c2:
    st.info(
        "**🌙 Axe 2 — Consommations nocturnes**\n\n"
        "Analyse de l'évolution des consommations de **nuit sur janvier 2023** "
        "(22h–00h le soir + 00h–06h le matin suivant)."
    )
with c3:
    st.info(
        "**📅 Axe 3 — Profils hebdomadaires**\n\n"
        "Mise en évidence des **profils de consommation hebdomadaire** sur le mois de **février 2023**."
    )
with c4:
    st.success(
        "**🤖 Machine Learning**\n\n"
        "Modélisation prédictive par **régression XGBoost** pour anticiper la consommation énergétique."
    )

st.divider()

# ── Guide de navigation ───────────────────────────────────────────────────────
st.subheader("Navigation")
st.write("Utilisez le **menu latéral gauche** pour accéder aux différentes analyses :")

nav1, nav2 = st.columns(2)
with nav1:
    st.markdown("""
    - **Comparaison 2023 vs 2022** — Axe 1
    - **Évolution janvier 2023** — Axe 2
    - **Profils février 2023** — Axe 3
    """)
with nav2:
    st.markdown("""
    - **Machine Learning** — Modèle prédictif XGBoost
    - **Ressources** — Données brutes
    - **À propos** — Auteur du projet
    """)

st.divider()

# ── Pied de page auteur ───────────────────────────────────────────────────────
col_a, col_b, col_c = st.columns(3)
with col_b:
    st.markdown(
        """
        <div style='text-align: center; color: #888; font-size: 0.85rem; padding: 10px;'>
            Projet réalisé par <strong>Sandeep-Singh NIRMAL</strong><br>
            BUT Informatique — Parcours Data · Université Paris Cité
        </div>
        """,
        unsafe_allow_html=True
    )
