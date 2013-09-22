#!/bin/bash
# Crawl all pages from year 2000 to 2012
zone_type=$1
for year in $(seq 2000 2012);
do
    scrapy crawl localgouv -o scraped_data/${zone_type}_$year.csv -t csv -a year=$year -a zone_type=$zone_type
done

