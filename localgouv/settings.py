# Scrapy settings for localgouv project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'localgouv'

SPIDER_MODULES = ['localgouv.spiders']
NEWSPIDER_MODULE = 'localgouv.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'localgouv (+http://www.yourdomain.com)'

#DOWNLOAD_DELAY = 0.25

AUTOTHROTTLE_ENABLED = True
