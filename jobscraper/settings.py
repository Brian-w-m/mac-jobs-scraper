# Scrapy settings for your project
BOT_NAME = 'jobscraper'

COOKIES_ENABLED = True

SPIDER_MODULES = ['jobscraper.spiders']
NEWSPIDER_MODULE = 'jobscraper.spiders'

# User-Agent to mimic a browser
USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
)

# Obey robots.txt rules (set to False if you need to ignore them)
ROBOTSTXT_OBEY = False

# Splash server address
SPLASH_URL = 'http://localhost:8050'

# Enable Splash-specific middlewares
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
}

# Enable Splash spider middlewares
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# Enable Splash-aware duplicate filtering
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

# Enable Splash-aware HTTP cache storage
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# Enable HTTP caching (recommended with Splash to avoid unnecessary render requests)
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600  # Cache expires after 1 hour
HTTPCACHE_DIR = '.scrapy/httpcache'

# Configure the item pipelines (if needed)
ITEM_PIPELINES = {
    # Add your pipelines here (if applicable)
}

# Configure download delay to avoid getting banned
DOWNLOAD_DELAY = 2  # 2 seconds delay between requests
CONCURRENT_REQUESTS = 8
CONCURRENT_REQUESTS_PER_DOMAIN = 4

# Retry settings
RETRY_ENABLED = True
RETRY_TIMES = 3  # Retry a request 3 times if it fails

# Logging settings
LOG_LEVEL = 'INFO'  # Change to DEBUG for more detailed logs

# Other optional settings
COOKIES_ENABLED = False  # Disable cookies unless necessary
