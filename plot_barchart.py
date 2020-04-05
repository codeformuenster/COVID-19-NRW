from functools import reduce
from datetime import datetime as dt

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
    def plot_label(df, ax):
        for index, row in df.iterrows():
            # text = "{:.0%}".format(row["confirmed_change_rate"])
            if (row['date'] >= dt.strptime("2020-03-13", "%Y-%m-%d")):
                if not np.isnan(row['confirmed_new']):
                    text = '%.0f' % row["confirmed_new"]

                    ax.text(
                        index,
                        df['recovered'].loc[index] + df["active"].loc[index] - df["confirmed_new"].loc[index] + 3,
                        text,
                        horizontalalignment='center',
                        fontsize=10,
                        color="#FFFFFF",
                    )

        for index, row in df.iterrows():
            if (row['date'] >= dt.strptime("2020-03-14", "%Y-%m-%d")):
                text = int(row["active"])
                ax.text(
                    index,
                    df['recovered'].loc[index] + df["active"].loc[index] / 2,
                    text,
                    horizontalalignment='center',
                    fontsize=10,
                    color="#FFFFFF",
                )

        for index, row in df.iterrows():
            if (row['date'] >= dt.strptime("2020-03-14", "%Y-%m-%d")):
                text = int(row["recovered"])
                ax.text(
                    index,
                    df["recovered"].loc[index] / 2 + 3.0,
                    text,
                    horizontalalignment='center',
                    fontsize=10,
                    color="#FFFFFF",
                )

    def plot_doubled_since(df, ax):
        idx_last_entry = df.index.max()

        has_doubled = df["confirmed"] <= max(df["confirmed"] / 2)

        if has_doubled.any():
            idx_doubled_since = df[has_doubled].index.max()
            last_entry_date = df.loc[idx_last_entry]["date"]
            doubled_since_date = df.loc[idx_doubled_since]["date"]

            doubled_since_in_days = (last_entry_date - doubled_since_date).days - 1

            ax.hlines(
                max(df["confirmed"]),
                idx_doubled_since,
                idx_last_entry,
                linestyles='dashed',
                lw=1,
                color="#00548b",
            )
            ax.vlines(
                idx_doubled_since,
                max(df["confirmed"]),
                max(df["confirmed"] / 2),
                linestyles="dashed",
                lw=1,
                color="#00548b",
            )
            # ax.axvline(12, 0.2, 0.8, color='k', linestyle='--')
            ax.annotate(
                f"Letzte Verdoppelung: \n{doubled_since_in_days} Tage",
                (idx_doubled_since + 0.5 , max(df["confirmed"] / 1.1)),
            )

    def plot_axis(ax):
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.set_xlabel("")
        ax.set_ylabel("Anzahl an Fällen", fontsize=12)
        ax.yaxis.set_label_position("right")
        x_labels = df["date"].dt.strftime("%d.%m.")
        ax.set_xticklabels(labels=x_labels, rotation=45, ha="right")
        ax.set(yticks=np.arange(0, max(df["confirmed"]) + 50, step=100))
        ax.yaxis.tick_right()

    def plot_legend(ax):
        ax.legend(["Genesene", "Erkrankte", "Anteil von Neuinfektionen an Erkrankten"], frameon=False)

    def plot_bar(df):
        return df.plot.bar(
            x="date",
            y=["recovered", "active_without_new", "confirmed_new"],
            stacked=True,
            color=["#dbcd00", "#2792cb", "#00548b"],
            figsize=(20, 10),
            width=0.8,
            fontsize=13,
            linewidth=2,
        )


    df = load(kommune)
    ax = plot_bar(df)
    plot_label(df, ax)
    plot_axis(ax)
    plot_legend(ax)
    plot_doubled_since(df, ax)

    return ax.get_figure()


def save():
    def get_kommunen():
        df_raw = pd.read_csv("data/time_series/time_series_covid-19_nrw_confirmed.csv")
        return df_raw["Kommune"].unique()

    def get_short_name(kommune):
        return str.split(kommune)[1].lower()

    def get_image_name(short_name):
        return "images/covid-19-" + short_name + ".svg"

    def save_plotted_svg(kommune, image_name):
        fig = plot(kommune)
        fig.savefig(image_name, bbox_inches='tight')

    def generate_html(short_name, image_name):
        f = open("diff_plot_" + short_name + "_temp.html", "w")
        f.write('<div style="text-align: center;">')
        f.write("<img src='" + image_name + "'/>")
        f.write("</div>")
        f.close()


    kommunen = get_kommunen()

    for kommune in kommunen:
        print(kommune)

        short_name = get_short_name(kommune)
        image_name = get_image_name(short_name)

        save_plotted_svg(kommune, image_name)
        generate_html(short_name, image_name)


if __name__ == "__main__":
    save()
