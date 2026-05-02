from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

DATA_PATH = Path("ml/data/crop_yield_dataset.csv")
MODEL_DIR = Path("ml/models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)


def create_synthetic_data() -> pd.DataFrame:
    np.random.seed(42)
    rows = 1200
    rainfall = np.random.uniform(250, 1400, rows)
    temp = np.random.uniform(18, 38, rows)
    n = np.random.uniform(20, 120, rows)
    p = np.random.uniform(10, 70, rows)
    k = np.random.uniform(10, 80, rows)
    ph = np.random.uniform(5.5, 8.0, rows)

    yield_ = (
        0.0028 * rainfall + 0.085 * n + 0.06 * p + 0.055 * k - 0.9 * np.abs(ph - 6.6) - 0.07 * (temp - 27) ** 2 + 2.5
    )
    yield_ += np.random.normal(0, 0.6, rows)

    return pd.DataFrame(
        {
            "rainfall": rainfall,
            "temperature": temp,
            "nitrogen": n,
            "phosphorus": p,
            "potassium": k,
            "ph": ph,
            "yield_per_hectare": yield_.clip(0.7),
        }
    )


def load_data() -> pd.DataFrame:
    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH)
    return create_synthetic_data()


def evaluate(model, x_test, y_test) -> tuple[float, float]:
    y_pred = model.predict(x_test)
    return mean_absolute_error(y_test, y_pred), r2_score(y_test, y_pred)


def main() -> None:
    df = load_data()
    x = df[["rainfall", "temperature", "nitrogen", "phosphorus", "potassium", "ph"]]
    y = df["yield_per_hectare"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    models = {
        "LinearRegression": LinearRegression(),
        "RandomForest": RandomForestRegressor(n_estimators=300, random_state=42),
        "XGBoost": XGBRegressor(
            n_estimators=400,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.9,
            colsample_bytree=0.9,
            objective="reg:squarederror",
            random_state=42,
        ),
    }

    leaderboard = []
    best_name = ""
    best_model = None
    best_r2 = -10.0

    for name, model in models.items():
        model.fit(x_train, y_train)
        mae, r2 = evaluate(model, x_test, y_test)
        leaderboard.append((name, mae, r2))
        if r2 > best_r2:
            best_r2 = r2
            best_name = name
            best_model = model

    if best_model is None:
        raise RuntimeError("No model selected")

    model_path = MODEL_DIR / "best_yield_model.joblib"
    joblib.dump(best_model, model_path)

    print("Model comparison:")
    for name, mae, r2 in leaderboard:
        print(f"- {name}: MAE={mae:.4f}, R2={r2:.4f}")
    print(f"Best model: {best_name}")
    print(f"Saved to: {model_path}")


if __name__ == "__main__":
    main()
