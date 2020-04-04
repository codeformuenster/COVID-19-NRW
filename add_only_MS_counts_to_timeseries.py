#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas
import sys

if len(sys.argv) != 4:
  print("Usage: python add_only_MS_counts_to_timeseries.py infected_int recovered_int deaths_int")
  exit(1)

confirmed_df = pandas.read_csv("data/time_series/time_series_covid-19_nrw_confirmed.csv")
recovered_df = pandas.read_csv("data/time_series/time_series_covid-19_nrw_recovered.csv")
deaths_df = pandas.read_csv("data/time_series/time_series_covid-19_nrw_deaths.csv")

confirmed_df = confirmed_df.set_index(['Kommune'], drop=True)
recovered_df = recovered_df.set_index(['Kommune'], drop=True)
deaths_df = deaths_df.set_index(['Kommune'], drop=True)

confirmed_df.loc["Stadt Münster", pandas.to_datetime('today').strftime('%Y-%m-%d')] = sys.argv[1]
recovered_df.loc["Stadt Münster", pandas.to_datetime('today').strftime('%Y-%m-%d')] = sys.argv[2]
deaths_df.loc["Stadt Münster", pandas.to_datetime('today').strftime('%Y-%m-%d')] = sys.argv[3]

confirmed_df.to_csv("data/time_series/time_series_covid-19_nrw_confirmed.csv")
recovered_df.to_csv("data/time_series/time_series_covid-19_nrw_recovered.csv")
deaths_df.to_csv("data/time_series/time_series_covid-19_nrw_deaths.csv")
