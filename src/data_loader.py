from pathlib import Path
from urllib.request import urlretrieve

import pandas as pd

from .config import DATASET_PATH, DATASET_URL, FEATURE_COLUMNS, TARGET_COLUMN


def download_dataset(destination: Path = DATASET_PATH) -> Path:
    """Baixa o dataset Pima Indians Diabetes se ainda nao existir localmente."""
    destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.exists():
        return destination

    print(f"Baixando dataset de {DATASET_URL} ...")
    urlretrieve(DATASET_URL, destination)
    print(f"Dataset salvo em {destination}")
    return destination


def load_dataset(path: Path = DATASET_PATH) -> pd.DataFrame:
    """Carrega o dataset e valida as colunas esperadas."""
    if not path.exists():
        download_dataset(path)

    df = pd.read_csv(path)
    expected_columns = FEATURE_COLUMNS + [TARGET_COLUMN]
    missing = [col for col in expected_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Colunas ausentes no dataset: {missing}")

    return df
