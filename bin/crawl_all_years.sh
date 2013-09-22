#!/bin/bash
# Crawl all pages from year 2000 to 2012
zone_type=$1
startyear=2000
if [ $zone_type -eq "region"]; then
    startyear=2008
fi

if [ $zone_type -eq "department"]; then
    startyear=2008
fi

for year in $(seq 2008 2012);
do
    scrapy crawl localgouv -o scraped_data/${zone_type}_$year.csv -t csv -a year=$year -a zone_type=$zone_type
done

