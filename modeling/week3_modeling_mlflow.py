# ============================================
# Week 3 – Modeling & MLflow (MULTI-MODEL VERSION)
# Project: Wikipedia Socio-Economic Data Pipeline
# ============================================

import pandas as pd
import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier  # pip install xgboost si nécessaire

# --------------------------------------------
# 1. Load Dataset
# --------------------------------------------

DATA_PATH = "data\processed\processed_data.csv"
df = pd.read_csv(DATA_PATH)

print("Dataset loaded")
print(df.shape)

# --------------------------------------------
# 2. Feature / Target Separation
# --------------------------------------------

TARGET = "Development_Level"

X = df.drop(columns=[TARGET, "Country"])
y = df[TARGET]

# --------------------------------------------
# 3. Handle Missing Values
# --------------------------------------------

X = X.fillna(X.median(numeric_only=True))

# --------------------------------------------
# 4. Encode Categorical Features
# --------------------------------------------

X = pd.get_dummies(X, drop_first=True)
print("Features after encoding:", X.shape)

# --------------------------------------------
# 5. Encode Target Variable
# --------------------------------------------

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)
print("Target classes:", label_encoder.classes_)

# --------------------------------------------
# 6. Train / Test Split
# --------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)

# --------------------------------------------
# 7. MLflow Experiment
# --------------------------------------------

mlflow.set_experiment("Week3_Development_Level_MultiModel")

# --------------------------------------------
# 8. Define Models to Test
# --------------------------------------------

models = [
    ("GradientBoosting", GradientBoostingClassifier(n_estimators=150, learning_rate=0.05, max_depth=3, random_state=42)),
    ("RandomForest", RandomForestClassifier(n_estimators=200, max_depth=5, random_state=42)),
    ("XGBoost", XGBClassifier(n_estimators=150, learning_rate=0.05, max_depth=3, use_label_encoder=False, eval_metric='mlogloss', random_state=42))
]

# --------------------------------------------
# 9. Train & Log Each Model in MLflow
# --------------------------------------------

for model_name, model_instance in models:
    with mlflow.start_run(run_name=model_name):
        # Train model
        model_instance.fit(X_train, y_train)
        y_pred = model_instance.predict(X_test)

        # Evaluation
        accuracy = accuracy_score(y_test, y_pred)
        print(f"\nModel: {model_name}")
        print("Accuracy:", accuracy)
        print(classification_report(y_test, y_pred, target_names=[str(c) for c in label_encoder.classes_]))

        # MLflow logging
        mlflow.log_param("model", model_name)
        if hasattr(model_instance, "n_estimators"):
            mlflow.log_param("n_estimators", model_instance.n_estimators)
        if hasattr(model_instance, "learning_rate"):
            mlflow.log_param("learning_rate", model_instance.learning_rate)
        if hasattr(model_instance, "max_depth"):
            mlflow.log_param("max_depth", model_instance.max_depth)

        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(model_instance, f"{model_name}_model")

print("\n✅ All models trained and logged to MLflow!")
