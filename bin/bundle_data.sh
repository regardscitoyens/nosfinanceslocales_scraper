#!/bin/bash
# Concatenate all csv file for a zone type and generate a file
# in nosdonnees/zone_type.csv with french headers
dir='scraped_data/'
zone_type=$1
name=$dir$1
head -n 1 ${name}_2008.csv > $name.head
find $dir -name "${zone_type}_*[0-9].csv" | xargs -n 1 tail -n +2 > $name.data
cat $name.head ${name}.data > ${name}_all.csv
rm $name.head ${name}.data

python bin/to_french_headers.py ${name}_all.csv $zone_type
