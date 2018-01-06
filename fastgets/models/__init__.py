from mongoengine import connect
from .instance import Instance
from .unknown_error_log import UnknownErrorLog


connect('test', host='localhost', port=27017)
