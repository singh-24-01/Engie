import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Statistiques Globales", page_icon="📈", layout="wide")

@st.cache_data
def load_data():
    df1 = pd.read_csv('data/pdl_1.csv')
    df2 = pd.read_csv('data/pdl_2.csv')
    df1['timestamp'] = pd.to_datetime(df1['timestamp'], utc=True).dt.tz_convert(None)
    df2['timestamp'] = pd.to_datetime(df2['timestamp'], utc=True).dt.tz_convert(None)
    df1['point'] = 'Point 1'
    df2['point'] = 'Point 2'
    return df1, df2

df1, df2 = load_data()
df_all = pd.concat([df1, df2], ignore_index=True)

st.title("📈 Statistiques Globales")
st.caption("Sandeep-Singh NIRMAL — BUT Informatique, Université Paris Cité 2023")
st.write("Vue synthétique de l'ensemble des données des deux points de consommation.")

st.divider()

# ── KPIs globaux ──────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Point 1", f"{df1['value'].sum():,.0f} kWh".replace(",", " "))
k2.metric("Total Point 2", f"{df2['value'].sum():,.0f} kWh".replace(",", " "))
k3.metric("Moy. horaire P1", f"{df1['value'].mean():.3f} kWh")
k4.metric("Moy. horaire P2", f"{df2['value'].mean():.3f} kWh")
k5.metric("Relevés totaux", f"{len(df_all):,}".replace(",", " "))

st.divider()

# ── Consommation mensuelle cumulée ────────────────────────────────────────────
st.subheader("Consommation mensuelle cumulée (2022–2023)")

df_all['year_month'] = df_all['timestamp'].dt.to_period('M')
monthly = df_all.groupby(['year_month', 'point'])['value'].sum().unstack('point')
monthly.index = monthly.index.astype(str)

fig1, ax1 = plt.subplots(figsize=(13, 5))
ax1.bar(monthly.index, monthly.get('Point 1', 0), label='Point 1',
        color='#1565C0', alpha=0.8)
ax1.bar(monthly.index, monthly.get('Point 2', 0), label='Point 2',
        bottom=monthly.get('Point 1', 0), color='#00B050', alpha=0.8)
ax1.set_xlabel('Mois')
ax1.set_ylabel('Consommation (kWh)')
ax1.set_title('Consommation mensuelle cumulée — Point 1 + Point 2')
plt.xticks(rotation=45, ha='right', fontsize=8)
ax1.legend()
ax1.grid(True, axis='y', alpha=0.3)
fig1.tight_layout()
st.pyplot(fig1)

st.divider()

# ── Profil horaire moyen ───────────────────────────────────────────────────────
st.subheader("Profil horaire moyen sur toute la période")

col_l, col_r = st.columns(2)

with col_l:
    h1 = df1.groupby(df1['timestamp'].dt.hour)['value'].mean()
    fig2, ax2 = plt.subplots(figsize=(7, 4))
    ax2.fill_between(h1.index, h1.values, alpha=0.35, color='#1565C0')
    ax2.plot(h1.index, h1.values, color='#1565C0', linewidth=2)
    ax2.set_xticks(range(0, 24, 2))
    ax2.set_xlabel('Heure')
    ax2.set_ylabel('kWh moyen')
    ax2.set_title('Profil horaire — Point 1')
    ax2.grid(True, alpha=0.3)
    fig2.tight_layout()
    st.pyplot(fig2)

with col_r:
    h2 = df2.groupby(df2['timestamp'].dt.hour)['value'].mean()
    fig3, ax3 = plt.subplots(figsize=(7, 4))
    ax3.fill_between(h2.index, h2.values, alpha=0.35, color='#00B050')
    ax3.plot(h2.index, h2.values, color='#00B050', linewidth=2)
    ax3.set_xticks(range(0, 24, 2))
    ax3.set_xlabel('Heure')
    ax3.set_ylabel('kWh moyen')
    ax3.set_title('Profil horaire — Point 2')
    ax3.grid(True, alpha=0.3)
    fig3.tight_layout()
    st.pyplot(fig3)

st.divider()

# ── Consommation par jour de la semaine ───────────────────────────────────────
st.subheader("Consommation moyenne par jour de la semaine")

JOURS = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

d1 = df1.groupby(df1['timestamp'].dt.dayofweek)['value'].mean()
d2 = df2.groupby(df2['timestamp'].dt.dayofweek)['value'].mean()

fig4, ax4 = plt.subplots(figsize=(10, 4))
x = range(7)
width = 0.35
ax4.bar([i - width/2 for i in x], d1.values, width, label='Point 1', color='#1565C0', alpha=0.8)
ax4.bar([i + width/2 for i in x], d2.values, width, label='Point 2', color='#00B050', alpha=0.8)
ax4.set_xticks(range(7))
ax4.set_xticklabels(JOURS)
ax4.set_ylabel('Consommation moyenne (kWh)')
ax4.set_title('Consommation moyenne par jour de la semaine')
ax4.legend()
ax4.grid(True, axis='y', alpha=0.3)
fig4.tight_layout()
st.pyplot(fig4)

st.divider()

# ── Tableau statistiques descriptives ─────────────────────────────────────────
st.subheader("Statistiques descriptives")

desc1 = df1['value'].describe().rename("Point 1")
desc2 = df2['value'].describe().rename("Point 2")
desc = pd.concat([desc1, desc2], axis=1)
desc.index = ['Nombre', 'Moyenne', 'Écart-type', 'Min', '25%', 'Médiane', '75%', 'Max']
st.dataframe(desc.style.format("{:.3f}"), use_container_width=True)
