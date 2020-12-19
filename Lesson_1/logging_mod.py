from reusepatterns.singletones import SingletonByName
import time
from datetime import datetime


class Logger(metaclass=SingletonByName):
    def __init__(self, name):
        self.name = name

    def log(self, text):
        print('log===>', text)


def debug(func):
    def inner(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'{datetime.now()} DEBUG===> {func.__name__} time spent={end - start} sec')
        return result

    return inner
