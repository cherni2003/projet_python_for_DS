# projet_python_for_data_science
📌 Nom du projet

Wikipedia Socio-Economic Data Pipeline & Life Expectancy Prediction

🎯 Objectifs du projet

🎯 Objectif général

Développer un pipeline complet de données et de machine learning à partir de données publiques issues de Wikipedia afin de prédire l’espérance de vie d’un pays.

🎯 Objectifs spécifiques

Scraper automatiquement plusieurs pages Wikipedia

Nettoyer, standardiser et fusionner les données

Réaliser une analyse exploratoire (EDA)

Construire un modèle de machine learning (Boosting)

Exposer le modèle via une API REST

Développer une interface frontend

Conteneuriser et déployer l’application

🌐 Liens des datasets à scraper (Sources)

Les données sont extraites des pages Wikipedia suivantes :

Population par pays
https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population

PIB (GDP nominal) par pays
https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)

Espérance de vie par pays
https://en.wikipedia.org/wiki/List_of_countries_by_life_expectancy

➡️ Ces pages contiennent des tableaux structurés (wikitable) adaptés au web scraping.

🏗️ Architecture du projet
🔹 Architecture globale
<img width="1024" height="1536" alt="image" src="https://github.com/user-attachments/assets/daa8967a-6578-42fa-82ea-edd0f5586e0e" />


📁 Architecture des dossiers
wikipedia-ml-pipeline/
│── data/
│   ├── raw/              # Données brutes issues du scraping
│   ├── processed/        # Données nettoyées et fusionnées
│── scraping/             # Scripts de scraping Wikipedia
│── preprocessing/        # Nettoyage et feature engineering
│── modeling/             # Entraînement et évaluation ML
│── api/                  # API FastAPI
│── frontend/             # Application React
│── docker/               # Dockerfiles et docker-compose
│── notebooks/            # EDA et expérimentations
│── README.md
│── requirements.txt


---

## 📦 Livrables

- Scripts de web scraping
- Datasets bruts (CSV)
- Dataset final fusionné et nettoyé
- Notebook d’analyse exploratoire (EDA)
- Modèle de machine learning entraîné
- API REST fonctionnelle
- Interface frontend
- Fichiers Docker
- Rapport final et présentation

---

## ✅ Checklist par phase

### 🟦 Week 1 – Setup, Scraping & EDA
- [x] Choix des sources Wikipedia
- [x] Scripts de scraping (population, GDP, espérance de vie)
- [x] Sauvegarde des données brutes
- [x] Analyse exploratoire (EDA)

### 🟦 Week 2 – Preprocessing & Feature Engineering
- [x] Nettoyage des données
- [x] Standardisation des noms des pays
- [x] Fusion des datasets
- [x] Création de nouvelles variables

### 🟦 Week 3 – Modeling & MLflow
- [x] Sélection du modèle (Boosting)
- [x] Entraînement du modèle
- [x] Évaluation des performances
- [x] Suivi des expériences avec MLflow

### 🟦 Week 4 – API Development
- [ ] Création de l’API FastAPI
- [ ] Endpoint de prédiction
- [ ] Validation des données d’entrée

### 🟦 Week 5 – Frontend Development
- [ ] Interface utilisateur React
- [ ] Connexion à l’API
- [ ] Affichage des prédictions

### 🟦 Week 6 – Containerization
- [ ] Dockerfile backend
- [ ] Dockerfile frontend
- [ ] Docker Compose

### 🟦 Week 7 – Deployment & Final Review
- [ ] Déploiement de l’application
- [ ] Tests finaux
- [ ] Rapport final
- [ ] Soutenance

---

## ⚠️ Aspects éthiques et légaux
- Les données utilisées sont publiques et libres d’accès
- Le scraping est réalisé de manière responsable
- Aucune donnée personnelle n’est collectée

---








Aucune donnée personnelle n’est collectée
