# Application Engie — Analyse de Consommation Énergétique

**Auteur :** Sandeep-Singh NIRMAL  
**Formation :** BUT Informatique — Parcours Data · Université Paris Cité  
**Année :** 2023

---

## Contexte

Dans le cadre de ma deuxième année de BUT Informatique, j'ai eu l'opportunité de répondre à un test technique proposé par **Engie**. L'objectif était d'analyser la consommation énergétique de deux points de consommation appartenant à un même site, en produisant des visualisations pertinentes et en développant un modèle prédictif.

Ce projet m'a permis de mobiliser mes compétences en **analyse de données**, **data visualisation** et **machine learning** dans un contexte industriel réel.

---

## Problématique

> **Comment analyser et prédire la consommation énergétique d'un site à partir de données de relevés temporels ?**

Les données fournies couvrent deux points de consommation (PDL 1 et PDL 2) sur la période 2022–2023, avec des relevés toutes les 10 minutes.

---

## Axes d'analyse

1. **Comparaison 2023 vs 2022** — Comparaison de la consommation mensuelle entre les deux années pour identifier les tendances et les écarts.

2. **Consommations nocturnes — Janvier 2023** — Analyse de l'évolution des consommations de nuit (22h–06h) sur le mois de janvier 2023.

3. **Profils hebdomadaires — Février 2023** — Mise en évidence des différents profils de consommation hebdomadaire sur le mois de février 2023.

4. **Machine Learning** — Modélisation prédictive par régression XGBoost pour anticiper la consommation future à partir de caractéristiques temporelles.

---

## Stack technique

- **Python 3**
- **Streamlit** — Interface web interactive
- **Pandas / NumPy** — Manipulation des données
- **Matplotlib / Seaborn** — Visualisation
- **XGBoost / Scikit-learn** — Modélisation prédictive

---

## Lancer l'application

```bash
pip install -r requirements.txt
python -m streamlit run Accueil.py
```
