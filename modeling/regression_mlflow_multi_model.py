# ============================================
# Week 3 – Regression & MLflow (Auto Multi-Model + Best Model Selection)
# Target: Life_Expectancy
# ============================================

import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from xgboost import XGBRegressor  # pip install xgboost
import itertools

# --------------------------------------------
# 1. Load Dataset
# --------------------------------------------
DATA_PATH = "data/processed/processed_data.csv"
df = pd.read_csv(DATA_PATH)

print("Dataset loaded:", df.shape)

# --------------------------------------------
# 2. Feature / Target Separation
# --------------------------------------------
TARGET = "Life_Expectancy"
X = df.drop(columns=[TARGET, "Country"])
y = df[TARGET]

# --------------------------------------------
# 3. Handle Missing Values
# --------------------------------------------
X = X.fillna(X.median(numeric_only=True))
y = y.fillna(y.median())

print("Missing values in X:", X.isna().sum().sum())
print("Missing values in y:", y.isna().sum())

# --------------------------------------------
# 4. Encode Categorical Features
# --------------------------------------------
X = pd.get_dummies(X, drop_first=True)
print("Features after encoding:", X.shape)

# --------------------------------------------
# 5. Train / Test Split
# --------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --------------------------------------------
# 6. MLflow Experiment
# --------------------------------------------
experiment_name = "Week3_LifeExpectancy_MultiModel"
mlflow.set_experiment(experiment_name)

# --------------------------------------------
# 7. Define Models & Hyperparameters
# --------------------------------------------
models = [
    ("GradientBoosting", GradientBoostingRegressor, {
        "n_estimators": [150, 200],
        "learning_rate": [0.05, 0.1],
        "max_depth": [3, 4]
    }),
    ("RandomForest", RandomForestRegressor, {
        "n_estimators": [100, 200],
        "max_depth": [5, 7]
    }),
    ("XGBoost", XGBRegressor, {
        "n_estimators": [150, 200],
        "learning_rate": [0.05, 0.1],
        "max_depth": [3, 4],
        "eval_metric": ["rmse"]
    })
]

# --------------------------------------------
# 8. Train & Log Each Model + Hyperparameters
# --------------------------------------------
for model_name, model_class, param_grid in models:
    keys, values = zip(*param_grid.items())
    for combination in itertools.product(*values):
        params = dict(zip(keys, combination))
        
        run_name = f"{model_name}_" + "_".join([f"{k}={v}" for k, v in params.items()])
        
        with mlflow.start_run(run_name=run_name):
            # Instancier le modèle avec ces paramètres
            model_instance = model_class(**params, random_state=42)
            
            # Entraînement
            model_instance.fit(X_train, y_train)
            y_pred = model_instance.predict(X_test)
            
            # Metrics
            mse = mean_squared_error(y_test, y_pred)
            rmse = mse ** 0.5
            r2 = r2_score(y_test, y_pred)
            
            print(f"\nRun: {run_name}")
            print(f"RMSE: {rmse:.4f}, R2: {r2:.4f}")
            
            # MLflow logging
            mlflow.log_param("model", model_name)
            for k, v in params.items():
                mlflow.log_param(k, v)
            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("r2", r2)
            
            mlflow.sklearn.log_model(model_instance, f"{model_name}_model")

print("\n✅ All models and hyperparameter combinations logged to MLflow!")

# --------------------------------------------
# 9. Automatic Best Model Selection
# --------------------------------------------
# Récupérer le meilleur run selon R2
experiment = mlflow.get_experiment_by_name(experiment_name)
runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])

best_run = runs.loc[runs['metrics.r2'].idxmax()]
best_run_id = best_run['run_id']
best_model_name = best_run['params.model']

best_model = mlflow.sklearn.load_model(f"runs:/{best_run_id}/{best_model_name}_model")

print("\n✅ Best model loaded automatically from MLflow!")
print("Run ID:", best_run_id)
print("Model:", best_model_name)
print("R2 Score:", best_run['metrics.r2'])
print("RMSE:", best_run['metrics.rmse'])
