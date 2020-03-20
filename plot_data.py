import plotly.graph_objects as go  # plots
import pandas


confirmed = pandas.read_csv("data/time_series/time_series_covid-19_nrw_confirmed.csv")
recovered = pandas.read_csv("data/time_series/time_series_covid-19_nrw_recovered.csv")
deaths = pandas.read_csv("data/time_series/time_series_covid-19_nrw_deaths.csv")

# create plot
fig = go.Figure()

for kommune_idx in range(len(confirmed)):  

  kommune = confirmed.iloc[kommune_idx, 0]
  
  confirmed_ts = confirmed.iloc[kommune_idx, 2:].T  
  recovered_ts = recovered.iloc[kommune_idx, 2:].T
  deaths_ts = deaths.iloc[kommune_idx, 2:].T

  print(confirmed_ts)

  fig.add_trace(
    go.Scatter(
        x=confirmed_ts.index,
        y=confirmed_ts,
        name="Infektionen " + kommune,
        mode="lines+markers",
        legendgroup=kommune,
        # ~ text="test",
        line=dict(color="orange"),
        hovertemplate="Infektionen",
        # ~ + "<extra></extra>",
    )  # no additional legend text in tooltip
    )

  fig.add_trace(
    go.Scatter(
        x=recovered_ts.index,
        y=recovered_ts,
        name="Genesene " + kommune,
        mode="lines+markers",
        legendgroup=kommune,
        # ~ text=subdf_real.percentage,
        line=dict(color="green"),
        hovertemplate="genesen"
        + "<extra></extra>",
    )  # no additional legend text in tooltip
  )

  fig.add_trace(
      go.Scatter(
          x=deaths_ts.index,
          y=deaths_ts,
          name="Todesfälle " + kommune,
          mode="lines+markers",
          legendgroup=kommune,
          # ~ text=subdf_real.percentage,
          line=dict(color="black"),
          hovertemplate="Todesfälle"
          + "<extra></extra>",
      )  # no additional legend text in tooltip
  )

fig.update_layout(
  title="Coronafälle in Münster",
  xaxis_title="Datum",
  yaxis_title="Fälle",
  # disable dragmode for better mobile experience
  dragmode=False,
  # German number separators
  separators=",."
)

# write plot to file
fig.write_html("index.html",
  include_plotlyjs=True,
  config={"displayModeBar": False},
  full_html=True,
  auto_open=True,
)
