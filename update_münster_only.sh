if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    echo "Usage: ./update_münster_only.sh PATH infected_int recovered_int deaths_int"
    exit 1
fi

cd "$1"

git stash
git pull
python add_only_MS_counts_to_timeseries.py $2 $3 $4
python plot_data.py
git add data/time_series/
git add images/covid-19-münster.svg
git add münster.html
git commit -m "update only MS with newest data `date +'%d. %B'`"
git push
