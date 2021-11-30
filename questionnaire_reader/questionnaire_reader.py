from os import sched_setscheduler
from typing import Tuple

import matplotlib.pyplot as plt
import pandas as pd
from pandas.core.frame import DataFrame
from pandas.plotting import table

from questionnaire_reader.bfi import calculate_bfi
from questionnaire_reader.defaults import COLUMNS, NAMES, REPLACE_DICT
from questionnaire_reader.psqi import PsqiQuestions, calculate_psqi_scores
from questionnaire_reader.shs import (
    SHS_NORMAL_SCORING,
    SHS_REVERSED_SCORING,
    calculate_shs,
)
from questionnaire_reader.utils.freedman_diaconis import freedman_diaconis

DEFAULT_COLORS = plt.rcParams["axes.prop_cycle"].by_key()["color"] + [
    "lightsalmon",
    "greenyellow",
    "hotpink",
    "darkviolet",
]


class QuestionnaireReader:
    def __init__(
        self,
        path: str,
        columns: list = COLUMNS,
        replace_dict: dict = REPLACE_DICT,
    ):
        self.path = path
        self.columns = columns
        self.replace_dict = replace_dict
        self.raw = self.read_data()
        self.data = self.clean_data(self.raw)

    def read_data(self) -> pd.DataFrame:
        return pd.read_csv(
            self.path,
            header=0,
            index_col=1,
            parse_dates=True,
            names=NAMES,
            encoding="utf-8",
        )

    def get_column_name(self, key: str) -> str:
        default = key.title().replace("_", " ")
        return self.columns.get(key, default)

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        clean = self.raw.copy()
        self.fix_height(clean)
        self.replace_values(clean)
        self.fix_attention_deficit(clean)
        clean = self.convert_bfi_responses_to_results(clean)
        clean = self.convert_psqi_responses_to_results(clean)
        clean = self.convert_shs_responses_to_results(clean)
        return clean

    def fix_height(self, df: pd.DataFrame) -> None:
        height_col = self.get_column_name("height")
        height = df[height_col]
        df[height_col] = height.apply(lambda x: x * 100 if x < 3 else x)

    def fix_attention_deficit(self, df: pd.DataFrame) -> None:
        df["Attention Deficit Disorder"] = df[
            "Attention Deficit Disorder"
        ].combine_first(df["Attention Deficit Disorder (1)"])
        df.drop("Attention Deficit Disorder (1)", axis=1, inplace=True)

    def replace_values(self, df: pd.DataFrame) -> None:
        df.replace(self.replace_dict, inplace=True)
        for key, value in self.replace_dict.items():
            df.loc[~df[key].isin(value.values()), key] = "N/A"

    def check_bfi_column_name(self, column_name: str) -> bool:
        return column_name.startswith("BFI")

    def get_bfi_column_names(self, df: pd.DataFrame) -> list:
        return [
            column_name
            for column_name in df.columns
            if self.check_bfi_column_name(column_name)
        ]

    def get_bfi_responses(self, df: pd.DataFrame) -> pd.DataFrame:
        column_names = self.get_bfi_column_names(df)
        bfi = df[column_names].copy()
        bfi.columns = range(len(column_names))
        return bfi

    def get_bfi_scores(self, df: pd.DataFrame) -> pd.Series:
        bfi_responses = self.get_bfi_responses(df)
        return bfi_responses.apply(calculate_bfi, axis=1)

    def convert_bfi_responses_to_results(
        self, df: pd.DataFrame
    ) -> pd.DataFrame:
        bfi_scores = self.get_bfi_scores(df)
        bfi_columns = self.get_bfi_column_names(df)
        df.drop(labels=bfi_columns, axis=1, inplace=True)
        return pd.concat([df, bfi_scores], axis=1)

    def get_psqi_responses(self, df: pd.DataFrame) -> pd.DataFrame:
        psqi = df.iloc[:, 36:62].copy()
        column_names = []
        for i, col in enumerate(psqi.columns):
            question = f"PSQI_{i}"
            column_names.append(f"Q_{PsqiQuestions[question].value}")
        psqi.columns = column_names
        return psqi

    def get_psqi_scores(self, df: pd.DataFrame) -> pd.Series:
        psqi = self.get_psqi_responses(df)
        return calculate_psqi_scores(psqi)

    def convert_psqi_responses_to_results(self, df: pd.DataFrame) -> None:
        psqi_scores = self.get_psqi_scores(df)
        df.drop(labels=df.columns[36:62], axis=1, inplace=True)
        return pd.concat([df, psqi_scores], axis=1)

    def convert_shs_responses_to_results(
        self, df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Calculate SHS scores according to subjects' responses

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame the contains the SHS-relevant columns

        Returns
        -------
        pd.DataFrame
            A single column containing subjects' caclulated SHS score
        """
        shs_scores = calculate_shs(df)
        df = df.drop(SHS_REVERSED_SCORING + SHS_NORMAL_SCORING, axis=1).copy()
        df["SHS"] = shs_scores
        return df

    def calculate_bmi(self, df: pd.DataFrame) -> None:
        return df["Weight (kg)"] / ((df["Height (cm)"] / 100) ** 2)

    def fix_colors(
        self, value_counts: pd.Series, colors: list, by_index: bool = False
    ):
        count_indices = value_counts.index.to_list()
        try:
            na_index = count_indices.index("N/A")
        except ValueError:
            pass
        else:
            colors[na_index] = "lightgrey"
        if by_index:
            colors = [
                color for _, color in sorted(zip(value_counts.index, colors))
            ]
        return colors

    def plot_column_distribution(
        self,
        column_name: str,
        axes: plt.Axes = None,
        title: str = None,
        x_label: str = None,
        y_label: str = None,
        x_range: tuple = None,
        y_range: tuple = None,
        n_bins: int = None,
        kde: bool = True,
        **kwargs,
    ):
        column = self.data[column_name].dropna()
        if axes is None:
            _, axes = plt.subplots(figsize=kwargs.get("figsize"))

        # Plot histogram
        n_bins = n_bins or freedman_diaconis(column)
        DEFAULTS = {
            "bins": n_bins,
            "color": "blue",
            "grid": False,
        }
        configuration = {**DEFAULTS, **kwargs}
        self.data.hist(column=column_name, ax=axes, **configuration)

        # Set title
        axes.set_title(title or f"{column_name} Distribution")

        # Set axis labels
        axes.set_xlabel(x_label or column_name)
        if y_label is None:
            if configuration.get("density"):
                y_label = "Probability Density"
            else:
                y_label = "Number of Observations"
        axes.set_ylabel(y_label)

        # Set axis ranges
        if x_range:
            axes.set_xlim(x_range)
        if y_range:
            axes.set_ylim(y_range)

        # Plot KDE
        if kde and not configuration.get("by"):
            axes_2 = axes.twinx()
            column.plot.kde(ax=axes_2, color="red", legend=False)
            axes_2.set_ylabel("KDE")
            axes_2.set_ylim(0)
        return axes

    def plot_distribution(
        self,
        column_names: list,
        n_rows: int = None,
        n_columns: int = None,
        title: str = None,
        subplot_titles: list = None,
        x_labels: list = None,
        y_labels: list = None,
        x_range: tuple = None,
        y_range: tuple = None,
        sharex: bool = True,
        kde: bool = True,
        **kwargs,
    ):
        n_rows = n_rows or len(column_names)
        n_columns = n_columns or 1
        empty = [""] * n_rows * n_columns
        subplot_titles = subplot_titles or empty
        x_labels = x_labels or empty
        y_labels = y_labels or empty
        fig, axes = plt.subplots(
            nrows=n_rows,
            ncols=n_columns,
            figsize=kwargs.get("figsize"),
            sharex=sharex,
        )
        for i, ax in enumerate(fig.axes):
            try:
                column_name = column_names[i]
            except IndexError:
                ax.axis("off")
            else:
                self.plot_column_distribution(
                    column_name,
                    axes=ax,
                    title=subplot_titles[i],
                    x_label=x_labels[i],
                    y_label=y_labels[i],
                    x_range=x_range,
                    y_range=y_range,
                )
        return fig

    def plot_pie_chart(
        self,
        column_name: str,
        radius: float = 2.5,
        percentage_template: str = "%1.1f%%",
        percentage_distance: float = 0.75,
        counterclock: bool = False,
        colors: list = None,
        ax: plt.Axes = None,
    ) -> plt.Axes:
        colors = colors or DEFAULT_COLORS.copy()
        value_counts = self.data[column_name].value_counts()
        return value_counts.plot.pie(
            autopct=percentage_template,
            pctdistance=percentage_distance,
            radius=radius,
            counterclock=counterclock,
            colors=colors,
            ax=ax,
        )

    def plot_pie_chart_with_table(
        self,
        column_name: str,
        radius: float = 1.25,
        percentage_template: str = "%1.1f%%",
        percentage_distance: float = 0.75,
        counterclock: bool = False,
        colors: list = None,
    ):
        colors = colors or DEFAULT_COLORS.copy()
        value_counts = self.data[column_name].value_counts()
        colors = self.fix_colors(value_counts, colors)
        figure, axes = plt.subplots(ncols=2, figsize=(16, 6))
        pie_chart = self.plot_pie_chart(
            column_name=column_name,
            radius=radius,
            percentage_template=percentage_template,
            percentage_distance=percentage_distance,
            counterclock=counterclock,
            colors=colors,
            ax=axes[0],
        )
        axes[1].axis("off")
        table_ = table(
            axes[1],
            value_counts,
            bbox=[0.5, 0.25, 0.5, 0.75],
            rowColours=colors,
        )
        table_.set_fontsize(14)
        return pie_chart, table_

    def plot_bar_chart(
        self,
        column_name: str,
        figure_size: Tuple[int] = (16, 6),
        title: str = None,
        colors: list = None,
        x_label: str = "Values",
        y_label: str = "Count",
    ) -> plt.Axes:
        value_counts = self.data[column_name].value_counts()
        sorted_counts = value_counts.sort_index()
        colors = colors or DEFAULT_COLORS.copy()
        colors = self.fix_colors(value_counts, colors, by_index=True)
        title = title if title is not None else column_name
        plot = sorted_counts.plot(
            kind="bar", figsize=figure_size, title=title, color=colors
        )
        plot.set_xlabel(x_label)
        plot.set_ylabel(y_label)
        return plot
