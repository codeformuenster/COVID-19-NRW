from functools import reduce

import pandas as pd
import numpy as np

import seaborn as sns

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


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
    df_confirmed.dropna(subset=["confirmed"], inplace=True)

    df_confirmed["date"] = pd.to_datetime(df_confirmed["date"])
    df_confirmed["confirmed_delta"] = df_confirmed["confirmed"].diff()
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

    df = df[df.confirmed >= 10].reset_index()

    df["active"] = df["confirmed"] - df["recovered"] - df["deaths"]
    df["active_delta"] = df_deaths["deaths"].diff()
    df["active_change_rate"] = df_deaths["deaths"].pct_change()

    return df


def plot(kommune):
    df = load(kommune)

    sns.set(style="whitegrid")

    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(12, 10))

    # Plot the total cases
    sns.set_color_codes("pastel")
    plot_confirmed = sns.barplot(
        x="date", y="confirmed", data=df, label="gesamt", color="#05516D"
    )

    for index, row in df.iterrows():
        plot_confirmed.text(
            row.name,
            row.confirmed,
            int(row.confirmed),
            va="center",
            color="black",
            ha="center",
        )

    # Plot active cases
    plot_confirmed_delta = sns.barplot(
        x="date", y="confirmed_delta", data=df, label="Neuinfektionen", color="#05516D"
    )

    for index, row in df.iterrows():
        x = row.name
        y = 0 if row.confirmed_delta == np.isnan else row.confirmed_delta
        text = int(row.confirmed_delta) if row.confirmed_delta >= 5 else ""
        plot_confirmed_delta.text(
            x, y, text, va="bottom", color="black", ha="center",
        )

    plot_confirmed_delta.patches[0].set_hatch("\\")

    # Plot active
    sns.set_color_codes("muted")
    plot_active = sns.barplot(
        x="date", y="active", data=df, label="Infizierte", color="#E5F3FC"
    )

    for index, row in df.iterrows():
        x = row.name
        y = 0 if row.active == np.isnan else row.active
        text = int(row.active) if row.active >= 5 else ""
        plot_active.text(
            x, y, text, va="bottom", color="black", ha="center",
        )

    plot_recovered = sns.barplot(
        x="date", y="recovered", data=df, label="Genesene", color="g"
    )

    # for index, row in df.iterrows():
    # x = row.name - 1
    # y = 0 if row.confirmed_delta == np.isnan else row.confirmed_delta
    # text = int(row.confirmed_delta) if row.confirmed_delta >= 5 else ""
    # plot_confirmed.text(
    # x, y, text, va="bottom", color="black", ha="center",
    # )

    plot_deaths = sns.barplot(
        x="date", y="deaths", data=df, label="Todesfälle", color="#DD6600"
    )

    # for index, row in df.iterrows():
    # x = row.name - 1
    # y = 0 if row.confirmed_delta == np.isnan else row.confirmed_delta
    # text = int(row.confirmed_delta) if row.confirmed_delta >= 5 else ""
    # plot_confirmed.text(
    # x, y, text, va="bottom", color="black", ha="center",
    # )

    # No bar borders
    plt.setp(ax.patches, linewidth=0)
    # Add a legend and informative axis label

    ax.legend(ncol=3, loc="best", frameon=False)

    # ax.text(
    # 0.02,
    # 0.98,
    # "Entwicklung von COVID-19-Erkankungen, " + kommune,
    # ha="left",
    # va="top",
    # transform=ax.transAxes,
    # )
    ax.set_xlabel("")
    ax.set_ylabel("")
    x_labels = df["date"].dt.strftime("%d.%m.")
    ax.set_xticklabels(labels=x_labels, rotation=45, ha="right")
    sns.despine(left=True, bottom=True)
    ax.set(yticks=np.arange(0, max(df["confirmed"]) + 50, step=20))

    return f


def save():
    df_raw = pd.read_csv("data/time_series/time_series_covid-19_nrw_confirmed.csv")
    kommunen = df_raw["Kommune"].unique()

    for kommune in kommunen:
        print(kommune)

        kommune_short = str.split(kommune)[1].lower()

        fig = plot(kommune)
        image_name = "images/covid-19-" + kommune_short + ".svg"
        fig.savefig(image_name)
        f = open("diff_plot_" + kommune_short + "_temp.html", "w")
        f.write('<div style="text-align: center;">')
        f.write("<img src='" + image_name + "'/>")
        f.write("</div>")
        f.close()


if __name__ == "__main__":
    save()
