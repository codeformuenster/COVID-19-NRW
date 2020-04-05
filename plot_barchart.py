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
    # df_confirmed.dropna(subset=["confirmed"], inplace=True)

    df_confirmed["date"] = pd.to_datetime(df_confirmed["date"])
    df_confirmed["confirmed_yesterday"] = df_confirmed['confirmed'] - df_confirmed['confirmed'].diff()
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
    df["active_delta"] = df_deaths["deaths"].diff()
    df["active_change_rate"] = df_deaths["deaths"].pct_change()

    return df


def plot_pd(df):
    kommune = 'Stadt Münster'
    df = load(kommune)

    idx_last_entry = df.index.max()
    idx_doubled_since = df[df['confirmed'] <= max(df['confirmed'] / 2)].index.max()

    last_entry_date = df.iloc[idx_last_entry]['date']
    doubled_since_date = df.iloc[idx_doubled_since]['date']

    doubled_since_in_days = (last_entry_date - doubled_since_date).days - 1

    ax = df.plot.bar(x='date', y=['confirmed_yesterday', 'confirmed_new'], stacked=True, color=['#2792cb', '#00548b'], figsize=(12,10) )

    # df_new = df[['date', 'deaths', 'recovered', 'confirmed_yesterday', 'confirmed_new']]
    # ax = df_new.plot.bar(x='date', stacked=True, color=['#dd6600','#dbcd00', '#2792cb', '#00548b'])

    ax.set_xlabel("")
    ax.set_ylabel("Fälle")
    x_labels = df["date"].dt.strftime("%d.%m.")
    ax.set_xticklabels(labels=x_labels, rotation=45, ha="right")
    ax.set(yticks=np.arange(0, max(df["confirmed"]) + 50, step=100))
    ax.legend(['Infizierte', 'Neuinfizierte'], frameon=False)
    ax.hlines(max(df['confirmed']), idx_doubled_since, idx_last_entry, linestyles='-', lw=1)
    ax.vlines(idx_doubled_since, max(df['confirmed']), max(df['confirmed'] / 2), linestyles='-', lw=1)
    # ax.axvline(12, 0.2, 0.8, color='k', linestyle='--')
    ax.annotate(f"Letzte Verdoppelung: \n{doubled_since_in_days} Tage",(idx_doubled_since -5 ,max(df['confirmed'] / 1.5)))


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
