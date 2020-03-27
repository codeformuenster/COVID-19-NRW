git pull
python convert_ODMS_file_to_timeseries.py
python plot_data.py
git add data/
git add images/
git add *.html
git commit -m "update with newest data `date +'%d. %B'`"
git push
