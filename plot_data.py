import plotly.graph_objects as go  # plots
import pandas
import numpy
import os
import locale

locale.setlocale(locale.LC_ALL, 'de_DE.utf8')

os.system("python plot_barchart.py")

confirmed_df = pandas.read_csv("data/time_series/time_series_covid-19_nrw_confirmed.csv")
recovered_df = pandas.read_csv("data/time_series/time_series_covid-19_nrw_recovered.csv")
deaths_df = pandas.read_csv("data/time_series/time_series_covid-19_nrw_deaths.csv")

confirmed_df = confirmed_df.set_index(['Kommune'], drop=True)
recovered_df = recovered_df.set_index(['Kommune'], drop=True)
deaths_df = deaths_df.set_index(['Kommune'], drop=True)

for kommune in confirmed_df.index.unique():

  # create plot
  fig = go.Figure()

  kommune_short = str.split(kommune)[1].lower()
  
  confirmed_ts = confirmed_df.loc[kommune, :].T
  recovered_ts = recovered_df.loc[kommune, :].T
  deaths_ts = deaths_df.loc[kommune, :].T

  confirmed_ts.index = pandas.to_datetime(confirmed_ts.index)
  recovered_ts.index = pandas.to_datetime(recovered_ts.index)
  deaths_ts.index = pandas.to_datetime(deaths_ts.index)

  fig.add_trace(
    go.Scatter(
        x=confirmed_ts.index,
        y=confirmed_ts,
        name="Infektionen " + kommune,
        connectgaps=True,
        mode="lines+markers",
        legendgroup=kommune,
        line=dict(color="orange", width=4),
        marker=dict(size=10),
        hovertemplate="Infektionen " + kommune + ", %{x}: %{y}"
          + "<extra></extra>" # no additional legend text in tooltip
    )
  )

  fig.add_trace(
    go.Scatter(
        x=recovered_ts.index,
        y=recovered_ts,
        name="Genesene " + kommune,
        connectgaps=True,
        mode="lines+markers",
        legendgroup=kommune,
        line=dict(color="green", width=4),
        marker=dict(size=10),
        hovertemplate="genesen " + kommune + ", %{x}: %{y}"
          + "<extra></extra>" # no additional legend text in tooltip
    )
  )

  fig.add_trace(
      go.Scatter(
          x=deaths_ts.index,
          y=deaths_ts,
          name="Todesfälle " + kommune,
          connectgaps=True,
          mode="lines+markers",
          legendgroup=kommune,
          line=dict(color="black", width=4),
          marker=dict(size=10),
          hovertemplate="Todesfälle " + kommune + ", %{x}: %{y}"
            + "<extra></extra>" # no additional legend text in tooltip
      )  
  )

  last_update_date = max(confirmed_ts.index).strftime('%d. %B') #str(all_data_kommune.iloc[-1]['Last Update Day'].strftime('%d. %B'))
  # ~ last_update_source = str(all_data_kommune.iloc[-1]['Source (Link)'])

  fig.update_layout(
    title="Coronafälle<br>" + kommune + " (Stand: " + last_update_date + ")",
    xaxis_title="Datum",
    yaxis_title="Fälle",
    legend_orientation="h",
    # disable dragmode for better mobile experience
    dragmode=False,
    font=dict(size=22),
    xaxis_tickformat = '%d. %B',
  )

  # write plot to file
  fig.write_html(kommune_short.lower()+'_temp.html',
    include_plotlyjs=False,
    full_html=False,
    config={"displayModeBar": False,
            "locale": "de"}
    # ~ auto_open=True
  )

  fig.add_trace(
      go.Scatter(
          x=confirmed_ts.index,
          y=2**((confirmed_ts.index - confirmed_ts.index[0]).days/2),
          name="Verdoppelung alle 2 Tage",
          connectgaps=True,
          mode="lines",
          line=dict(color="grey", width=4, dash='dash'),
          marker=dict(size=10),
          hovertemplate="Verdopplung alle 2 Tage"
            + "<extra></extra>" # no additional legend text in tooltip
      )  
  )

  fig.add_trace(
      go.Scatter(
          x=confirmed_ts.index,
          y=2**((confirmed_ts.index - confirmed_ts.index[0]).days/3),
          name="Verdoppelung alle 3 Tage ",
          connectgaps=True,
          mode="lines",
          line=dict(color="grey", width=4, dash='dash'),
          marker=dict(size=10),
          hovertemplate="Verdopplung alle 3 Tage"
            + "<extra></extra>" # no additional legend text in tooltip
      )  
  )

  fig.add_trace(
      go.Scatter(
          x=confirmed_ts.index,
          y=2**((confirmed_ts.index - confirmed_ts.index[0]).days/5),
          name="Verdoppelung alle 5 Tage ",
          connectgaps=True,
          mode="lines",
          line=dict(color="grey", width=4, dash='dash'),
          marker=dict(size=10),
          hovertemplate="Verdopplung alle 5 Tage"
            + "<extra></extra>" # no additional legend text in tooltip
      )  
  )

  fig.add_trace(
      go.Scatter(
          x=confirmed_ts.index,
          y=2**((confirmed_ts.index - confirmed_ts.index[0]).days/10),
          name="Verdoppelung alle 10 Tage ",
          connectgaps=True,
          mode="lines",
          line=dict(color="grey", width=4, dash='dash'),
          marker=dict(size=10),
          hovertemplate="Verdopplung alle 10 Tage"
            + "<extra></extra>" # no additional legend text in tooltip
      )  
  )
  
  fig.update_layout(
    title="Coronafälle, logarithmisch<br>" + kommune + " (Stand: " + last_update_date + ")",
    xaxis_title="Datum",
    yaxis_title="Fälle (logarithmische Skala)",
    legend_orientation="h",
    # disable dragmode for better mobile experience
    dragmode=False,
    font=dict(size=22),
    xaxis_tickformat = '%d. %B',
    yaxis_type="log"
  )
   
  # write plot to file
  fig.write_html(kommune_short.lower()+'_log_temp.html',
    include_plotlyjs=False,
    full_html=False,
    config={"displayModeBar": False,
            "locale": "de"}
    # ~ auto_open=True
  )
  
  filenames = ['header.html', kommune_short.lower()+'_temp.html', 'diff_plot_' + kommune_short.lower() + '_temp.html', kommune_short.lower()+'_temp_log.html', 'footer.html']
  with open(kommune_short.lower()+'.html', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)

os.system("rm *_temp.html")
