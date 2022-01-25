"""Structural patterns"""
from time import time


class AppRoute:
    """
    Декоратор для маршрутизации контроллеров
    """
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


class Debug:
    """
    Декоратор для вычисления времени выполнения методов класса
    """
    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def timeit(method):
            def timed(*args, **kwargs):
                time_start = time()
                result = method(*args, **kwargs)
                time_end = time()
                time_delta = time_end - time_start

                print(f'debug: {self.name} выполнялся {time_delta:2.2f} ms')
                return result
            return timed
        return timeit(cls)
