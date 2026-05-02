from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

MODEL_PATH = Path("ml/models/pest_risk_classifier.joblib")
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)


def build_dataset(rows: int = 900) -> pd.DataFrame:
    np.random.seed(11)
    humidity = np.random.uniform(30, 98, rows)
    temp = np.random.uniform(15, 42, rows)
    rainfall = np.random.uniform(0, 220, rows)

    raw = 0.45 * (humidity / 100) + 0.3 * (temp / 42) + 0.25 * (rainfall / 220)
    labels = np.where(raw < 0.38, "low", np.where(raw < 0.64, "medium", "high"))

    return pd.DataFrame({"humidity": humidity, "temperature": temp, "rainfall": rainfall, "risk": labels})


def main() -> None:
    df = build_dataset()
    x = df[["humidity", "temperature", "rainfall"]]
    y = df["risk"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=250, random_state=42)
    clf.fit(x_train, y_train)

    y_pred = clf.predict(x_test)
    print(classification_report(y_test, y_pred))

    joblib.dump(clf, MODEL_PATH)
    print(f"Saved classifier to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
