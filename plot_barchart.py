import pandas as pd
import numpy as np

import seaborn as sns

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


matplotlib.use("agg")


def plot(kommune):
    df_raw = pd.read_csv("data/time_series/time_series_covid-19_nrw_confirmed.csv")
    df_raw = df_raw[df_raw.Kommune == kommune]
    df = (
        df_raw.transpose()
        .reset_index()
        .drop([0])
        )
        # ~ .rename(columns={"index": "date", 0: "confirmed"})
    # ~ )
    df.columns = ['date', 'confirmed']
    df = df.dropna(subset=['confirmed'])
    df["date"] = pd.to_datetime(df["date"])
    df["new_cases"] = df["confirmed"].diff()
    df["change"] = df["confirmed"].pct_change()
    sns.set(style="whitegrid")

    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(12, 10))

    # Plot the total cases
    sns.set_color_codes("pastel")
    plot_confirmed = sns.barplot(
        x="date", y="confirmed", data=df, label="gesamt", color="b"
    )

    for index, row in df.iterrows():
        plot_confirmed.text(
            row.name - 1,
            row.confirmed,
            int(row.confirmed),
            va="bottom",
            color="black",
            ha="center",
        )

    # Plot the crashes where alcohol was involved
    sns.set_color_codes("muted")
    plot_new_cases = sns.barplot(
        x="date", y="new_cases", data=df, label="Neuerkrankungen", color="b"
    )

    for index, row in df.iterrows():
        x = row.name - 1
        y = 0 if row.new_cases == np.isnan else row.new_cases
        text = int(row.new_cases) if row.new_cases >= 5 else ""
        plot_confirmed.text(
            x, y, text, va="bottom", color="black", ha="center",
        )

    # Add a legend and informative axis label
    ax.legend(ncol=2, loc="best", frameon=False)

    ax.text(
        0.02,
        0.98,
        "Entwicklung von COVID-19-Erkankungen, " + kommune,
        ha="left",
        va="top",
        transform=ax.transAxes,
    )
    ax.set_xlabel("")
    ax.set_ylabel("")
    x_labels = df["date"].dt.strftime("%d.%m.")
    ax.set_xticklabels(labels=x_labels, rotation=45, ha="right")
    sns.despine(left=True, bottom=True)
    ax.set(yticks=np.arange(0, max(df["confirmed"])+50, step=20))

    return f


def save():
    df_raw = pd.read_csv("data/time_series/time_series_covid-19_nrw_confirmed.csv")

    for kommune in df_raw['Kommune'].unique():

      kommune_short = str.split(kommune)[1].lower()
  
      fig = plot(kommune)
      image_name = "images/covid-19-" + kommune_short + ".svg"
      fig.savefig(image_name)
      f = open("diff_plot_" + kommune_short + "_temp.html", "w")
      f.write("<div>")
      f.write("<img src='" + image_name + "'/>")
      f.write("</div>")
      f.close()


if __name__ == "__main__":
    save()
