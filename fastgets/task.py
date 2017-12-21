# coding: utf8
import time
import uuid
import requests
from mongoengine import *

from . import logger


class Task(Document):

    METHOD_GET = 'GET'
    METHOD_POST = 'POST'

    id = StringField(primary_key=True)
    headers = DictField()
    url = URLField()
    method = StringField(default='GET')
    get_payload = DictField()
    post_payload = DictField()
    temp_data = DictField()
    timeout = IntField(default=5)
    encoding = StringField()

    def new(self):
        task = Task.from_json(self.to_json())
        del task.id
        return task

    def _prepare_kwds(self):
        kwds = {
            'timeout': self.timeout,
            'headers': self.headers
        }
        return kwds

    def _get_crawl(self):
        kwds = self._prepare_kwds()
        if self.get_payload:
            kwds['params'] = self.get_payload

        r = requests.get(self.url, **kwds)
        if self.encoding:
            r.encoding = self.encoding
        return r.text

    def _post_crawl(self):
        kwds = self._prepare_kwds()
        if self.post_payload:
            kwds['data'] = self.post_payload

        r = requests.post(self.url, **kwds)
        if self.encoding:
            r.encoding = self.encoding
        return r.text

    def crawl(self):
        if self.method == self.METHOD_GET:
            return self._get_crawl()
        elif self.method == self.METHOD_POST:
            return self._post_crawl()

    def process(self, page_raw):
        self.func(self, page_raw)

    def exec(self):
        assert not self.id
        self.id = str(uuid.uuid4())

        start_time = time.time()
        logger.info('[crawl][{}]'.format(self.url))
        page_raw = self.crawl()
        logger.info('[crawl][{}][seconds: {}]'.format(self.url, time.time()-start_time))

        start_time = time.time()
        logger.info('[process][{}]'.format(self.url))
        self.process(page_raw)
        logger.info('[process][{}][seconds: {}]'.format(self.url, time.time()-start_time))

    @property
    def func(self):
        return self._func

    @func.setter
    def func(self, func):
        self._func = func
