from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
import pandas as pd
import joblib
import math
import io
import os

app = FastAPI(
    title="World Countries Prediction API",
    description="Predicts Life Expectancy (regression) and Development Level (classification).",
    version="1.0.0"
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ── Model loading ──────────────────────────────────────────────────────────────
LIFE_EXP_MODEL_PATH  = r"C:\Users\Cherni Oumaima\Desktop\projet_python_for_DS\data\LifeExpectancyBestModel.pkl"
DEV_LEVEL_MODEL_PATH = r"C:\Users\Cherni Oumaima\Desktop\projet_python_for_DS\data\DevelopmentLevelBestModel.pkl"

def load_model(path: str):
    if os.path.exists(path):
        try:
            return joblib.load(path)
        except Exception as e:
            print(f"[WARNING] Could not load model from '{path}': {e}")
            return None
    print(f"[WARNING] Model file not found: '{path}'")
    return None

life_exp_model  = load_model(LIFE_EXP_MODEL_PATH)
dev_level_model = load_model(DEV_LEVEL_MODEL_PATH)

# ── Exact feature columns from training (pd.get_dummies drop_first=True) ──────
#
# Regression model (Life_Expectancy) — 21 features
# X = df.drop(columns=["Life_Expectancy", "Country"])  → get_dummies
LIFE_EXP_FEATURES = [
    "Rank", "Population", "GDP_Rank", "GDP_USD_millions", "GDP_USD_billions",
    "Life_Expectancy_Male", "Life_Expectancy_Female", "GDP_per_Capita",
    "Log_Population", "Log_GDP", "Log_GDP_per_Capita",
    "Life_Expectancy_Gender_Gap", "Wealth_Score",
    "Population_Category_Medium", "Population_Category_Small",
    "Population_Category_Very Large",
    "GDP_Category_Low", "GDP_Category_Medium", "GDP_Category_Very High",
    "Development_Level_Developing", "Development_Level_Emerging",
]

# Classification model (Development_Level) — 20 features
# X = df.drop(columns=["Development_Level", "Country"])  → get_dummies
DEV_LEVEL_FEATURES = [
    "Rank", "Population", "GDP_Rank", "GDP_USD_millions", "GDP_USD_billions",
    "Life_Expectancy", "Life_Expectancy_Male", "Life_Expectancy_Female",
    "GDP_per_Capita", "Log_Population", "Log_GDP", "Log_GDP_per_Capita",
    "Life_Expectancy_Gender_Gap", "Wealth_Score",
    "Population_Category_Medium", "Population_Category_Small",
    "Population_Category_Very Large",
    "GDP_Category_Low", "GDP_Category_Medium", "GDP_Category_Very High",
]

# ── Valid categorical values (from dataset) ────────────────────────────────────
VALID_POPULATION_CATEGORIES = ["Large", "Medium", "Small", "Very Large"]
VALID_GDP_CATEGORIES        = ["High", "Low", "Medium", "Very High"]
VALID_DEVELOPMENT_LEVELS    = ["Developed", "Developing", "Emerging"]

# ── Pydantic schema ────────────────────────────────────────────────────────────
# The user sends raw values — the API handles encoding internally.
class CountryData(BaseModel):
    # Numeric
    Rank:                      int     = Field(..., example=50)
    Population:                float   = Field(..., example=50_000_000)
    GDP_Rank:                  float   = Field(..., example=40.0)
    GDP_USD_millions:          float   = Field(..., example=500_000.0)
    GDP_USD_billions:          float   = Field(..., example=500.0)
    Life_Expectancy_Male:      float   = Field(..., example=72.0)
    Life_Expectancy_Female:    float   = Field(..., example=76.0)
    GDP_per_Capita:            float   = Field(..., example=10_000.0)
    Log_Population:            float   = Field(..., example=17.7)
    Log_GDP:                   float   = Field(..., example=13.1)
    Log_GDP_per_Capita:        float   = Field(..., example=9.2)
    Life_Expectancy_Gender_Gap:float   = Field(..., example=4.0)
    Wealth_Score:              float   = Field(..., example=0.0003)

    # Categorical (raw string — encoded internally)
    Population_Category: str = Field(..., example="Very Large",
                                     description="One of: Large, Medium, Small, Very Large")
    GDP_Category:        str = Field(..., example="High",
                                     description="One of: High, Low, Medium, Very High")
    Development_Level:   str = Field(..., example="Emerging",
                                     description="One of: Developed, Developing, Emerging — used only for Life_Expectancy prediction")

    # Optional — only needed for Development_Level prediction
    Life_Expectancy: Optional[float] = Field(None, example=74.0,
                                             description="Required only for Development_Level prediction")

    model_config = {
        "json_schema_extra": {
            "example": {
                "Rank": 50,
                "Population": 50_000_000,
                "GDP_Rank": 40.0,
                "GDP_USD_millions": 500_000.0,
                "GDP_USD_billions": 500.0,
                "Life_Expectancy_Male": 72.0,
                "Life_Expectancy_Female": 76.0,
                "GDP_per_Capita": 10_000.0,
                "Log_Population": 17.7,
                "Log_GDP": 13.1,
                "Log_GDP_per_Capita": 9.2,
                "Life_Expectancy_Gender_Gap": 4.0,
                "Wealth_Score": 0.0003,
                "Population_Category": "Very Large",
                "GDP_Category": "High",
                "Development_Level": "Emerging",
                "Life_Expectancy": 74.0,
            }
        }
    }


# ── Encoding helper ────────────────────────────────────────────────────────────
def encode_categoricals(row: dict) -> dict:
    """
    Reproduces pd.get_dummies(drop_first=True) applied during training.
    drop_first removes the first category alphabetically:
      Population_Category → drops 'Large'   (keeps Medium, Small, Very Large)
      GDP_Category        → drops 'High'     (keeps Low, Medium, Very High)
      Development_Level   → drops 'Developed'(keeps Developing, Emerging)
    """
    pop_cat = row.get("Population_Category", "")
    gdp_cat = row.get("GDP_Category", "")
    dev_lvl = row.get("Development_Level", "")

    encoded = {
        # Population_Category dummies (base = Large)
        "Population_Category_Medium":     int(pop_cat == "Medium"),
        "Population_Category_Small":      int(pop_cat == "Small"),
        "Population_Category_Very Large": int(pop_cat == "Very Large"),
        # GDP_Category dummies (base = High)
        "GDP_Category_Low":               int(gdp_cat == "Low"),
        "GDP_Category_Medium":            int(gdp_cat == "Medium"),
        "GDP_Category_Very High":         int(gdp_cat == "Very High"),
        # Development_Level dummies (base = Developed) — only for regression
        "Development_Level_Developing":   int(dev_lvl == "Developing"),
        "Development_Level_Emerging":     int(dev_lvl == "Emerging"),
    }
    return encoded


def build_regression_input(data: CountryData) -> pd.DataFrame:
    """Builds the 21-column DataFrame expected by the Life Expectancy model."""
    row = data.model_dump()
    enc = encode_categoricals(row)
    flat = {
        "Rank":                       row["Rank"],
        "Population":                 row["Population"],
        "GDP_Rank":                   row["GDP_Rank"],
        "GDP_USD_millions":           row["GDP_USD_millions"],
        "GDP_USD_billions":           row["GDP_USD_billions"],
        "Life_Expectancy_Male":       row["Life_Expectancy_Male"],
        "Life_Expectancy_Female":     row["Life_Expectancy_Female"],
        "GDP_per_Capita":             row["GDP_per_Capita"],
        "Log_Population":             row["Log_Population"],
        "Log_GDP":                    row["Log_GDP"],
        "Log_GDP_per_Capita":         row["Log_GDP_per_Capita"],
        "Life_Expectancy_Gender_Gap": row["Life_Expectancy_Gender_Gap"],
        "Wealth_Score":               row["Wealth_Score"],
        **enc,
    }
    df = pd.DataFrame([flat])[LIFE_EXP_FEATURES]
    return df


def build_classification_input(data: CountryData) -> pd.DataFrame:
    """Builds the 20-column DataFrame expected by the Development Level model."""
    row = data.model_dump()
    enc = encode_categoricals(row)

    life_exp = row.get("Life_Expectancy")
    if life_exp is None:
        raise HTTPException(
            status_code=422,
            detail="'Life_Expectancy' is required for Development Level prediction."
        )

    flat = {
        "Rank":                       row["Rank"],
        "Population":                 row["Population"],
        "GDP_Rank":                   row["GDP_Rank"],
        "GDP_USD_millions":           row["GDP_USD_millions"],
        "GDP_USD_billions":           row["GDP_USD_billions"],
        "Life_Expectancy":            life_exp,
        "Life_Expectancy_Male":       row["Life_Expectancy_Male"],
        "Life_Expectancy_Female":     row["Life_Expectancy_Female"],
        "GDP_per_Capita":             row["GDP_per_Capita"],
        "Log_Population":             row["Log_Population"],
        "Log_GDP":                    row["Log_GDP"],
        "Log_GDP_per_Capita":         row["Log_GDP_per_Capita"],
        "Life_Expectancy_Gender_Gap": row["Life_Expectancy_Gender_Gap"],
        "Wealth_Score":               row["Wealth_Score"],
        **enc,
    }
    df = pd.DataFrame([flat])[DEV_LEVEL_FEATURES]
    return df


def encode_batch(df: pd.DataFrame) -> pd.DataFrame:
    """Applies the same get_dummies encoding on a batch DataFrame."""
    df = df.copy()
    df = df.fillna(df.median(numeric_only=True))

    for col, categories, base in [
        ("Population_Category", VALID_POPULATION_CATEGORIES, "Large"),
        ("GDP_Category",        VALID_GDP_CATEGORIES,        "High"),
        ("Development_Level",   VALID_DEVELOPMENT_LEVELS,    "Developed"),
    ]:
        if col in df.columns:
            for cat in categories:
                if cat != base:
                    df[f"{col}_{cat}"] = (df[col] == cat).astype(int)
            df.drop(columns=[col], inplace=True)

    return df


# ── Health ─────────────────────────────────────────────────────────────────────
@app.get("/health", tags=["Monitoring"])
def health_check():
    """Returns the loading status of both models."""
    return {
        "status": "ok" if life_exp_model and dev_level_model else "degraded",
        "life_expectancy_model_loaded":  life_exp_model  is not None,
        "development_level_model_loaded": dev_level_model is not None,
    }


# ── Single prediction ──────────────────────────────────────────────────────────
@app.post("/predict", tags=["Prediction"])
def predict(data: CountryData):
    """
    Real-time dual prediction for a single country.

    Returns:
    - **life_expectancy_prediction** – predicted life expectancy in years
    - **development_level_prediction** – Developed / Developing / Emerging
    - **development_level_probabilities** – probability for each class
    """
    if not life_exp_model or not dev_level_model:
        raise HTTPException(status_code=503, detail="One or both models are not available.")

    # ── Life Expectancy (regression) ──────────────────────────────────────────
    reg_df        = build_regression_input(data)
    life_exp_pred = float(life_exp_model.predict(reg_df)[0])

    # ── Development Level (classification) ───────────────────────────────────
    clf_df      = build_classification_input(data)
    dev_pred    = dev_level_model.predict(clf_df)[0]
    dev_proba   = dev_level_model.predict_proba(clf_df)[0]
    dev_classes = dev_level_model.classes_.tolist()

    # dev_level_model uses LabelEncoder → classes are integers, map back
    label_map = {0: "Developed", 1: "Developing", 2: "Emerging"}
    dev_pred_label = label_map.get(int(dev_pred), str(dev_pred))

    return {
        "life_expectancy_prediction": round(life_exp_pred, 2),
        "development_level_prediction": dev_pred_label,
        "development_level_probabilities": {
            label_map.get(cls, str(cls)): round(float(prob), 4)
            for cls, prob in zip(dev_classes, dev_proba)
        },
    }


# ── Batch prediction ───────────────────────────────────────────────────────────
@app.post("/predict_batch", tags=["Prediction"])
async def predict_batch(file: UploadFile = File(...)):
    """
    Batch dual prediction from a CSV file.

    The CSV must contain the raw columns (before encoding).
    Returns original rows enriched with:
    - **Life_Expectancy_Prediction**
    - **Development_Level_Prediction**
    - **Dev_Prob_Developed**, **Dev_Prob_Developing**, **Dev_Prob_Emerging**
    """
    if not life_exp_model or not dev_level_model:
        raise HTTPException(status_code=503, detail="One or both models are not available.")

    try:
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read CSV: {e}")

    df_enc = encode_batch(df)

    # ── Life Expectancy ───────────────────────────────────────────────────────
    missing_reg = [c for c in LIFE_EXP_FEATURES if c not in df_enc.columns]
    if missing_reg:
        raise HTTPException(status_code=400, detail=f"CSV missing columns for regression: {missing_reg}")

    df["Life_Expectancy_Prediction"] = life_exp_model.predict(df_enc[LIFE_EXP_FEATURES]).round(2)

    # ── Development Level ─────────────────────────────────────────────────────
    missing_clf = [c for c in DEV_LEVEL_FEATURES if c not in df_enc.columns]
    if missing_clf:
        raise HTTPException(status_code=400, detail=f"CSV missing columns for classification: {missing_clf}")

    label_map   = {0: "Developed", 1: "Developing", 2: "Emerging"}
    raw_preds   = dev_level_model.predict(df_enc[DEV_LEVEL_FEATURES])
    dev_proba   = dev_level_model.predict_proba(df_enc[DEV_LEVEL_FEATURES])
    dev_classes = dev_level_model.classes_.tolist()

    df["Development_Level_Prediction"] = [label_map.get(int(p), str(p)) for p in raw_preds]
    for i, cls in enumerate(dev_classes):
        df[f"Dev_Prob_{label_map.get(cls, str(cls))}"] = dev_proba[:, i].round(4)

    # ── NaN-safe JSON serialization ───────────────────────────────────────────
    # Python's json module raises ValueError on NaN floats.
    # We convert every value: NaN/Inf → None, numpy types → native Python.
    def sanitize(val):
        if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
            return None
        if hasattr(val, "item"):          # numpy scalar → python scalar
            return val.item()
        return val

    records = [
        {k: sanitize(v) for k, v in row.items()}
        for row in df.to_dict(orient="records")
    ]

    return JSONResponse(content=records)


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)