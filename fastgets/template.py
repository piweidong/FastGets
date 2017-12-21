# coding: utf8


class Template(object):

    @classmethod
    def load(cls):
        raise NotImplementedError

    @classmethod
    def run(cls):
        cls.load()
