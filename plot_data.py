import plotly.graph_objects as go  # plots
import pandas
import locale


confirmed = pandas.read_csv("data/time_series/time_series_covid-19_nrw_confirmed.csv")
recovered = pandas.read_csv("data/time_series/time_series_covid-19_nrw_recovered.csv")
deaths = pandas.read_csv("data/time_series/time_series_covid-19_nrw_deaths.csv")

# create plot
fig = go.Figure()

locale.setlocale(locale.LC_ALL, 'de_DE')

for kommune_idx in range(len(confirmed)):  

  kommune = confirmed.iloc[kommune_idx, 0]
  
  confirmed_ts = confirmed.iloc[kommune_idx, 2:].T  
  recovered_ts = recovered.iloc[kommune_idx, 2:].T
  deaths_ts = deaths.iloc[kommune_idx, 2:].T

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
        line=dict(color="orange"),
        hovertemplate="Infektionen " + kommune + ": %{y}"
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
        line=dict(color="green"),
        hovertemplate="genesen " + kommune + ": %{y}"
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
          line=dict(color="black"),
          hovertemplate="Todesfälle " + kommune + ": %{y}"
            + "<extra></extra>" # no additional legend text in tooltip
      )  
  )

fig.update_layout(
  title="Coronafälle in Münster (Stand: 21. März, 17 Uhr)<br>Quellen: <a href='https://www.muenster.de/corona'>muenster.de/corona</a> und <a href='https://www.bezreg-muenster.de/de/im_fokus/uebergreifende_themen/coronavirus/coronavirus_allgemein/index.html'>Bezirksregierung Münster</a>",
  xaxis_title="Datum",
  yaxis_title="Fälle",
  legend_orientation="h",
  # disable dragmode for better mobile experience
  dragmode=False,
  # German number separators
  separators=",."
)

# write plot to file
fig.write_html("index.html",
  include_plotlyjs="cdn",
  config={"displayModeBar": False,
          "locale": "de"},
  auto_open=True
)

# this needs to be copy-pasted to the created html file

# after the plotly script
# <script src="https://cdn.plot.ly/plotly-locale-de-latest.js"></script>

# at the bottom
#Ein Projekt von <a href="https://codeformuenster.org"><img src="cfm_logo.png"></a><br>
#<a href="https://codeformuenster.org/impressum/">Impressum und Datenschutzerklärung</a>
#<!-- Fathom - simple website analytics - https://github.com/usefathom/fathom -->
#<script>
#(function(f, a, t, h, o, m){
#	a[h]=a[h]||function(){
#		(a[h].q=a[h].q||[]).push(arguments)
#	};
#	o=f.createElement('script'),
#	m=f.getElementsByTagName('script')[0];
#	o.async=1; o.src=t; o.id='fathom-script';
#	m.parentNode.insertBefore(o,m)
#})(document, window, '//fathom.codeformuenster.org/tracker.js', 'fathom');
#fathom('set', 'siteId', 'JJUAP');
#fathom('trackPageview');
#</script>
#<!-- / Fathom -->

