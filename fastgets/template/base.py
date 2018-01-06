# coding: utf8

import sys

from .. import env
from ..core.errors import FrameError


class TemplateBase(object):

    # thread_num
    # second_rate_limit
    # max_pending_task_num
    config = {}

    @classmethod
    def load(cls):
        raise NotImplementedError

    @classmethod
    def check_config(cls):
        for key, val in cls.config.items():
            if key not in ['thread_num', 'second_rate_limit', 'max_pending_task_num']:
                raise ValueError('unknown config item: {}'.format(key))

            if key == 'thread_num':
                if not isinstance(val, int) or not (10 >= val > 0):
                    raise ValueError('config thread_num must be int & 10 > thread_num > 0')
            if key == 'second_rate_limit':
                if not isinstance(val, int) or not val > 0:
                    raise ValueError('config second_rate_limit must be int & second_rate_limit > 0')
            if key == 'max_pending_task_num':
                if not isinstance(val, int) or not 100000 > val > 0:
                    raise ValueError('config max_pending_task_num must be int & 100,000 > max_pending_task_num > 0')

    @classmethod
    def run(cls):
        from ..engine import DistributedEngine, LocalEngine

        cls.check_config()

        if len(sys.argv) >= 2:
            mode = sys.argv[1]
        else:
            mode = 'l'

        if mode == 't':
            env.mode = env.TEST
            engine = LocalEngine(cls, is_testing=True)
        elif mode == 'l':
            env.mode = env.LOCAL
            engine = LocalEngine(cls)
        elif mode == 'p':
            env.mode = env.DISTRIBUTED
            env.is_loading_tasks = True
            engine = DistributedEngine(cls)
        else:
            raise FrameError('unknown mode')

        engine.run()
