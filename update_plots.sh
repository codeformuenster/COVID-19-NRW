#!/bin/bash

set -e

git pull origin master
python convert_ODMS_file_to_timeseries.py
python plot_data.py
git add data/ images/ *.html
git commit -m "update with newest data $(date +'%d. %B %H:%m')"
git push origin master
