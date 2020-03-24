import pandas
import glob

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

