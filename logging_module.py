from loguru import logger
import functools
from typing import Callable


logger.add('debug.log', format='{time} {level} {message}',
           level='DEBUG', rotation='1 week', compression='zip') #serialize=True


def logging_decorator(func: Callable) -> Callable:
    """
    Декоратор, логгирующий работу кода
    """

    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        result = func(*args, **kwargs)
        logger.debug(f'{func.__name__} - успешно!')
        return result
    return wrapped_func

def logging_decorator_responce(func: Callable) -> Callable:
    """
    Декоратор, логгирующий работу кода
    """

    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        result = func(*args, **kwargs)
        if result:
            logger.debug(f'{func.__name__} - успешно!')
        else:
            logger.error(f'{func.__name__}  - ошибка! {result}')
        return result
    return wrapped_func