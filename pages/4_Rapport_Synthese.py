import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Rapport de synthèse", page_icon="📋", layout="wide")

@st.cache_data
def load_data():
    df1 = pd.read_csv('data/pdl_1.csv')
    df2 = pd.read_csv('data/pdl_2.csv')
    df1['timestamp'] = pd.to_datetime(df1['timestamp'], utc=True).dt.tz_convert(None)
    df2['timestamp'] = pd.to_datetime(df2['timestamp'], utc=True).dt.tz_convert(None)
    return df1, df2

df1, df2 = load_data()

st.title("📋 Rapport de synthèse")
st.caption("Sandeep-Singh NIRMAL — BUT Informatique, Université Paris Cité 2023")
st.write("Ce rapport résume l'ensemble des observations et conclusions issues des trois axes d'analyse.")

st.divider()

# ── KPIs globaux ──────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Consommation totale P1", f"{df1['value'].sum():,.0f} kWh".replace(",", " "))
k2.metric("Consommation totale P2", f"{df2['value'].sum():,.0f} kWh".replace(",", " "))
k3.metric("Période couverte", f"{df1['timestamp'].min().strftime('%d/%m/%Y')} → {df1['timestamp'].max().strftime('%d/%m/%Y')}")
k4.metric("Fréquence des relevés", "Toutes les 10 min")

st.divider()

# ── Axe 1 ─────────────────────────────────────────────────────────────────────
st.subheader("Axe 1 — Comparaison annuelle 2022 vs 2023")

df1['year']  = df1['timestamp'].dt.year
df1['month'] = df1['timestamp'].dt.month

m1_22 = df1[df1['year'] == 2022].groupby('month')['value'].sum()
m1_23 = df1[df1['year'] == 2023].groupby('month')['value'].sum()
variation = ((m1_23 - m1_22) / m1_22 * 100).mean()

col_txt, col_chart = st.columns([2, 3])
with col_txt:
    st.markdown("""
    **Observations clés :**
    - La consommation 2022 est globalement **supérieure** à celle de 2023.
    - Exception notable : **septembre** et la **fin d'année** (à partir de mi-octobre) où 2023 dépasse 2022.
    - Les deux points de consommation suivent la **même tendance saisonnière**.
    - La variation annuelle moyenne entre 2022 et 2023 est de **{:.1f} %**.
    """.format(variation))
with col_chart:
    MOIS = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(m1_22.index, m1_22.values, marker='o', label='2022', color='#1565C0', linewidth=2)
    ax.plot(m1_23.index, m1_23.values, marker='s', label='2023', color='#00B050', linewidth=2)
    ax.set_xticks(range(1, 13)); ax.set_xticklabels(MOIS, fontsize=8)
    ax.set_ylabel('kWh'); ax.legend(); ax.grid(True, alpha=0.3)
    ax.set_title('Point 1 — 2022 vs 2023')
    fig.tight_layout()
    st.pyplot(fig)

st.divider()

# ── Axe 2 ─────────────────────────────────────────────────────────────────────
st.subheader("Axe 2 — Consommations nocturnes — Janvier 2023")

df1_jan = df1[(df1['year'] == 2023) & (df1['month'] == 1)]
n1 = df1_jan[(df1_jan['timestamp'].dt.hour >= 22) | (df1_jan['timestamp'].dt.hour < 6)].groupby(df1_jan['timestamp'].dt.day)['value'].sum()

col_txt2, col_chart2 = st.columns([2, 3])
with col_txt2:
    st.markdown(f"""
    **Observations clés :**
    - Les deux points présentent une tendance nocturne **similaire** tout au long du mois.
    - **Chute brutale le 24 janvier** sur les deux points — probablement une interruption d'activité.
    - Le **Point 2 présente un pic exceptionnel le 10 janvier** (~150 kWh), retombant le lendemain.
    - La consommation nocturne moyenne du Point 1 est de **{n1.mean():.1f} kWh/nuit**.
    """)
with col_chart2:
    fig2, ax2 = plt.subplots(figsize=(8, 3))
    ax2.plot(n1.index, n1.values, marker='o', color='#1565C0', linewidth=2)
    if 24 in n1.index:
        ax2.axvline(24, color='#C62828', ls='--', alpha=0.7, label='Chute 24 jan.')
    ax2.set_xlabel('Jour'); ax2.set_ylabel('kWh'); ax2.legend()
    ax2.set_title('Consommation nocturne — Point 1 — Janvier 2023')
    ax2.grid(True, alpha=0.3)
    fig2.tight_layout()
    st.pyplot(fig2)

st.divider()

# ── Axe 3 ─────────────────────────────────────────────────────────────────────
st.subheader("Axe 3 — Profils hebdomadaires — Février 2023")

df1_feb = df1[(df1['year'] == 2023) & (df1['month'] == 2)].copy()
df1_feb['week'] = df1_feb['timestamp'].apply(lambda x: x.isocalendar()[1])
p1 = df1_feb.groupby('week')['value'].mean()
week_labels = [f"S{i+1}" for i in range(len(p1))]

col_txt3, col_chart3 = st.columns([2, 3])
with col_txt3:
    st.markdown(f"""
    **Observations clés :**
    - Les profils de consommation hebdomadaires du Point 1 et du Point 2 sont **strictement identiques**.
    - La consommation varie légèrement d'une semaine à l'autre ({p1.min():.3f} → {p1.max():.3f} kWh en moyenne).
    - Ce profil uniforme suggère des **habitudes de consommation stables** et régulières sur le site.
    """)
with col_chart3:
    fig3, ax3 = plt.subplots(figsize=(8, 3))
    ax3.plot(range(len(p1)), p1.values, marker='D', color='#1565C0', linewidth=2.5, ls='--')
    ax3.set_xticks(range(len(p1))); ax3.set_xticklabels(week_labels)
    ax3.set_ylabel('kWh moyen'); ax3.set_title('Profils hebdomadaires — Point 1')
    ax3.grid(True, alpha=0.3)
    fig3.tight_layout()
    st.pyplot(fig3)

st.divider()

# ── Machine Learning ──────────────────────────────────────────────────────────
st.subheader("Machine Learning — Modèle XGBoost")

col_ml1, col_ml2 = st.columns(2)
with col_ml1:
    st.markdown("""
    **Approche :**
    - Modèle de régression **XGBoost** entraîné sur les données 2022 – juin 2023.
    - Variables utilisées : heure, jour de la semaine, mois, année, jour de l'année.
    - Arrêt anticipé (*early stopping*) pour éviter le surapprentissage.

    **Résultats :**
    - L'heure et le jour de la semaine sont les **variables les plus importantes**.
    - Le modèle reproduit fidèlement les **cycles journaliers** de consommation.
    - Les jours les moins bien prédits se concentrent en **août 2023** (comportements atypiques).
    """)
with col_ml2:
    st.markdown("""
    **Pistes d'amélioration :**
    - Intégrer des **données météorologiques** (température, ensoleillement).
    - Ajouter des indicateurs pour les **jours fériés et vacances scolaires**.
    - Utiliser une **validation croisée temporelle** pour une évaluation plus robuste.
    - Explorer des modèles alternatifs : **Prophet** (Meta) ou **LSTM** (réseaux de neurones).
    """)

st.divider()

# ── Conclusion ────────────────────────────────────────────────────────────────
st.subheader("Conclusion générale")
st.success(
    "Les deux points de consommation présentent des comportements très similaires, avec des tendances "
    "saisonnières marquées. La consommation est significativement plus élevée en 2022 qu'en 2023, "
    "et les pics de consommation se produisent en hiver et en été. "
    "Le modèle XGBoost parvient à capturer la majorité des patterns temporels, "
    "mais pourrait être amélioré par l'intégration de variables contextuelles supplémentaires."
)

st.markdown(
    """
    <div style='text-align: center; color: #888; font-size: 0.85rem; padding: 20px;'>
        Sandeep-Singh NIRMAL · BUT Informatique — Parcours Data · Université Paris Cité · 2023
    </div>
    """,
    unsafe_allow_html=True
)
