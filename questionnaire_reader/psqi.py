from datetime import datetime
from enum import Enum

import pandas as pd


class PsqiQuestions(Enum):
    PSQI_0 = "1"
    PSQI_1 = "2"
    PSQI_2 = "3"
    PSQI_3 = "4"
    PSQI_4 = "5a"
    PSQI_5 = "5b"
    PSQI_6 = "5c"
    PSQI_7 = "5d"
    PSQI_8 = "5e"
    PSQI_9 = "5f"
    PSQI_10 = "5g"
    PSQI_11 = "5h"
    PSQI_12 = "5i"
    PSQI_13 = "5j"
    PSQI_14 = "5j_descriptive"
    PSQI_15 = "6"
    PSQI_16 = "7"
    PSQI_17 = "8"
    PSQI_18 = "9"
    PSQI_19 = "10"
    PSQI_20 = "10a"
    PSQI_21 = "10b"
    PSQI_22 = "10c"
    PSQI_23 = "10d"
    PSQI_24 = "10e"
    PSQI_25 = "10e_descriptive"


REPLACE_DICT = {
    "Q_9": {
        "לא התקשיתי כלל": 0,
        "התקשיתי מעט מאוד": 1,
        "די התקשיתי": 2,
        "התקשיתי מאוד": 3,
    },
    "Q_8": {
        "לא במהלך החודש האחרון": 0,
        "פחות מפעם בשבוע": 1,
        "פעם או פעמיים בשבוע": 2,
        "שלוש פעמים או יותר בשבוע": 3,
    },
    "Q_7": {
        "לא במהלך החודש האחרון": 0,
        "פחות מפעם בשבוע": 1,
        "פעם או פעמיים בשבוע": 2,
        "שלוש פעמים או יותר בשבוע": 3,
    },
    "Q_6": {"טובה מאוד": 0, "די טובה": 1, "די גרועה": 2, "גרועה מאוד": 3},
    "Q_5a": {
        "לא במהלך החודש האחרון": 0,
        "פחות מפעם בשבוע": 1,
        "פעם או פעמיים בשבוע": 2,
        "שלוש פעמים או יותר בשבוע": 3,
    },
    "Q_5b": {
        "לא במהלך החודש האחרון": 0,
        "פחות מפעם בשבוע": 1,
        "פעם או פעמיים בשבוע": 2,
        "שלוש פעמים או יותר בשבוע": 3,
    },
    "Q_5c": {
        "לא במהלך החודש האחרון": 0,
        "פחות מפעם בשבוע": 1,
        "פעם או פעמיים בשבוע": 2,
        "שלוש פעמים או יותר בשבוע": 3,
    },
    "Q_5d": {
        "לא במהלך החודש האחרון": 0,
        "פחות מפעם בשבוע": 1,
        "פעם או פעמיים בשבוע": 2,
        "שלוש פעמים או יותר בשבוע": 3,
    },
    "Q_5e": {
        "לא במהלך החודש האחרון": 0,
        "פחות מפעם בשבוע": 1,
        "פעם או פעמיים בשבוע": 2,
        "שלוש פעמים או יותר בשבוע": 3,
    },
    "Q_5f": {
        "לא במהלך החודש האחרון": 0,
        "פחות מפעם בשבוע": 1,
        "פעם או פעמיים בשבוע": 2,
        "שלוש פעמים או יותר בשבוע": 3,
    },
    "Q_5g": {
        "לא במהלך החודש האחרון": 0,
        "פחות מפעם בשבוע": 1,
        "פעם או פעמיים בשבוע": 2,
        "שלוש פעמים או יותר בשבוע": 3,
    },
    "Q_5h": {
        "לא במהלך החודש האחרון": 0,
        "פחות מפעם בשבוע": 1,
        "פעם או פעמיים בשבוע": 2,
        "שלוש פעמים או יותר בשבוע": 3,
    },
    "Q_5i": {
        "לא במהלך החודש האחרון": 0,
        "פחות מפעם בשבוע": 1,
        "פעם או פעמיים בשבוע": 2,
        "שלוש פעמים או יותר בשבוע": 3,
    },
    "Q_5j": {
        "לא במהלך החודש האחרון": 0,
        "פחות מפעם בשבוע": 1,
        "פעם או פעמיים בשבוע": 2,
        "שלוש פעמים או יותר בשבוע": 3,
    },
}


def convert_df(psqi_df: pd.DataFrame):
    psqi_df = psqi_df.replace(REPLACE_DICT)
    for ind_name in psqi_df.index:
        q2 = psqi_df.loc[ind_name, "Q_2"]
        q4 = psqi_df.loc[ind_name, "Q_4"]
        if (q2 <= 15).any():
            psqi_df.loc[ind_name, "Q_2"] = 0
        else:
            if (q2 <= 30).any():
                psqi_df.loc[ind_name, "Q_2"] = 1
            else:
                if (q2 <= 60).any():
                    psqi_df.loc[ind_name, "Q_2"] = 2
                else:
                    psqi_df.loc[ind_name, "Q_2"] = 3
        if (q4 > 7).any():
            psqi_df.loc[ind_name, "Q_4"] = 0
        else:
            if (q4 >= 6).any():
                psqi_df.loc[ind_name, "Q_4"] = 1
            else:
                if (q4 >= 5).any():
                    psqi_df.loc[ind_name, "Q_4"] = 2
                else:
                    psqi_df.loc[ind_name, "Q_4"] = 3
    return psqi_df


def calculate_psqi_scores(psqi_df: pd.DataFrame) -> pd.Series:
    psqi_df = convert_df(psqi_df)
    component_1 = psqi_df["Q_6"]
    component_2 = calculate_component_2(psqi_df["Q_2"] + psqi_df["Q_5a"])
    component_3 = psqi_df["Q_4"]
    component_4 = calculate_component_4(psqi_df[["Q_4", "Q_3", "Q_1"]])
    component_5 = calculate_component_5(
        psqi_df[
            [
                "Q_5a",
                "Q_5b",
                "Q_5c",
                "Q_5d",
                "Q_5e",
                "Q_5f",
                "Q_5g",
                "Q_5h",
                "Q_5i",
            ]
        ]
    )
    component_6 = psqi_df["Q_7"]
    component_7 = calculate_component_7(psqi_df[["Q_8", "Q_9"]])
    psqi_scores = pd.concat(
        [
            component_1,
            component_2,
            component_3,
            component_4,
            component_5,
            component_6,
            component_7,
        ],
        axis=1,
    )
    psqi_scores.columns = [
        "Comp_1",
        "Comp_2",
        "Comp_3",
        "Comp_4",
        "Comp_5",
        "Comp_6",
        "Comp_7",
    ]
    results = psqi_scores.sum(axis=1)
    results.name = "PSQI"
    return results


def calculate_component_7(scores: pd.DataFrame):
    sum_scores = scores.sum(axis=1)
    for i, ind in enumerate(sum_scores.index):
        score = sum_scores[i]
        if score < 1:
            sum_scores[i] = 0
        else:
            if score <= 2:
                sum_scores[i] = 1
            else:
                if score <= 4:
                    sum_scores[i] = 2
                else:
                    sum_scores[i] = 3
    return sum_scores


def calculate_component_5(scores: pd.DataFrame):
    scores_sum = scores.sum(axis=1)
    for i, ind in enumerate(scores_sum.index):
        score = scores_sum[i]
        if score < 1:
            scores_sum[i] = 0
        else:
            if score <= 9:
                scores_sum[i] = 1
            else:
                if score <= 18:
                    scores_sum[i] = 2
                else:
                    scores_sum[i] = 3
    return scores_sum


def get_habitual_sleep_category(value: float) -> int:
    if value >= 0.85:
        return 0
    elif 0.75 <= value < 0.85:
        return 1
    elif 0.65 >= value < 0.75:
        return 2
    else:
        return 3


def calculate_component_4(scores: pd.DataFrame):
    FMT = "%H:%M:%S %p"
    hours_in_bed = []
    habitual_sleep = []
    for i, ind in enumerate(scores.index):
        morning = scores["Q_3"][i]
        evening = scores["Q_1"][i]
        try:
            tdelta = datetime.strptime(morning, FMT) - datetime.strptime(
                evening, FMT
            )
            hours_in_bed.append(tdelta.seconds / 60 / 60)
            value = scores["Q_4"][i] / hours_in_bed[i]
            category = get_habitual_sleep_category(value)
        except Exception:
            category = None
        finally:
            habitual_sleep.append(category)
    return pd.Series(habitual_sleep, index=scores.index)


def calculate_component_2(scores: pd.Series):
    for i, ind in enumerate(scores):
        if ind >= 1:
            if ind <= 2:
                scores[i] = 1
            else:
                if ind <= 4:
                    scores[i] = 2
                else:
                    scores[i] = 3
    return scores
