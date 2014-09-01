#coding=utf-8
__author__ = 'DM_'

import threading
import Queue


class work(threading.Thread):
    def __init__(self, workQueue, timeout=3, **kwargs):
        self.timeout = timeout
        self.isRunning = False
        self.workQueue = workQueue
        threading.Thread.__init__(self, kwargs=kwargs)
#        self.daemon = True

    def stop(self):
        self.isRunning = False

    def run(self):
        self.isRunning = True
        while self.isRunning:
            try:
                func, args, kwargs = self.workQueue.get(timeout=self.timeout)
                apply(func, *args, **kwargs)
                self.workQueue.task_done()
            except Queue.Empty:
                self.isRunning = False
            except:
                pass

class ThreadPool:
    def __init__(self, num_of_threads=10):
        self.workQueue = Queue.Queue()
        self.threads = []

        for i in range(num_of_threads):
            thread = work(self.workQueue)
            self.threads.append(thread)

    def add_job(self, fun, *args, **kwargs):
        self.workQueue.put((fun, args, kwargs))

    def start(self):
        try:
            for t in self.threads:
                t.start()
        except:
            self.stop()

    def stop(self):
        for t in self.threads:
            t.stop()

    def wait_for_complete(self):
        try:
            for t in self.threads:
                while t.isAlive():
                    t.join(10)

        except KeyboardInterrupt:
            self.stop()
            print

