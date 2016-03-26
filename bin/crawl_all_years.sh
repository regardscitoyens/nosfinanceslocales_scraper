#!/bin/bash

echo "Crawl..."
echo "------------"

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

for year in $(seq $startyear 2014);
do
    scrapy crawl localfinance -o scraped_data/${zone_type}_$year.json -t jsonlines -a year=$year -a zone_type=$zone_type
done

echo "...done"
echo

