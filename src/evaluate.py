import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import GridSearchCV

from .config import FIGURES_DIR, OUTPUTS_DIR, RANDOM_STATE


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_proba: np.ndarray) -> dict:
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1_score": float(f1_score(y_true, y_pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_true, y_proba)),
    }


def save_classification_report(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    model_name: str,
    output_dir: Path = OUTPUTS_DIR,
) -> None:
    report = classification_report(y_true, y_pred, digits=4)
    report_path = output_dir / f"relatorio_{model_name.lower()}.txt"
    report_path.write_text(report, encoding="utf-8")


def plot_confusion_matrix(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    model_name: str,
    output_dir: Path = FIGURES_DIR,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    figure_path = output_dir / f"matriz_confusao_{model_name.lower()}.png"

    fig, ax = plt.subplots(figsize=(6, 5))
    ConfusionMatrixDisplay.from_predictions(
        y_true,
        y_pred,
        display_labels=["Sem diabetes", "Com diabetes"],
        cmap="Blues",
        ax=ax,
        colorbar=False,
    )
    ax.set_title(f"Matriz de confusao - {model_name}")
    fig.tight_layout()
    fig.savefig(figure_path, dpi=150)
    plt.close(fig)
    return figure_path


def plot_roc_curves(
    results: list[dict],
    output_dir: Path = FIGURES_DIR,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    figure_path = output_dir / "curvas_roc.png"

    fig, ax = plt.subplots(figsize=(7, 6))
    for result in results:
        fpr, tpr, _ = roc_curve(result["y_true"], result["y_proba"])
        ax.plot(
            fpr,
            tpr,
            label=f"{result['model_name']} (AUC = {result['metrics']['roc_auc']:.3f})",
        )

    ax.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Classificador aleatorio")
    ax.set_xlabel("Taxa de falso positivo")
    ax.set_ylabel("Taxa de verdadeiro positivo")
    ax.set_title("Curvas ROC - KNN vs SVM")
    ax.legend()
    fig.tight_layout()
    fig.savefig(figure_path, dpi=150)
    plt.close(fig)
    return figure_path


def plot_metrics_comparison(
    metrics_df: pd.DataFrame,
    output_dir: Path = FIGURES_DIR,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    figure_path = output_dir / "comparacao_metricas.png"

    melted = metrics_df.melt(
        id_vars="modelo",
        value_vars=["accuracy", "precision", "recall", "f1_score", "roc_auc"],
        var_name="metrica",
        value_name="valor",
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=melted, x="metrica", y="valor", hue="modelo", ax=ax)
    ax.set_ylim(0, 1)
    ax.set_title("Comparacao de metricas entre modelos")
    ax.set_xlabel("Metrica")
    ax.set_ylabel("Valor")
    fig.tight_layout()
    fig.savefig(figure_path, dpi=150)
    plt.close(fig)
    return figure_path


def plot_knn_k_search(
    grid_search: GridSearchCV,
    output_dir: Path = FIGURES_DIR,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    figure_path = output_dir / "knn_busca_k.png"

    results = pd.DataFrame(grid_search.cv_results_)
    grouped = (
        results.groupby("param_n_neighbors")["mean_test_score"]
        .mean()
        .reset_index()
        .sort_values("param_n_neighbors")
    )

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(
        grouped["param_n_neighbors"],
        grouped["mean_test_score"],
        marker="o",
    )
    ax.set_title("KNN - validacao cruzada por valor de k")
    ax.set_xlabel("Numero de vizinhos (k)")
    ax.set_ylabel("Acuracia media (validacao cruzada)")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(figure_path, dpi=150)
    plt.close(fig)
    return figure_path


def save_metrics_summary(metrics_df: pd.DataFrame, output_dir: Path = OUTPUTS_DIR) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "metricas_comparacao.csv"
    json_path = output_dir / "metricas_comparacao.json"

    metrics_df.to_csv(csv_path, index=False)
    json_path.write_text(
        metrics_df.to_json(orient="records", indent=2, force_ascii=False),
        encoding="utf-8",
    )
    return csv_path
