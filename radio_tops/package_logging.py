import logging.handlers
from .config import settings


logger = logging.getLogger('radio_tops')
formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s]%(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

if settings.log_level_debug == 'True':
    logger.setLevel(logging.DEBUG)
    stream_handler.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
    stream_handler.setLevel(logging.INFO)

logger.addHandler(stream_handler)
