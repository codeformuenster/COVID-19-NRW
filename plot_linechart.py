from functools import reduce

import pandas as pd
import numpy as np

import seaborn as sns

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


# set jupyter's max row display
pd.set_option("display.max_row", 1000)

# set jupyter's max column width to 50
pd.set_option("display.max_columns", 50)

matplotlib.use("agg")


def load(kommune):
    df_confirmed_raw = pd.read_csv(
        "data/time_series/time_series_covid-19_nrw_confirmed.csv"
    )
    df_confirmed = (
        df_confirmed_raw[df_confirmed_raw.Kommune == kommune]
        .transpose()
        .reset_index()
        .drop([0])
    )

    df_confirmed.columns = ["date", "confirmed"]
    # df_confirmed.dropna(subset=["confirmed"], inplace=True)

    df_confirmed["date"] = pd.to_datetime(df_confirmed["date"])
    df_confirmed["confirmed_yesterday"] = (
        df_confirmed["confirmed"] - df_confirmed["confirmed"].diff()
    )
    df_confirmed["confirmed_new"] = df_confirmed["confirmed"].diff()
    df_confirmed["confirmed_change_rate"] = df_confirmed["confirmed"].pct_change()

    df_recovered_raw = pd.read_csv(
        "data/time_series/time_series_covid-19_nrw_recovered.csv"
    )

    df_recovered = (
        df_recovered_raw[df_recovered_raw.Kommune == kommune]
        .transpose()
        .reset_index()
        .drop([0])
    )

    df_recovered.columns = ["date", "recovered"]
    df_recovered.dropna(subset=["recovered"], inplace=True)

    df_recovered["date"] = pd.to_datetime(df_recovered["date"])
    df_recovered["recovered_delta"] = df_recovered["recovered"].diff()
    df_recovered["recovered_change_rate"] = df_recovered["recovered"].pct_change()

    df_deaths_raw = pd.read_csv("data/time_series/time_series_covid-19_nrw_deaths.csv")

    df_deaths = (
        df_deaths_raw[df_deaths_raw.Kommune == kommune]
        .transpose()
        .reset_index()
        .drop([0])
    )

    df_deaths.columns = ["date", "deaths"]
    df_deaths.dropna(subset=["deaths"], inplace=True)

    df_deaths["date"] = pd.to_datetime(df_deaths["date"])
    df_deaths["deaths_delta"] = df_deaths["deaths"].diff()
    df_deaths["deaths_change_rate"] = df_deaths["deaths"].pct_change()

    dfs = [df_confirmed, df_recovered, df_deaths]
    df = reduce(lambda left, right: pd.merge(left, right, on="date"), dfs)

    # df = df[df.confirmed >= 10].reset_index()

    df["active"] = df["confirmed"] - df["recovered"] - df["deaths"]
    df["active_without_new"] = df["confirmed"] - df["recovered"] - df["deaths"] - df['confirmed_new']
    df["active_delta"] = df_deaths["deaths"].diff()
    df["active_change_rate"] = df_deaths["deaths"].pct_change()

    return df


def plot(kommune):
    # kommune = "Stadt Münster"

    df = load(kommune)

    ax = df.plot.line(
        x="date",
        y=["recovered", "active"],
        style='.-',
        color=["#dbcd00", "#2792cb"],
        figsize=(20, 10),
        fontsize=13,
        linewidth=2,
    )

    ax.grid(axis='y')
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("")
    ax.set_ylabel("Anzahl von Fällen", fontsize=12)
    ax.yaxis.set_label_position("left")
    x_labels = df["date"].dt.strftime("%d.%m.")
    ax.set(yticks=np.arange(0, max(df["confirmed"]) + 50, step=100))
    ax.yaxis.tick_left()
    ax.legend(["Genesene", "Erkrankte"], frameon=False)

    return ax.get_figure()


def save():
    df_raw = pd.read_csv("data/time_series/time_series_covid-19_nrw_confirmed.csv")
    kommunen = df_raw["Kommune"].unique()

    for kommune in kommunen:
        print(kommune)

        kommune_short = str.split(kommune)[1].lower()

        fig = plot(kommune)
        image_name = "images/covid-19-" + kommune_short + '_line' + ".svg"
        fig.savefig(image_name, bbox_inches='tight')
        f = open("diff_plot_" + kommune_short + '_line' + "_temp.html", "w")
        f.write('<div style="text-align: center;">')
        f.write("<img src='" + image_name + "'/>")
        f.write("</div>")
        f.close()


if __name__ == "__main__":
    save()
