Localgouv
=========

This project aims at scrapping financial data of all towns (="communes") from
the website http://www.collectivites-locales.gouv.fr/.

We used scrapy lib to crawl the page and xpaths stuff to scrap data.

Usage
=====

For example, to scrap data of every towns on the fiscal year 2012, run the root
dir:
`scrapy crawl localgouv -o scrapped_data_dir/localgouv_2012.json -t json -a year=2012`

Requirements
===========
[See requirements.txt file.](requirements.txt)


