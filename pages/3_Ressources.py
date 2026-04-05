import pandas as pd
import streamlit as st

st.set_page_config(page_title="Ressources — Données brutes", page_icon="🗄️", layout="wide")

@st.cache_data
def load_data():
    df1 = pd.read_csv('data/pdl_1.csv')
    df2 = pd.read_csv('data/pdl_2.csv')
    df1['timestamp'] = pd.to_datetime(df1['timestamp'], utc=True).dt.tz_convert(None)
    df2['timestamp'] = pd.to_datetime(df2['timestamp'], utc=True).dt.tz_convert(None)
    return df1, df2

df1, df2 = load_data()

st.title("🗄️ Bases de données — Données brutes")
st.caption("Sandeep-Singh NIRMAL — BUT Informatique, Université Paris Cité 2023")
st.image("image/engie.png", width=160)

st.divider()

# ── Statistiques globales ─────────────────────────────────────────────────────
st.subheader("Statistiques globales")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Relevés — Point 1", f"{len(df1):,}".replace(",", " "))
c2.metric("Relevés — Point 2", f"{len(df2):,}".replace(",", " "))
c3.metric("Période", f"{df1['timestamp'].min().strftime('%d/%m/%Y')} → {df1['timestamp'].max().strftime('%d/%m/%Y')}")
c4.metric("Fréquence", "10 minutes")

st.divider()

# ── Filtres ───────────────────────────────────────────────────────────────────
st.subheader("Exploration des données")

col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    point = st.selectbox("Point de consommation", ["Point 1", "Point 2"])
with col_f2:
    annee = st.selectbox("Année", [2022, 2023])
with col_f3:
    mois_options = {
        'Tous': None, 'Janvier': 1, 'Février': 2, 'Mars': 3, 'Avril': 4,
        'Mai': 5, 'Juin': 6, 'Juillet': 7, 'Août': 8,
        'Septembre': 9, 'Octobre': 10, 'Novembre': 11, 'Décembre': 12
    }
    mois_label = st.selectbox("Mois", list(mois_options.keys()))
    mois_val = mois_options[mois_label]

df_selected = df1.copy() if point == "Point 1" else df2.copy()
df_selected = df_selected[df_selected['timestamp'].dt.year == annee]
if mois_val:
    df_selected = df_selected[df_selected['timestamp'].dt.month == mois_val]

st.caption(f"{len(df_selected):,} relevés affichés".replace(",", " "))

# Statistiques descriptives
sc1, sc2, sc3, sc4 = st.columns(4)
sc1.metric("Consommation totale", f"{df_selected['value'].sum():,.1f} kWh".replace(",", " "))
sc2.metric("Moyenne", f"{df_selected['value'].mean():.3f} kWh")
sc3.metric("Maximum", f"{df_selected['value'].max():.3f} kWh")
sc4.metric("Minimum", f"{df_selected['value'].min():.3f} kWh")

st.dataframe(
    df_selected.rename(columns={'timestamp': 'Horodatage', 'value': 'Valeur (kWh)'}),
    use_container_width=True,
    hide_index=True,
    height=400
)

# ── Téléchargement ────────────────────────────────────────────────────────────
st.divider()
csv = df_selected.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Télécharger la sélection (CSV)",
    data=csv,
    file_name=f"pdl_{'1' if point == 'Point 1' else '2'}_{annee}{'_' + str(mois_val) if mois_val else ''}.csv",
    mime='text/csv'
)
