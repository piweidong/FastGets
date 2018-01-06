from mongoengine import connect
from .instance import Instance
from .unknown_error_log import UnknownErrorLog
from .. import env

if env.mode == env.DISTRIBUTED:
    if env.configured:
        connect(env.MONGO_CONFIG['db'], host=env.MONGO_CONFIG['host'], port=env.MONGO_CONFIG['port'])
    else:
        raise ValueError('must call fastgets.init_fastgets_env to init env')
