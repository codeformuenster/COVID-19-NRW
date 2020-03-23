import plotly.graph_objects as go  # plots
import pandas
import locale
import glob
import os

daily_report_files = glob.glob('data/daily_reports/*.csv')

all_data = pandas.DataFrame({'Kommune': [],
                            'Last Update Day': [],
                            'Last Update Time': [],
                            'Confirmed': [],
                            'Deaths': [],
                            'Recovered': [],
                            'Quarantine': [],
                            'Source (Link)': []
                            })

for f in daily_report_files:
  all_data = pandas.concat([pandas.read_csv(f), all_data], sort=False)

all_data['Last Update Day'] = pandas.to_datetime(all_data['Last Update Day'])
all_data['Last Update Time'] = pandas.to_datetime(all_data['Last Update Time'])
all_data['Confirmed'] = all_data['Confirmed'].astype(int)
all_data['Recovered'] = all_data['Recovered'].astype(int)
all_data['Deaths'] = all_data['Deaths'].astype(int)
# ~ all_data['Deaths'] = all_data['Quarantine'].astype(int)

all_data = all_data.sort_values(by='Last Update Day')

confirmed_df = pandas.DataFrame({'Kommune': all_data['Kommune'].unique()})
recovered_df = pandas.DataFrame({'Kommune': all_data['Kommune'].unique()})
deaths_df = pandas.DataFrame({'Kommune':  all_data['Kommune'].unique()})

confirmed_df = confirmed_df.set_index('Kommune', drop=True)
recovered_df = recovered_df.set_index('Kommune', drop=True)
deaths_df = deaths_df.set_index('Kommune', drop=True)


for day in all_data['Last Update Day'].dt.date.unique():

  for kommune in all_data['Kommune'].unique():
    all_data_kommune = all_data[all_data['Kommune'] == kommune]

    c = all_data_kommune[all_data_kommune['Last Update Day'] == pandas.Timestamp(day)]['Confirmed'].values
    r = all_data_kommune[all_data_kommune['Last Update Day'] == pandas.Timestamp(day)]['Recovered'].values
    d = all_data_kommune[all_data_kommune['Last Update Day'] == pandas.Timestamp(day)]['Deaths'].values
    
    if len(c) == 1:
      confirmed_df.loc[kommune, day] = c

    if len(r) == 1:
      recovered_df.loc[kommune, day] = r
      
    if len(d) == 1:
      deaths_df.loc[kommune, day] = d

confirmed_df.to_csv("data/time_series/time_series_covid-19_nrw_confirmed.csv")
recovered_df.to_csv("data/time_series/time_series_covid-19_nrw_recovered.csv")
deaths_df.to_csv("data/time_series/time_series_covid-19_nrw_deaths.csv")

locale.setlocale(locale.LC_ALL, 'de_DE')

# ~ for kommune_idx in range(len(confirmed_df)):
# ~ for kommune, row in confirmed_df.iterrows():
    
for kommune in all_data['Kommune'].unique():

  # create plot
  fig = go.Figure()

  # ~ kommune = confirmed_df.iloc[kommune_idx, 0]
  
  print(kommune)

  # ~ print(kommune_idx)

  all_data_kommune = all_data[all_data['Kommune'] == kommune]
  
  # ~ confirmed_ts = confirmed_df.iloc[kommune, 2:].T
  # ~ recovered_ts = recovered_df.iloc[kommune, 2:].T
  # ~ deaths_ts = deaths_df.iloc[kommune, 2:].T
  
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
          mode="lines+markers",
          legendgroup=kommune,
          line=dict(color="black", width=4),
          marker=dict(size=10),
          hovertemplate="Todesfälle " + kommune + ", %{x}: %{y}"
            + "<extra></extra>" # no additional legend text in tooltip
      )  
  )

  last_update_date = str(all_data_kommune.iloc[-1]['Last Update Day'].strftime('%d. %B'))
  last_update_time = str(all_data_kommune.iloc[-1]['Last Update Time'].hour)
  last_update_source = str(all_data_kommune.iloc[-1]['Source (Link)'])

  fig.update_layout(
    title="Coronafälle in " + kommune + " (Stand: " + last_update_date + ", " + last_update_time + 
    " Uhr)<br><a href='" + last_update_source + "'>Quelle (klick!)</a>",
    xaxis_title="Datum",
    yaxis_title="Fälle",
    legend_orientation="h",
    # disable dragmode for better mobile experience
    dragmode=False,
    font=dict(size=22)
)

  # write plot to file
  fig.write_html(kommune+".html",
    include_plotlyjs="cdn",
    config={"displayModeBar": False,
            "locale": "de"},
    auto_open=True
  )

os.system("python plot_barchart.py")

