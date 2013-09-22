Localgouv
=========

This project aims at scraping financial data of cities (="communes"), EPCI
(group of cities Cf. [wikipedia](http://fr.wikipedia.org/wiki/%C3%89tablissement_public_de_coop%C3%A9ration_intercommunale)), department and regions from the website
http://www.collectivites-locales.gouv.fr/.

We used scrapy lib to crawl the page and xpaths stuff to scrap data.

To check the quality of the crawling and to analyze data, we use ipython
notebooks:
 * analysis of data from cities in 2012 [here](http://nbviewer.ipython.org/urls/raw.github.com/fmassot/localgouv_scraper/master/notebooks/localgouvdata_analysis.ipynb)
 * analysis of data from epci in 2012 [here](http://nbviewer.ipython.org/urls/raw.github.com/fmassot/localgouv_scraper/master/notebooks/epcidata_analysis.ipynb)


Usage
=====

To scrap data of a give zone type (city, epci, department or region) on a given fiscal
year YYYY, run in the root dir:

`scrapy crawl localgouv -o scraped_data_dir/zonetype_YYYY.json -t csv -a year=YYYY`

To scrap data for all available fiscal years for a given zone type:

`. bin/crawl_all_years zonetype`

To generate a csv file with all data for a given zonetype and with french
header, run:

`. bin/bundle zonetype`

This command will generate a file in nosdonnees/zonetype_all.csv which you can
upload on [nosdonnees.fr](nosdonnees.fr) website.



Requirements
===========
[See requirements.txt file.](requirements.txt)


Tests
=====

`unit2 discover`

TODO
====
 * Add some docs, especially indicate the mapping between variable names and
   fields in html pages.
 * Get simple stats on scraped data to check its quality (partly made for
   cities and epci).
 * Add some tests on different fiscal years.


