
CRAWL_REDIS_HOST = 'localhost'
CRAWL_REDIS_PORT = 6379
CRAWL_REDIS_PWD = ''

REDIS_CONFIG = dict(
    host=CRAWL_REDIS_HOST,
    port=CRAWL_REDIS_PORT,
    password=CRAWL_REDIS_PWD,
)


ERROR_TASK_POOL_REDIS_CONFIG = dict(
    host=CRAWL_REDIS_HOST,
    port=CRAWL_REDIS_PORT,
    password=CRAWL_REDIS_PWD,
    db=1
)


STATS_REDIS_CONFIG = dict(
    host=CRAWL_REDIS_HOST,
    port=CRAWL_REDIS_PORT,
    password=CRAWL_REDIS_PWD,
    db=2
)


API_HOST = 'localhost'
API_PORT = 8081


ROOT_DIR = __file__.split('FastGets')[0] + 'FastGets/'

TEMPLATES_DIR = ROOT_DIR + 'templates/'
TEMPLATES_DIR = __file__.split('FastGets')[0] + 'MyProject/myproject/templates/'

PYTHON = '/srv/virtualenvs/FastGets/bin/python3'
PYTHON = 'python3'

CRON_USER = 'xuyong'
