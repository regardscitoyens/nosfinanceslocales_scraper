# Scrapy settings for localgouv project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'localfinance'

SPIDER_MODULES = ['localfinance.spiders']
NEWSPIDER_MODULE = 'localfinance.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'localgouv (+http://www.yourdomain.com)'

#DOWNLOAD_DELAY = 0.25

AUTOTHROTTLE_ENABLED = True

# Logging does weird things...
#import scrapy
#scrapy.log.start(logfile="logs/logs", loglevel=scrapy.log.DEBUG, logstdout=True)
HTTPCACHE_ENABLED = True
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': 543,
}

HTTPCACHE_STORAGE = 'scrapy.contrib.httpcache.FilesystemCacheStorage'
