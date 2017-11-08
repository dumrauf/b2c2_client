from logging.config import dictConfig, logging
from urlparse import urljoin

import requests

from settings import LOGGING_CONFIG, ERROR_CODES_TO_MEANING_MAPPING
from utils.errors import UnexpectedHTTPStatusCodeReturnedError, HTTPErrorCodeReceivedError

dictConfig(LOGGING_CONFIG)
logger = logging.getLogger()


class Connection(object):

    def __init__(self, b2c2_base_url, api_token):
        self.b2c2_base_url = b2c2_base_url
        self.api_token = api_token

    def _get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Token {api_token}'.format(api_token=self.api_token),
        }

    def _check_response_for_known_error_codes(self, response, known_error_codes):
        status_code = response.status_code
        if known_error_codes is not None and status_code in known_error_codes:
            message = ERROR_CODES_TO_MEANING_MAPPING[status_code]
            logger.info('Detected error status code {status_code}: {message}'.format(status_code=status_code,
                                                                                     message=message))
            raise HTTPErrorCodeReceivedError(message)

    def _check_response_for_expected_status_codes(self, response, expected_status_codes):
        status_code = response.status_code
        if expected_status_codes is not None and status_code not in expected_status_codes:
            logger.info('Detected unexpected status code {status_code}'.format(status_code=status_code))
            raise UnexpectedHTTPStatusCodeReturnedError('Received status code {status_code} is not contained in the list of '
                                                        'expected status codes {expected_status_codes}'.format(expected_status_codes=expected_status_codes,
                                                                                                               status_code=status_code))

    def _validate_response(self, response, expected_status_codes, known_error_codes):
        self._check_response_for_known_error_codes(response=response,
                                                   known_error_codes=known_error_codes)
        self._check_response_for_expected_status_codes(response=response,
                                                       expected_status_codes=expected_status_codes)

    def get_from_url(self, relative_url, data, expected_status_codes=None, known_error_codes=None):
        url = urljoin(self.b2c2_base_url,
                      relative_url)
        logger.info("GETting {data} from '{url}'...".format(data=data,
                                                            url=url))
        response = requests.get(url=url,
                                headers=self._get_headers(),
                                params=data,
                                verify=False)
        self._validate_response(response=response,
                                expected_status_codes=expected_status_codes,
                                known_error_codes=known_error_codes)
        logger.info("...done GETting {data} from '{url}'!".format(data=data,
                                                                  url=url))
        return response

    def post_to_url(self, relative_url, data, expected_status_codes=None, known_error_codes=None):
        url = urljoin(self.b2c2_base_url,
                      relative_url)
        logger.info("POSTing {data} to '{url}'...".format(data=data,
                                                          url=url))
        response = requests.post(url=url,
                                 headers=self._get_headers(),
                                 json=data,
                                 verify=False)
        self._validate_response(response=response,
                                expected_status_codes=expected_status_codes,
                                known_error_codes=known_error_codes)
        logger.info("...done POSTing {data} to '{url}'!".format(data=data,
                                                                url=url))
        return response
