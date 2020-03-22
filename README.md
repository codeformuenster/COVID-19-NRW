# COVID-19-NRW

Doku noch sehr rudimentär, sorry!
Daten bisher nur für Münster, tendentiell sollte es aber auch für andere Kommunen klappen.

Um eine neue Kommune hinzuzufügen, eine entsprechende Zeile unter `data/daily_reports` schreiben.
Dann `python plot_data.py` ausführen.

Für einen deutschen Plot muss dann noch folgendes in die erstellte HTML-Datei eingefügt werden (s. https://github.com/plotly/plotly.py/issues/2302):

```
# this needs to be copy-pasted to the created html file
# after the plotly script
<script src="https://cdn.plot.ly/plotly-locale-de-latest.js"></script>
```

Die HTML-Datei sollte damit alleine lauffähig sein.

Außerdem folgenden Code ganz nach unten für unser Logo & Co und damit wir sehen, wieviele Leute sich die Visualisierung angucken:

```
Ein Projekt von <a href="https://codeformuenster.org"><img src="cfm_logo.png"></a><br>
<a href="https://codeformuenster.org/impressum/">Impressum und Datenschutzerklärung</a>
<!-- Fathom - simple website analytics - https://github.com/usefathom/fathom -->
<script>
(function(f, a, t, h, o, m){
  a[h]=a[h]||function(){
    (a[h].q=a[h].q||[]).push(arguments)
  };
  o=f.createElement('script'),
  m=f.getElementsByTagName('script')[0];
  o.async=1; o.src=t; o.id='fathom-script';
m.parentNode.insertBefore(o,m)
})(document, window, '//fathom.codeformuenster.org/tracker.js', 'fathom');
fathom('set', 'siteId', 'JJUAP');
fathom('trackPageview');
</script>
<!-- / Fathom -->
```
