import logging
from logging.config import dictConfig
from uuid import uuid4

from settings import LOGGING_CONFIG
from utils.connection import Connection


dictConfig(LOGGING_CONFIG)
logger = logging.getLogger()


UUID_ATTRIBUTE_NAME = '__uuid'


class BasicAction(object):
    @property
    def uuid(self):
        if getattr(self, UUID_ATTRIBUTE_NAME, None) is None:
            uuid = str(uuid4())
            setattr(self, UUID_ATTRIBUTE_NAME, uuid)
            self.logger.info('Set UUID to {uuid}'.format(uuid=uuid))
        return getattr(self, UUID_ATTRIBUTE_NAME)

    def __init__(self, b2c2_base_url, api_token):
        self.b2c2_base_url = b2c2_base_url
        self.api_token = api_token
        self._connection = Connection(b2c2_base_url=b2c2_base_url,
                                      api_token=api_token)
        self.logger = logger

    def run(self):
        raise NotImplementedError("Actions must implement the '_run' method")
