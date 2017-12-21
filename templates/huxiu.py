# coding: utf8
import re
import json
import lxml.html
from fastgets.task import Task
from fastgets.template import Template


class HuxiuTemplate(Template):

    @classmethod
    def load(cls):

        task = Task()
        task.url = 'https://www.huxiu.com/'
        task.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'  # NOQA
        }
        task.timeout = 20
        task.func = cls.parse_channel_url_list_page
        task.exec()

    @classmethod
    def parse_channel_url_list_page(cls, task, page_raw):
        doc = lxml.html.fromstring(page_raw)
        channel_urls = [
            'https://www.huxiu.com/' + url
            for url in doc.xpath('//ul[contains(@class, "menu-box")]/li/a/@href')
        ]

        for channel_url in channel_urls:
            new_task = task.new()
            new_task.url = channel_url
            new_task.func = cls.parse_channel_detail_page
            new_task.exec()

    @classmethod
    def parse_channel_detail_page(cls, task, page_raw):
        doc = lxml.html.fromstring(page_raw)

        channel_name = doc.xpath('//div[@class="column-wrap"]/span/text()')[0]
        channel_id = re.findall('/(\d+)\.html', task.url)[0]
        huxiu_hash_code = re.findall('huxiu_hash_code=\'([0-9a-z]+)\'', page_raw)[0]

        new_task = task.new()
        new_task.url = 'https://www.huxiu.com/channel/ajaxGetMore'
        new_task.headers['Referer'] = task.url
        new_task.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        new_task.headers['Origin'] = 'https://www.huxiu.com'
        new_task.method = Task.METHOD_POST
        new_task.post_payload = {
            'huxiu_hash_code': huxiu_hash_code,
            'catId': channel_id,
            'page': 1,
        }
        new_task.func = cls.parse_article_list_json
        new_task.temp_data['channel_name'] = channel_name
        new_task.exec()

    @classmethod
    def parse_article_list_json(cls, task, page_raw):
        json_dict = json.loads(page_raw)
        html = json_dict['data']['data']
        doc = lxml.html.fromstring(html)

        for url in doc.xpath('//h2/a/@href'):
            new_task = task.new()
            new_task.url = 'https://www.huxiu.com' + url
            new_task.method = Task.METHOD_GET
            new_task.func = cls.parse_article_detail_page
            new_task.exec()

    @classmethod
    def parse_article_detail_page(cls, task, page_raw):
        doc = lxml.html.fromstring(page_raw)
        id = doc.xpath('//div[@class="article-section"]/@data-aid')[0]
        title = doc.xpath('//h1[@class="t-h1"]/text()')[0].strip()
        channel_name = task.temp_data['channel_name']

        # 这里先直接打印出来，不做其它复杂处理
        print(channel_name, id, title, task.url)


if __name__ == '__main__':
    HuxiuTemplate.run()
