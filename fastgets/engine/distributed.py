# coding: utf8

import datetime
import os
import threading
import time

from ..models.instance import Instance
from .. import env
from ..pool import RunningPoolMonitor
from ..utils import create_id, format_exception
from .base import Engine


class DistributedEngine(Engine):

    def __init__(self, template_class):
        self.template_class = template_class
        self.instance = self.make_instance()

        self.running_pool_monitor = RunningPoolMonitor(self.instance.id)

        self.running_pool_monitor_thread = None
        self.instance_update_thread = None
        self.seed_task_load_thread = None

        env.instance_id = self.instance.id

    def make_instance(self):
        instance = Instance()
        instance.id = create_id()
        instance.process_id = str(os.getpid())
        instance.name = self.template_class.__name__
        instance.description = (self.template_class.__doc__ or '').strip()
        instance.start_at = datetime.datetime.now()
        instance.save()

        return instance

    def sync_instance_from_mongo(self):
        self.instance = Instance.objects.with_id(self.instance.id)
        assert self.instance

    def update_instance_from_redis(self):
        pass

    def start_running_pool_monitor_thread(self):
        def _():
            while self.instance.is_running():
                self.running_pool_monitor.loop()
                time.sleep(self.running_pool_monitor.CHECK_INTERVAL_SECONDS)

        self.running_pool_monitor_thread = threading.Thread(target=_)
        self.running_pool_monitor_thread.start()

    def start_instance_update_thread(self):
        def _():
            while self.instance.is_running():
                self.update_instance_from_redis()
                self.sync_instance_from_mongo()
                time.sleep(1)

        self.instance_update_thread = threading.Thread(target=_)
        self.instance_update_thread.start()

    def start_seed_task_load_thread(self):
        def _():
            try:
                self.template_class.load()
            except Exception:
                Instance.objects(id=self.instance.id).update(
                    set__traceback_string=format_exception(),
                    set__stop_at=datetime.datetime.now(),
                )

        self.seed_task_load_thread = threading.Thread(target=_, daemon=True)  # 由于无法主动中断 load 函数的执行 所以需要加 daemon
        self.seed_task_load_thread.start()

    def is_running(self):
        return self.running_pool_monitor_thread.is_alive() or \
               self.instance_update_thread.is_alive() or \
               (self.instance.is_running() and self.seed_task_load_thread.is_alive())

    def run(self):
        self.start_running_pool_monitor_thread()
        self.start_instance_update_thread()
        self.start_seed_task_load_thread()

        while self.is_running():
            time.sleep(1)
