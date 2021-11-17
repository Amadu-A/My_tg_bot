from loguru import logger


logger.add('debug.json', format='{time} {level} {message}',
           level='DEBUG', rotation='1 week', compression='zip', serialize=True)