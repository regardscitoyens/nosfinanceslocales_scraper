#!/bin/sh

year=2008

mkdir -p .cache
cd .cache

for year in $(seq $year 2015);
do
    wget -N "http://www.collectivites-locales.gouv.fr/files/files/epcicom${year}.csv"
done

cd ..

