# COVID-19-NRW

Doku noch sehr rudimentär, sorry!
Daten für den Regierungsbezirk Münster, s. Datenlizenz unten.

Das Skript `update_plots.sh` generiert alle HTML-Seiten mit allen verfügbaren Plots basierend auf den aktuellen Daten aus dem Open-Data-Portal der Stadt Münster (s. unten).
Dabei werden die Skripte `plot_barchart.py` und `plot_linechart.py` vom Skript `plot_data.py` aufgerufen.
Für jede Kommune/Landkreise sollte nach Ausführen von `update_plots.sh` nun eine lauffähige HTMl-Datei erstellt worden sein (und, bei entsprechenden `git`-Rechten sollten diese Datein auch bereits hochgeladen sein).

## Gegenüberstellung der Fallzahlen von Erkrankten und bereits Genesenen

In dem Repo befinden sich zwei Python-Skripte, mit denen ein Balkendiagramm und ein Liniendiagramm zur Analyse der täglichen Fallzahlen generiert werden kann:
- plot_barchart.py
- plot_linechart.py

### Visulisierung am Beispiel der Fallzahlen von Münster
![Balkendiagramm](https://github.com/codeformuenster/COVID-19-NRW/blob/master/images/covid-19-m%C3%BCnster.svg)
![Liniendiagramm](https://github.com/codeformuenster/COVID-19-NRW/blob/master/images/covid-19-m%C3%BCnster_line.svg)

## Rechtliches

### Datenlizenz

Die Daten [stammen aus dem Open-Data-Portal der Stadt Münster (Datenquelle: Bezirksregierung Münster)](https://opendata.stadt-muenster.de/dataset/coronavirus-infektionen-sars-cov-2-im-regierungsbezirk-m%C3%BCnster). Sie sind unter der [„Datenlizenz Deutschland – Namensnennung – Version 2.0"](https://www.govdata.de/dl-de/by-2-0) lizenziert.

### Softwarelizenz

Der Quelltext dieses Projekts ist lizenziert unter der Apache 2.0 Lizenz:

```
Copyright 2020 Code for Münster

Licensed under the Apache License, Version 2.0 (the "License");
you may not use these files except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
