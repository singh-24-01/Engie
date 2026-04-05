import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Analyses", page_icon="🔍", layout="wide")

@st.cache_data
def load_data():
    df1 = pd.read_csv('data/pdl_1.csv')
    df2 = pd.read_csv('data/pdl_2.csv')
    df1['timestamp'] = pd.to_datetime(df1['timestamp'], utc=True).dt.tz_convert(None)
    df2['timestamp'] = pd.to_datetime(df2['timestamp'], utc=True).dt.tz_convert(None)
    return df1, df2

df1, df2 = load_data()

MOIS = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']

st.title("🔍 Analyses de consommation")
st.caption("Sandeep-Singh NIRMAL — BUT Informatique, Université Paris Cité 2023")

point = st.sidebar.selectbox("Point de consommation", ["Point 1 & 2", "Point 1", "Point 2"])

tab1, tab2, tab3 = st.tabs(["📊 Comparaison 2022 vs 2023", "🌙 Consommations nocturnes — Janvier", "📅 Profils hebdomadaires — Février"])


# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — Comparaison annuelle
# ════════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Comparaison de la consommation mensuelle — 2023 vs 2022")

    for df in [df1, df2]:
        df['month'] = df['timestamp'].dt.month
        df['year']  = df['timestamp'].dt.year

    def monthly(df, year):
        return df[df['year'] == year].groupby('month')['value'].sum()

    m1_22, m1_23 = monthly(df1, 2022), monthly(df1, 2023)
    m2_22, m2_23 = monthly(df2, 2022), monthly(df2, 2023)

    def show_axe1(m22, m23, label):
        delta = (m23.sum() - m22.sum()) / m22.sum() * 100
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total 2022", f"{m22.sum():,.0f} kWh".replace(",", " "))
        c2.metric("Total 2023", f"{m23.sum():,.0f} kWh".replace(",", " "), delta=f"{delta:+.1f}%")
        c3.metric("Mois de pointe 2022", MOIS[m22.idxmax() - 1])
        c4.metric("Mois de pointe 2023", MOIS[m23.idxmax() - 1])

        fig, ax = plt.subplots(figsize=(11, 4))
        ax.plot(m22.index, m22.values, marker='o', label='2022', color='#1565C0', linewidth=2)
        ax.plot(m23.index, m23.values, marker='s', label='2023', color='#00B050', linewidth=2)
        ax.set_xticks(range(1, 13)); ax.set_xticklabels(MOIS)
        ax.set_ylabel('Consommation totale (kWh)')
        ax.set_title(f'Comparaison mensuelle — {label}')
        ax.legend(); ax.grid(True, alpha=0.3)
        fig.tight_layout()
        st.pyplot(fig)

        # Variation %
        delta_vals = ((m23 - m22) / m22 * 100).values
        fig2, ax2 = plt.subplots(figsize=(11, 3))
        colors = ['#00B050' if v > 0 else '#C62828' for v in delta_vals]
        ax2.bar(MOIS[:len(delta_vals)], delta_vals, color=colors)
        ax2.axhline(0, color='white', linewidth=0.8)
        ax2.set_ylabel('Variation (%)'); ax2.set_title(f'Variation 2022 → 2023 — {label}')
        ax2.grid(True, axis='y', alpha=0.3)
        fig2.tight_layout()
        st.pyplot(fig2)

    if point in ("Point 1 & 2", "Point 1"):
        show_axe1(m1_22, m1_23, "Point 1")
        st.info("On consomme globalement plus en 2022 qu'en 2023, sauf en septembre et à partir de mi-octobre.")

    if point == "Point 1 & 2":
        st.divider()

    if point in ("Point 1 & 2", "Point 2"):
        show_axe1(m2_22, m2_23, "Point 2")
        st.info("Le Point 2 suit la même tendance que le Point 1 — seule l'échelle de consommation diffère.")


# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — Consommations nocturnes
# ════════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Évolution des consommations nocturnes — Janvier 2023")
    st.write("Une **nuit** = relevés du jour J de 22h à 00h + du jour J+1 de 00h à 06h.")

    def night_jan(df):
        df_jan = df[(df['timestamp'].dt.year == 2023) & (df['timestamp'].dt.month == 1)]
        df_night = df_jan[(df_jan['timestamp'].dt.hour >= 22) | (df_jan['timestamp'].dt.hour < 6)]
        return df_night.groupby(df_jan['timestamp'].dt.day)['value'].sum()

    n1, n2 = night_jan(df1), night_jan(df2)

    def show_axe2(series_list, labels, colors):
        # Métriques
        for s, lbl in zip(series_list, labels):
            c1, c2, c3, c4 = st.columns(4)
            c1.metric(f"Total nocturne — {lbl}", f"{s.sum():,.1f} kWh".replace(",", " "))
            c2.metric(f"Nuit max — {lbl}", f"Jour {s.idxmax()} ({s.max():.1f} kWh)")
            c3.metric(f"Nuit min — {lbl}", f"Jour {s.idxmin()} ({s.min():.1f} kWh)")
            c4.metric(f"Moyenne — {lbl}", f"{s.mean():.1f} kWh/nuit")

        fig, ax = plt.subplots(figsize=(12, 5))
        for s, lbl, col in zip(series_list, labels, colors):
            ax.plot(s.index, s.values, marker='o', label=lbl, color=col, linewidth=2)

        if len(series_list) > 1 and 10 in n2.index:
            ax.annotate(f"Pic : {n2[10]:.1f} kWh", xy=(10, n2[10]),
                        xytext=(12, n2[10] - 5),
                        arrowprops=dict(arrowstyle='->', color='#C62828'),
                        fontsize=9, color='#C62828')
        if 24 in series_list[0].index:
            ax.annotate("Chute 24 jan.", xy=(24, series_list[0][24]),
                        xytext=(20, series_list[0][24] + 8),
                        arrowprops=dict(arrowstyle='->', color='#1565C0'),
                        fontsize=9, color='#1565C0')

        ax.set_xlabel('Jour du mois'); ax.set_ylabel('Consommation nocturne (kWh)')
        ax.set_title('Consommation nocturne — Janvier 2023')
        ax.legend(); ax.grid(True, alpha=0.3)
        fig.tight_layout()
        st.pyplot(fig)

        # Boxplot
        fig2, ax2 = plt.subplots(figsize=(7, 4))
        bp = ax2.boxplot([s.values for s in series_list], labels=labels, patch_artist=True)
        for patch, col in zip(bp['boxes'], colors):
            patch.set_facecolor(col); patch.set_alpha(0.6)
        ax2.set_ylabel('kWh'); ax2.set_title('Distribution nocturne')
        ax2.grid(True, axis='y', alpha=0.3)
        fig2.tight_layout()
        st.pyplot(fig2)

    if point == "Point 1 & 2":
        show_axe2([n1, n2], ['Point 1', 'Point 2'], ['#1565C0', '#00B050'])
        st.info("Les deux points suivent la même tendance. Chute brutale le 24 janvier. Pic exceptionnel du Point 2 le 10 janvier (≈ 150 kWh).")
    elif point == "Point 1":
        show_axe2([n1], ['Point 1'], ['#1565C0'])
    elif point == "Point 2":
        show_axe2([n2], ['Point 2'], ['#00B050'])


# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — Profils hebdomadaires
# ════════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Profils de consommation hebdomadaires — Février 2023")

    def weekly_profiles(df):
        df = df.copy()
        df['week_number'] = df['timestamp'].apply(lambda x: x.isocalendar()[1])
        df_feb = df[(df['timestamp'].dt.year == 2023) & (df['timestamp'].dt.month == 2)]
        return df_feb.groupby('week_number')['value'].mean()

    p1, p2 = weekly_profiles(df1), weekly_profiles(df2)
    week_labels = {w: f"S{i+1} (sem.{w})" for i, w in enumerate(sorted(p1.index))}

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Semaines analysées", len(p1))
    c2.metric("Semaine la plus active", week_labels[p1.idxmax()], f"{p1.max():.3f} kWh")
    c3.metric("Semaine la plus calme", week_labels[p1.idxmin()], f"{p1.min():.3f} kWh")
    c4.metric("Écart max–min", f"{p1.max() - p1.min():.3f} kWh")

    def show_axe3(series_list, labels, colors, markers):
        fig, ax = plt.subplots(figsize=(10, 5))
        for s, lbl, col, mk in zip(series_list, labels, colors, markers):
            ax.plot(s.index, s.values, label=lbl, color=col, marker=mk, linewidth=2.5, markersize=8, ls='--')
        ax.set_xticks(sorted(p1.index))
        ax.set_xticklabels([week_labels[w] for w in sorted(p1.index)])
        ax.set_ylabel('Consommation moyenne (kWh)')
        ax.set_title('Profils hebdomadaires — Février 2023')
        ax.legend(); ax.grid(True, alpha=0.3)
        fig.tight_layout()
        st.pyplot(fig)

    if point == "Point 1 & 2":
        show_axe3([p1, p2], ['Point 1', 'Point 2'], ['#1565C0', '#00B050'], ['D', 'o'])
        st.info("Les profils des deux points se superposent parfaitement — les habitudes de consommation sont identiques.")
    elif point == "Point 1":
        show_axe3([p1], ['Point 1'], ['#1565C0'], ['D'])
    elif point == "Point 2":
        show_axe3([p2], ['Point 2'], ['#00B050'], ['o'])

    st.divider()
    st.subheader("Tableau de synthèse")
    table = pd.DataFrame({
        'Semaine': [week_labels[w] for w in sorted(p1.index)],
        'Moy. Point 1 (kWh)': [f"{v:.3f}" for v in p1.sort_index().values],
        'Moy. Point 2 (kWh)': [f"{v:.3f}" for v in p2.sort_index().values],
        'Écart P1–P2': [f"{abs(a-b):.3f}" for a, b in zip(p1.sort_index().values, p2.sort_index().values)],
    })
    st.dataframe(table, use_container_width=True, hide_index=True)

    st.subheader("Profil horaire moyen — Février 2023")
    hourly = df1[(df1['timestamp'].dt.year == 2023) & (df1['timestamp'].dt.month == 2)].groupby(df1['timestamp'].dt.hour)['value'].mean()
    fig3, ax3 = plt.subplots(figsize=(11, 4))
    ax3.fill_between(hourly.index, hourly.values, alpha=0.35, color='#1565C0')
    ax3.plot(hourly.index, hourly.values, color='#1565C0', linewidth=2)
    ax3.set_xticks(range(0, 24)); ax3.set_xlabel('Heure'); ax3.set_ylabel('kWh moyen')
    ax3.set_title('Profil horaire moyen — Février 2023 — Point 1')
    ax3.grid(True, alpha=0.3)
    fig3.tight_layout()
    st.pyplot(fig3)
