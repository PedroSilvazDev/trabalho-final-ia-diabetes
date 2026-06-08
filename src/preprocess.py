from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .config import FEATURE_COLUMNS, RANDOM_STATE, TARGET_COLUMN, TEST_SIZE


@dataclass
class PreparedData:
    x_train: np.ndarray
    x_test: np.ndarray
    y_train: np.ndarray
    y_test: np.ndarray
    feature_names: list[str]
    preprocessing_pipeline: Pipeline


def replace_invalid_zeros(df: pd.DataFrame) -> pd.DataFrame:
    """
    No dataset original, zeros representam valores ausentes em variaveis
    clinicas como glicose, pressao arterial, espessura da pele, insulina e IMC.
    """
    cleaned = df.copy()
    zero_as_missing = [
        "Glucose",
        "BloodPressure",
        "SkinThickness",
        "Insulin",
        "BMI",
    ]

    for column in zero_as_missing:
        cleaned[column] = cleaned[column].replace(0, np.nan)

    return cleaned


def build_preprocessing_pipeline() -> Pipeline:
    return Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )


def prepare_data(df: pd.DataFrame) -> PreparedData:
    cleaned = replace_invalid_zeros(df)
    x = cleaned[FEATURE_COLUMNS]
    y = cleaned[TARGET_COLUMN].astype(int)

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    pipeline = build_preprocessing_pipeline()
    x_train_processed = pipeline.fit_transform(x_train)
    x_test_processed = pipeline.transform(x_test)

    return PreparedData(
        x_train=x_train_processed,
        x_test=x_test_processed,
        y_train=y_train.to_numpy(),
        y_test=y_test.to_numpy(),
        feature_names=FEATURE_COLUMNS,
        preprocessing_pipeline=pipeline,
    )
