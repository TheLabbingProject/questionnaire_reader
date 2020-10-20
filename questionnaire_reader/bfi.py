import pandas as pd

from enum import Enum


class BFI(Enum):
    AGREE = "Agreeableness"
    CONSC = "Conscientiousness"
    EXRTA = "Extraversion"
    NEURO = "Neuroticism"
    OPEN = "Openness to Experience"


BFI_QUESTIONS = {
    BFI.AGREE: [1, 6, 11, 16, 21, 26, 31, 36, 41],
    BFI.CONSC: [2, 7, 12, 17, 22, 27, 32, 37, 42],
    BFI.EXRTA: [0, 5, 10, 15, 20, 25, 30, 35],
    BFI.NEURO: [3, 8, 13, 18, 23, 28, 33, 38],
    BFI.OPEN: [4, 9, 14, 19, 24, 29, 34, 39, 40, 43],
}
REVERSED_SCORING = (1, 5, 7, 8, 11, 17, 20, 22, 23, 26, 30, 33, 34, 36, 40, 42)
REPLACE_DICT = {
    "בהחלט לא מסכים": 1,
    "לא מסכים": 2,
    "ניטראלי": 3,
    "מסכים": 4,
    "מסכים בהחלט": 5,
}


def calculate_bfi(data: pd.Series) -> pd.Series:
    data.replace(REPLACE_DICT, inplace=True)
    scores = {}
    for trait in BFI:
        indices = BFI_QUESTIONS[trait]
        responses = data[indices]
        reverse = 6 - responses[responses.index.isin(REVERSED_SCORING)]
        responses.update(reverse)
        scores[trait.value] = responses.mean()
    return pd.Series(scores)
