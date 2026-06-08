import json
from pathlib import Path

import pandas as pd

from src.config import DATASET_PATH, FIGURES_DIR, OUTPUTS_DIR
from src.data_loader import load_dataset
from src.evaluate import (
    plot_confusion_matrix,
    plot_knn_k_search,
    plot_metrics_comparison,
    plot_roc_curves,
    save_metrics_summary,
)
from src.preprocess import prepare_data
from src.train import print_result_summary, save_model_bundle, train_knn, train_svm


def print_dataset_summary(df: pd.DataFrame) -> None:
    print("=== Resumo do dataset ===")
    print(f"Arquivo: {DATASET_PATH}")
    print(f"Registros: {len(df)}")
    print(f"Atributos: {df.shape[1] - 1}")
    print("Distribuicao da variavel alvo (Outcome):")
    print(df["Outcome"].value_counts().to_string())
    print()


def choose_best_model(metrics_df: pd.DataFrame) -> str:
    best_row = metrics_df.sort_values(
        by=["f1_score", "roc_auc", "accuracy"],
        ascending=False,
    ).iloc[0]
    return best_row["modelo"]


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    df = load_dataset()
    print_dataset_summary(df)

    prepared = prepare_data(df)
    print("=== Divisao treino/teste ===")
    print(f"Treino: {len(prepared.y_train)} amostras")
    print(f"Teste: {len(prepared.y_test)} amostras")
    print("Pre-processamento: imputacao por mediana + padronizacao (StandardScaler)")

    knn_result = train_knn(prepared)
    svm_result = train_svm(prepared)

    print_result_summary(knn_result, prepared)
    print_result_summary(svm_result, prepared)

    save_model_bundle(knn_result, prepared.preprocessing_pipeline)
    save_model_bundle(svm_result, prepared.preprocessing_pipeline)

    metrics_df = pd.DataFrame(
        [
            {"modelo": knn_result.model_name, **knn_result.metrics},
            {"modelo": svm_result.model_name, **svm_result.metrics},
        ]
    )
    save_metrics_summary(metrics_df)

    plot_confusion_matrix(prepared.y_test, knn_result.y_pred, knn_result.model_name)
    plot_confusion_matrix(prepared.y_test, svm_result.y_pred, svm_result.model_name)
    plot_knn_k_search(knn_result.grid_search)
    plot_metrics_comparison(metrics_df)
    plot_roc_curves(
        [
            {
                "model_name": knn_result.model_name,
                "y_true": prepared.y_test,
                "y_proba": knn_result.y_proba,
                "metrics": knn_result.metrics,
            },
            {
                "model_name": svm_result.model_name,
                "y_true": prepared.y_test,
                "y_proba": svm_result.y_proba,
                "metrics": svm_result.metrics,
            },
        ]
    )

    best_model = choose_best_model(metrics_df)
    conclusion = {
        "melhor_modelo": best_model,
        "metricas": metrics_df.to_dict(orient="records"),
        "knn_hiperparametros": knn_result.best_params,
        "svm_hiperparametros": svm_result.best_params,
    }

    conclusion_path = OUTPUTS_DIR / "conclusao.json"
    conclusion_path.write_text(
        json.dumps(conclusion, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\n=== Comparacao final ===")
    print(metrics_df.to_string(index=False))
    print(f"\nMelhor modelo segundo F1-score e ROC-AUC: {best_model}")
    print(f"Graficos salvos em: {FIGURES_DIR}")
    print(f"Modelos salvos em: models/")


if __name__ == "__main__":
    main()
