import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xgboost as xgb
import seaborn as sns
from sklearn.metrics import mean_squared_error
import streamlit as st

st.set_page_config(page_title="Machine Learning — XGBoost", page_icon="🤖", layout="wide")

df1 = pd.read_csv('data/pdl_1.csv')
df2 = pd.read_csv('data/pdl_2.csv')


def main():
    menu_options = ["Point 1", "Point 2"]
    choix_menu = st.sidebar.selectbox("Machine Learning :", menu_options)
    st.title("🤖 Modélisation prédictive par régression de la consommation")
    st.caption("Sandeep-Singh NIRMAL — BUT Informatique, Université Paris Cité 2023")

    df = df1.copy() if choix_menu == "Point 1" else df2.copy()

    df = df.set_index('timestamp')
    df.index = pd.to_datetime(df.index, utc=True).tz_convert(None)

    color_pal = sns.color_palette()
    plt.style.use('fivethirtyeight')

    # ── Série temporelle ──────────────────────────────────────────────────────
    st.subheader("Série temporelle de consommation")

    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df['value'], '.', color=color_pal[0], markersize=1)
    ax.set_title('Consommation (en kWh)')
    fig.tight_layout()
    st.pyplot(fig)

    # ── Échantillons d'apprentissage et de test ───────────────────────────────
    st.subheader("Échantillons d'apprentissage et de test")

    train = df.loc[df.index < '2023-07-01']
    test  = df.loc[df.index >= '2023-07-01']

    fig, ax = plt.subplots(figsize=(15, 5))
    train.plot(ax=ax, label="Apprentissage", title='Consommation (en kWh)')
    test.plot(ax=ax, label='Test')
    ax.axvline('2023-07-01', color='black', ls='--')
    ax.legend(["Échantillon d'apprentissage", "Échantillon de test"])
    fig.tight_layout()
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(15, 5))
    df.loc[(df.index > '09-01-2023') & (df.index < '09-08-2023')].plot(
        ax=ax, title='Consommation sur une semaine (début septembre 2023)')
    fig.tight_layout()
    st.pyplot(fig)

    st.write(
        "On observe chaque jour un ou deux pics de consommation. "
        "On notera toutefois une consommation quasi nulle le 3 septembre."
    )

    # ── Relation variable / cible ─────────────────────────────────────────────
    st.subheader("Relation entre les variables temporelles et la consommation")

    def create_features(df):
        df = df.copy()
        df['hour']       = df.index.hour
        df['dayofweek']  = df.index.dayofweek
        df['month']      = df.index.month
        df['year']       = df.index.year
        df['dayofyear']  = df.index.dayofyear
        df['dayofmonth'] = df.index.day
        df['weekofyear'] = df.index.isocalendar().week
        return df

    df = create_features(df)

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.boxplot(data=df, x='hour', y='value', ax=ax)
    ax.set_title('Consommation par heure (en kWh)')
    fig.tight_layout()
    st.pyplot(fig)

    st.write(
        "La consommation est quasi nulle entre 19h et 4h du matin. "
        "Elle se stabilise à un niveau constant entre 7h et 16h."
    )

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.boxplot(data=df, x='month', y='value', palette='Blues', ax=ax)
    ax.set_title('Consommation par mois (en kWh)')
    fig.tight_layout()
    st.pyplot(fig)

    st.write(
        "La consommation présente deux pics annuels : un premier en hiver, "
        "lié au chauffage, et un second en été, probablement dû à la climatisation."
    )

    # ── Modèle de régression ──────────────────────────────────────────────────
    st.subheader("Entraînement du modèle XGBoost")

    code = '''reg = xgb.XGBRegressor(
    base_score=0.5, booster='gbtree',
    n_estimators=1000,        # nombre maximum d'arbres
    early_stopping_rounds=50, # arrêt si pas d'amélioration sur 50 itérations
    objective='reg:linear',
    max_depth=3,
    learning_rate=0.01        # faible taux pour limiter le surapprentissage
)
reg.fit(X_train, y_train,
        eval_set=[(X_train, y_train), (X_test, y_test)],
        verbose=100)'''

    st.code(code, language='python')

    train = create_features(train)
    test  = create_features(test)
    FEATURES = ['dayofyear', 'hour', 'dayofweek', 'month', 'year']
    TARGET   = 'value'
    X_train, y_train = train[FEATURES], train[TARGET]
    X_test,  y_test  = test[FEATURES],  test[TARGET]

    reg = xgb.XGBRegressor(
        base_score=0.5, booster='gbtree',
        n_estimators=1000,
        early_stopping_rounds=50,
        objective='reg:linear',
        max_depth=3,
        learning_rate=0.01
    )
    reg.fit(X_train, y_train,
            eval_set=[(X_train, y_train), (X_test, y_test)],
            verbose=100)

    st.write(
        "Le modèle a été configuré pour créer jusqu'à 1 000 arbres de décision. "
        "L'entraînement s'est arrêté anticipativement lorsque l'erreur quadratique moyenne "
        "a cessé de diminuer. Le taux d'apprentissage de 0,01 permet de limiter le surapprentissage."
    )

    # ── Importance des variables ──────────────────────────────────────────────
    st.subheader("Importance des variables")

    fi = pd.DataFrame(
        data=reg.feature_importances_,
        index=reg.feature_names_in_,
        columns=['importance']
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    fi.sort_values('importance').plot(kind='barh', title='Importance des variables', ax=ax)
    fig.tight_layout()
    st.pyplot(fig)

    st.write(
        "L'heure et le jour de la semaine sont les variables les plus déterminantes pour le modèle. "
        "L'année et le jour de l'année ont une influence modérée, tandis que le mois contribue peu. "
        "Ces scores reflètent l'importance relative de chaque variable au sein du modèle global."
    )

    # ── Prévisions ────────────────────────────────────────────────────────────
    st.subheader("Prévisions sur l'échantillon de test")

    test['prediction'] = reg.predict(X_test)
    df = df.merge(test[['prediction']], how='left', left_index=True, right_index=True, suffixes=('', '_test'))

    fig, ax = plt.subplots(figsize=(15, 5))
    df[['value']].plot(ax=ax)
    df['prediction'].plot(ax=ax)
    ax.legend(['Données réelles', 'Prévisions'])
    ax.set_title('Données réelles vs prévisions — série complète')
    fig.tight_layout()
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(15, 5))
    df.loc[(df.index > '09-01-2023') & (df.index < '09-08-2023')]['value'].plot(ax=ax)
    df.loc[(df.index > '09-01-2023') & (df.index < '09-08-2023')]['prediction'].plot(ax=ax, style='-')
    ax.legend(['Données réelles', 'Prévisions'])
    ax.set_title('Prévisions sur une semaine — début septembre 2023')
    fig.tight_layout()
    st.pyplot(fig)

    st.write(
        "Le modèle reproduit globalement la tendance attendue : une consommation relativement stable "
        "en journée et des creux nocturnes. Il reste perfectible, notamment sur les événements atypiques."
    )
    st.write(
        "Une piste d'amélioration serait d'intégrer des indicateurs pour les jours spéciaux "
        "(jours fériés, vacances scolaires), qui influencent significativement la consommation."
    )

    # ── RMSE ──────────────────────────────────────────────────────────────────
    st.subheader("Erreur quadratique moyenne (RMSE)")

    score = np.sqrt(mean_squared_error(test['value'], test['prediction']))
    st.metric("RMSE sur l'échantillon de test", f"{score:.2f} kWh")

    # ── Erreurs de prévision ──────────────────────────────────────────────────
    st.subheader("Jours les moins bien prédits")

    test['error'] = np.abs(test[TARGET] - test['prediction'])
    test['date']  = test.index.date
    top_errors = test.groupby('date')['error'].mean().sort_values(ascending=False).head(10)
    st.dataframe(
        top_errors.reset_index().rename(columns={'date': 'Date', 'error': 'Erreur moyenne (kWh)'}),
        use_container_width=True, hide_index=True
    )

    st.write(
        "Les journées les moins bien prédites se concentrent majoritairement en août 2023, "
        "période où la consommation présente probablement des comportements atypiques."
    )

    # ── Pistes d'amélioration ─────────────────────────────────────────────────
    st.subheader("Pistes d'amélioration")
    st.write(
        "Plusieurs axes peuvent être explorés pour améliorer les performances du modèle :\n\n"
        "- **Validation croisée temporelle** (*time series cross-validation*) pour une évaluation plus robuste.\n"
        "- **Variables exogènes** : données météorologiques, localisation du site, jours fériés et vacances.\n"
        "- **Optimisation des hyperparamètres** via une recherche par grille ou un algorithme bayésien.\n"
        "- **Modèles alternatifs** : Prophet (Meta) ou LSTM pour mieux capturer les tendances longues."
    )


if __name__ == "__main__":
    main()
