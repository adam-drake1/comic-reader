import functools
import time


def debug(func):
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        start_time = time.time()
        value = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start_time} to run")
        return value
    return wrapper_debug
