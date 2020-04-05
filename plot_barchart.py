from functools import reduce

import pandas as pd
import numpy as np

import seaborn as sns

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


# set jupyter's max row display
pd.set_option('display.max_row', 1000)

# set jupyter's max column width to 50
pd.set_option('display.max_columns', 50)

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

    # idx_first_day_with_100_confirmed = df[df['confirmed'] >= 100].index.min()
    # df = df.iloc[idx_first_day_with_100_confirmed:-1]


    idx_last_entry = df.index.max()
    idx_doubled_since = df[df['confirmed'] <= max(df['confirmed'] / 2)].index.max()

    last_entry_date = df.loc[idx_last_entry]['date']
    doubled_since_date = df.loc[idx_doubled_since]['date']

    doubled_since_in_days = (last_entry_date - doubled_since_date).days - 1

    ax = df.plot.bar(x='date', y=['confirmed_yesterday', 'confirmed_new'], stacked=True, color=['#2792cb', '#00548b'], figsize=(20,10), width=0.8, fontsize=13, edgecolor='#2792cb', linewidth=2 )

    for index, row in df.iterrows():
        text = ('+\n{:.0%}'.format(row['confirmed_change_rate']))
        ax.text(index -.30, df['confirmed'].loc[index] - 13.0, \
                text, fontsize=10, color='#FFFFFF')

    for index, row in df.iterrows():
        text = int(row['confirmed'])
        ax.text(index -.30, df['confirmed'].loc[index] / 2 + 3.0, \
                text, fontsize=10, color='#FFFFFF')

    # for index, row in df.iterrows():
        # text = ('{:.1%}'.format(row['confirmed_change_rate']))
        # ax.annotate(text,(index ,df['confirmed'].loc[index]))

    # df_new = df[['date', 'deaths', 'recovered', 'confirmed_yesterday', 'confirmed_new']]
    # ax = df_new.plot.bar(x='date', stacked=True, color=['#dd6600','#dbcd00', '#2792cb', '#00548b'])

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_xlabel("")
    ax.set_ylabel("Fälle", fontsize=15)
    ax.yaxis.set_label_position("right")
    x_labels = df["date"].dt.strftime("%d.%m.")
    ax.set_xticklabels(labels=x_labels, rotation=45, ha="right")
    ax.set(yticks=np.arange(0, max(df["confirmed"]) + 50, step=100))
    ax.yaxis.tick_right()
    ax.legend(['Infizierte', 'Neuinfektionen zum Vortag'], frameon=False)
    ax.hlines(max(df['confirmed']), idx_doubled_since, idx_last_entry, linestyles='-', lw=1, color='#00548b')
    ax.vlines(idx_doubled_since, max(df['confirmed']), max(df['confirmed'] / 2), linestyles='-', lw=1, color='#00548b')
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
