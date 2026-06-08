from dataclasses import dataclass
from pathlib import Path

import joblib
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from .config import MODELS_DIR, RANDOM_STATE
from .evaluate import compute_metrics, save_classification_report
from .preprocess import PreparedData


@dataclass
class ModelResult:
    model_name: str
    estimator: object
    best_params: dict
    y_pred: np.ndarray
    y_proba: np.ndarray
    metrics: dict
    grid_search: GridSearchCV | None = None


def train_knn(data: PreparedData) -> ModelResult:
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    param_grid = {"n_neighbors": list(range(3, 22, 2))}

    grid_search = GridSearchCV(
        KNeighborsClassifier(),
        param_grid=param_grid,
        scoring="accuracy",
        cv=cv,
        n_jobs=-1,
    )
    grid_search.fit(data.x_train, data.y_train)

    model = grid_search.best_estimator_
    y_pred = model.predict(data.x_test)
    y_proba = model.predict_proba(data.x_test)[:, 1]
    metrics = compute_metrics(data.y_test, y_pred, y_proba)

    return ModelResult(
        model_name="KNN",
        estimator=model,
        best_params=grid_search.best_params_,
        y_pred=y_pred,
        y_proba=y_proba,
        metrics=metrics,
        grid_search=grid_search,
    )


def train_svm(data: PreparedData) -> ModelResult:
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    param_grid = {
        "C": [0.1, 1, 10],
        "kernel": ["linear", "rbf"],
        "gamma": ["scale", "auto"],
    }

    grid_search = GridSearchCV(
        SVC(probability=True, random_state=RANDOM_STATE),
        param_grid=param_grid,
        scoring="accuracy",
        cv=cv,
        n_jobs=-1,
    )
    grid_search.fit(data.x_train, data.y_train)

    model = grid_search.best_estimator_
    y_pred = model.predict(data.x_test)
    y_proba = model.predict_proba(data.x_test)[:, 1]
    metrics = compute_metrics(data.y_test, y_pred, y_proba)

    return ModelResult(
        model_name="SVM",
        estimator=model,
        best_params=grid_search.best_params_,
        y_pred=y_pred,
        y_proba=y_proba,
        metrics=metrics,
        grid_search=grid_search,
    )


def save_model_bundle(
    result: ModelResult,
    preprocessing_pipeline,
    output_dir: Path = MODELS_DIR,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = output_dir / f"{result.model_name.lower()}_model.joblib"

    bundle = {
        "model_name": result.model_name,
        "classifier": result.estimator,
        "preprocessing_pipeline": preprocessing_pipeline,
        "best_params": result.best_params,
        "metrics": result.metrics,
    }
    joblib.dump(bundle, model_path)
    return model_path


def print_result_summary(result: ModelResult, data: PreparedData) -> None:
    train_accuracy = accuracy_score(
        data.y_train,
        result.estimator.predict(data.x_train),
    )

    print(f"\n=== {result.model_name} ===")
    print(f"Melhores hiperparametros: {result.best_params}")
    print(f"Acuracia no treino: {train_accuracy:.4f}")
    print(f"Acuracia no teste: {result.metrics['accuracy']:.4f}")
    print(f"Precisao: {result.metrics['precision']:.4f}")
    print(f"Revocacao: {result.metrics['recall']:.4f}")
    print(f"F1-score: {result.metrics['f1_score']:.4f}")
    print(f"ROC-AUC: {result.metrics['roc_auc']:.4f}")

    save_classification_report(data.y_test, result.y_pred, result.model_name)
