import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    "%(asctime)s:%(name)s:%(funcName)s:[%(levelname)s]:%(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# usage
# logger.debug('A debug message')
# logger.info('An info message')
# logger.warning('There is something wrong')
# logger.error('An error has happened.')
# logger.critical('Fatal error occured. Cannot continue')
