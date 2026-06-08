import sys
from pathlib import Path

import joblib
import numpy as np

from .config import FEATURE_COLUMNS, MODELS_DIR


def load_model(model_name: str):
    model_path = MODELS_DIR / f"{model_name.lower()}_model.joblib"
    if not model_path.exists():
        raise FileNotFoundError(
            f"Modelo nao encontrado em {model_path}. Execute python main.py primeiro."
        )
    return joblib.load(model_path)


def predict_sample(model_name: str, sample: dict) -> None:
    bundle = load_model(model_name)
    pipeline = bundle["preprocessing_pipeline"]
    classifier = bundle["classifier"]

    values = [sample[column] for column in FEATURE_COLUMNS]
    processed = pipeline.transform(np.array(values).reshape(1, -1))
    prediction = classifier.predict(processed)[0]
    probability = classifier.predict_proba(processed)[0][1]

    label = "Com diabetes" if prediction == 1 else "Sem diabetes"
    print(f"Modelo: {model_name.upper()}")
    print(f"Predicao: {label}")
    print(f"Probabilidade de diabetes: {probability:.2%}")


if __name__ == "__main__":
    exemplo = {
        "Pregnancies": 2,
        "Glucose": 120,
        "BloodPressure": 70,
        "SkinThickness": 20,
        "Insulin": 80,
        "BMI": 31.0,
        "DiabetesPedigreeFunction": 0.45,
        "Age": 35,
    }

    modelo = sys.argv[1] if len(sys.argv) > 1 else "knn"
    predict_sample(modelo, exemplo)
