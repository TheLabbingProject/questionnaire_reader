from enum import Enum

import pandas as pd

NORMAL_SCORING = ["SHS Q1", "SHS Q2", "SHS Q3"]
REVERSED_SCORING = ["SHS Q4"]


def calculate_shs(data: pd.Series) -> pd.Series:
    shs_data = data[NORMAL_SCORING]
    reverse = 8 - data[REVERSED_SCORING]
    shs_data[REVERSED_SCORING] = reverse
    return shs_data.mean(axis=1)
