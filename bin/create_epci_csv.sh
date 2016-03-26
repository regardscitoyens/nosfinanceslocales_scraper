#!/bin/sh

year=2012

mkdir -p .cache
cd .cache

for year in $(seq $year 2014);
do
    wget -N http://www.insee.fr/fr/methodes/zonages/epci-au-01-01-${year}.zip
    rm -f epci-au-01-01-${year}.xls
    unzip epci-au-01-01-${year}.zip
done

cd ..

python bin/create_epci_csv.py