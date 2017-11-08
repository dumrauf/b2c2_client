import json
from unittest import TestCase
from urlparse import urljoin

import httpretty

from settings import B2C2_BASE_URL, B2C2_BALANCE_URL, B2C2_TRADE_URL, B2C2_REQUEST_FOR_QUOTE_URL, \
    API_TOKEN, B2C2_INSTRUMENTS_URL
from settings import KNOWN_ERROR_CODES
from utils.errors import HTTPErrorCodeReceivedError


class BasicHTTPRequest(TestCase):
    ####################################################################################################################
    # URL Endpoint Helper Methods
    ####################################################################################################################
    def _update_request_for_quote_url(self, quantity, side, instrument):
        body = {
            "valid_until": u"2017-01-01T19:45:22.025464Z",
            "rfq_id": u"d4e41399-e7a1-4576-9b46-349420040e1a",
            "client_rfq_id": u"149dc3e7-4e30-4e1a-bb9c-9c30bd8f5ec7",
            "quantity": unicode(quantity),
            "side": side,
            "instrument": instrument,
            "price": u"700.00000000",
        }
        httpretty.register_uri(method=httpretty.POST,
                               uri=urljoin(B2C2_BASE_URL,
                                           B2C2_REQUEST_FOR_QUOTE_URL),
                               body=json.dumps(body),
                               content_type='text/json')
        return body

    def _update_trade_url(self, instrument, side, quantity, price, rfq_id):
        body = {
            "created": "2016-09-27T11:27:46.599039Z",
            "price": unicode(price),
            "instrument": instrument,
            "trade_id": "5c7e90cc-a8d6-4db5-8348-44053b2dcbdf",
            "rfq_id": rfq_id,
            "side": side,
            "quantity": unicode(quantity)
        }
        httpretty.register_uri(method=httpretty.POST,
                               uri=urljoin(B2C2_BASE_URL,
                                           B2C2_TRADE_URL),
                               body=json.dumps(body),
                               content_type='text/json')
        return body

    def _update_balance_url(self):
        body = {
            "USD": "0",
            "BTC": "0",
            "JPY": "0",
            "GBP": "0",
            "ETH": "0",
            "EUR": "0",
            "CAD": "0"
        }
        httpretty.register_uri(method=httpretty.GET,
                               uri=urljoin(B2C2_BASE_URL,
                                           B2C2_BALANCE_URL),
                               body=json.dumps(body),
                               content_type='text/json')
        return body

    def _update_instruments_url(self):
        body = [
            {
                "name": "BTCUSD"
            },
            {
                "name": "BTCEUR"
            },
            {
                "name": "BTCGBP"
            },
            {
                "name": "ETHBTC"
            },
            {
                "name": "ETHUSD"
            },
            {
                "name": "EURUSD"
            }
        ]
        httpretty.register_uri(method=httpretty.GET,
                               uri=urljoin(B2C2_BASE_URL,
                                           B2C2_INSTRUMENTS_URL),
                               body=json.dumps(body),
                               content_type='text/json')
        return body

    ####################################################################################################################
    # Validation Helper Methods
    ####################################################################################################################
    def _test_error_codes(self, method, relative_url, function_to_test, known_error_codes=KNOWN_ERROR_CODES, args=None, kwargs=None):
        for known_error_code in known_error_codes:
            httpretty.enable()
            httpretty.register_uri(method=method,
                                   uri=urljoin(B2C2_BASE_URL,
                                               relative_url),
                                   body=json.dumps('irrelevant'),
                                   status=known_error_code)
            args = [] if args is None else args
            kwargs = {} if kwargs is None else kwargs
            self.assertRaises(HTTPErrorCodeReceivedError, function_to_test, *args, **kwargs)
            httpretty.reset()

    def _test_authorisation_token(self, method, relative_url, function_to_test, args, kwargs):
        expeced_autorisation_headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token {api_token}'.format(api_token=API_TOKEN),
        }
        httpretty.enable()
        httpretty.register_uri(method=method,
                               uri=urljoin(B2C2_BASE_URL,
                                           relative_url),
                               body=json.dumps('irrelevant'))
        response = function_to_test(*args, **kwargs)
        headers = httpretty.last_request().headers
        self.assertDictContainsSubset(expeced_autorisation_headers,
                                      headers)
