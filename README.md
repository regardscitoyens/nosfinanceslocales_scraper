Localgouv
=========

This project aims at scrapping financial data of cities (="communes"), EPCI
(group of cities Cf. [wikipedia](http://fr.wikipedia.org/wiki/%C3%89tablissement_public_de_coop%C3%A9ration_intercommunale)), department and regions from the website
http://www.collectivites-locales.gouv.fr/.

We used scrapy lib to crawl the page and xpaths stuff to scrap data.

To check the quality of the crawling and to analyze data, we use ipython
notebooks:
 * analysis of data from cities in 2012 [here](http://nbviewer.ipython.org/urls/raw.github.com/fmassot/localgouv_scraper/master/notebooks/localgouvdata_analysis.ipynb)
 * analysis of data from epci in 2012 [here](http://nbviewer.ipython.org/urls/raw.github.com/fmassot/localgouv_scraper/master/notebooks/epcidata_analysis.ipynb)


Usage
=====

To scrap data of every cities on the fiscal year 2012, run in the root
dir:
`scrapy crawl localgouv -o scraped_data_dir/localgouv_2012.json -t json -a year=2012`

To crawl EPCI, add an optionnal paramter `-a zone_type='epci'`.

Scraped data samples are available in scraped_data directory:
 * [epci_2012.sample.json](scraped_data/epci_2012.sample.json)


Requirements
===========
[See requirements.txt file.](requirements.txt)


TODO
====
 * Crawl department and region pages.
 * Add some docs, especially indicate the mapping between variable names and
   fields in html pages.
 * Get simple stats on scraped data to check its quality (partly made for
   cities).
 * Add some tests on different fiscal years.


