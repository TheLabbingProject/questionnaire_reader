from enum import Enum

import pandas as pd

SHS_NORMAL_SCORING = ["SHS Q1", "SHS Q2", "SHS Q3"]
SHS_REVERSED_SCORING = ["SHS Q4"]


def calculate_shs(data: pd.DataFrame) -> pd.Series:
    shs_data = data[SHS_NORMAL_SCORING].copy()
    reverse = 8 - data[SHS_REVERSED_SCORING].copy()
    shs_data[SHS_REVERSED_SCORING] = reverse
    return shs_data.mean(axis=1)
