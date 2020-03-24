import pandas
import glob
import urllib.request

url = 'http://example.com/'
open_data_ms = pandas.read_csv(urllib.request.urlopen("https://raw.githubusercontent.com/od-ms/resources/master/coronavirus-fallzahlen-regierungsbezirk-muenster.csv"))

open_data_ms['Datum'] = pandas.to_datetime(open_data_ms['Datum'], format='%d.%m.%Y')

open_data_ms = open_data_ms.sort_values(by='Datum')

confirmed_df = pandas.DataFrame({'Kommune': open_data_ms['Gebiet'].unique()})
recovered_df = pandas.DataFrame({'Kommune': open_data_ms['Gebiet'].unique()})
deaths_df = pandas.DataFrame({'Kommune':  open_data_ms['Gebiet'].unique()})

confirmed_df = confirmed_df.set_index(['Kommune'], drop=True)
recovered_df = recovered_df.set_index(['Kommune'], drop=True)
deaths_df = deaths_df.set_index(['Kommune'], drop=True)

for day in open_data_ms['Datum'].dt.date.unique():

  for kommune in open_data_ms['Gebiet'].unique():
    all_data_kommune = open_data_ms[open_data_ms['Gebiet'] == kommune]

    c = all_data_kommune[all_data_kommune['Datum'] == pandas.Timestamp(day)]['Bestätigte Faelle'].values
    r = all_data_kommune[all_data_kommune['Datum'] == pandas.Timestamp(day)]['Gesundete'].values
    d = all_data_kommune[all_data_kommune['Datum'] == pandas.Timestamp(day)]['Todesfaelle'].values
    
    if len(c) == 1:
      confirmed_df.loc[kommune, day] = c

    if len(r) == 1:
      recovered_df.loc[kommune, day] = r
      
    if len(d) == 1:
      deaths_df.loc[kommune, day] = d

confirmed_df.to_csv("data/time_series/time_series_covid-19_nrw_confirmed.csv")
recovered_df.to_csv("data/time_series/time_series_covid-19_nrw_recovered.csv")
deaths_df.to_csv("data/time_series/time_series_covid-19_nrw_deaths.csv")

