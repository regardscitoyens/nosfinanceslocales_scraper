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
USER_AGENT = 'RegardsCitoyens (+https://regardscitoyens.org)'

DOWNLOAD_DELAY = 0.1

AUTOTHROTTLE_ENABLED = True

LOG_LEVEL = "INFO"

HTTPCACHE_ENABLED = True
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 543,
}

HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
