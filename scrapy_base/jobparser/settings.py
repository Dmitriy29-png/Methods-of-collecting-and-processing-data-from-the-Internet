

SPIDER_MODULES = ['jobparser.spiders']
NEWSPIDER_MODULE = 'jobparser.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'

LOG_ENABLE = True
LOG_FILE = 'log.txt'
LOG_LEVEL = 'DEBUG'

IMAGES_STORE = 'images'
ROBOTSTXT_OBEY = False
ITEM_PIPELINES = {
    'jobparser.pipeline.LeroyparserPipeline': 400,
    'jobparser.pipeline.CSVPipeline':300,
    'jobparser.pipeline.LeroyImagesPipeline': 200,
}
ONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 3
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 8