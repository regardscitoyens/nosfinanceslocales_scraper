#!/bin/bash
# Crawl all pages from year 2000 to 2012
zone_type=$1
startyear=2000
if [ $zone_type = "region" ]; then
    startyear=2008
fi

if [ $zone_type = "department" ]; then
    startyear=2008
fi

if [ $zone_type = "epci" ]; then
    startyear=2007
fi

for year in $(seq $startyear 2012);
do
    echo $year
    scrapy crawl localfinance -o scraped_data/${zone_type}_$year.csv -t csv -a year=$year -a zone_type=$zone_type
done

