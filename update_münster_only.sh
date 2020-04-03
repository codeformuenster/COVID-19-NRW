if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    echo "Usage: ./update_münster_only.sh infected_int recovered_int deaths_int"
    exit 1
fi

git stash
git pull
python add_only_MS_counts_to_timeseries.py $1 $2 $3
python plot_data.py
git add data/time_series/
git add images/covid-19-münster.svg
git add münster.html
git commit -m "update only MS with newest data `date +'%d. %B'`"
git push
