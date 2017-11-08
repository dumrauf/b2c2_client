import json
import sys

import httpretty
from mock import patch

from actions.request_for_quote_action import RequestForQuoteAction
from settings import B2C2_BASE_URL, B2C2_BALANCE_URL, B2C2_TRADE_URL, B2C2_REQUEST_FOR_QUOTE_URL, \
    API_TOKEN, INSTRUMENT_KEY, SIDE_KEY, QUANTITY_KEY, PRICE_KEY, RFQ_ID_KEY
from tests.basic_http_request import BasicHTTPRequest
from tests.testing_utils import get_random_string, capture
from toreda import main


class TestRequestForQuote(BasicHTTPRequest):
    def setUp(self):
        self.rfq_test_action = RequestForQuoteAction(b2c2_base_url=B2C2_BASE_URL,
                                                     api_token=API_TOKEN,
                                                     instrument='BTCUSD',
                                                     side='buy',
                                                     quantity="1.0000000000")

    def tearDown(self):
        httpretty.reset()  # disable afterwards, so that you will have no problems in code that uses that socket module

    ####################################################################################################################
    # Arguments Tests
    ####################################################################################################################
    def test_cli_input_parameters_instrument_missing(self):
        sys.argv = ['toreda.py', '--side', 'buy', '--quantity', '222']
        self.assertRaises(SystemExit, main)

    def test_cli_input_parameters_instrument_empty(self):
        sys.argv = ['toreda.py', '--instrument', '--side', 'buy', '--quantity', '222']
        self.assertRaises(SystemExit, main)

    def test_cli_input_parameters_side_missing(self):
        sys.argv = ['toreda.py', '--instrument', 'BTCUSD', '--quantity', '222']
        self.assertRaises(SystemExit, main)

    def test_cli_input_parameters_side_empty(self):
        sys.argv = ['toreda.py', '--instrument', 'BTCUSD', '--side', '--quantity', '222']
        self.assertRaises(SystemExit, main)

    def test_cli_input_parameters_side_unknown(self):
        sys.argv = ['toreda.py', '--instrument', 'BTCUSD', '--side', 'unknown', '--quantity', '222']
        self.assertRaises(SystemExit, main)

    def test_cli_input_parameters_quantity_missing(self):
        sys.argv = ['toreda.py', '--instrument', 'BTCUSD', '--side', 'buy']
        self.assertRaises(SystemExit, main)

    def test_cli_input_parameters_quantity_empty(self):
        sys.argv = ['toreda.py', '--instrument', 'BTCUSD', '--side', 'buy', '--quantity']
        self.assertRaises(SystemExit, main)

    def test_cli_input_parameters_quantity_nan(self):
        sys.argv = ['toreda.py', '--instrument', 'BTCUSD', '--side', 'buy', '--quantity', 'not_a_number']
        self.assertRaises(SystemExit, main)

    ####################################################################################################################
    # Internal Functional Tests
    ####################################################################################################################
    def test_uuid_fixed(self):
        uuid = self.rfq_test_action.uuid
        for _ in xrange(1000):
            self.assertEqual(uuid,
                             self.rfq_test_action.uuid)

    def test_trade_repeats_rfq_parameters(self):
        self._update_trade_url(instrument=get_random_string(length=10),
                               side=get_random_string(length=10),
                               quantity=get_random_string(length=10),
                               price=get_random_string(length=10),
                               rfq_id=get_random_string(length=10))
        for _ in xrange(10):
            # GIVEN
            random_rfq_response = {
                INSTRUMENT_KEY: get_random_string(),
                SIDE_KEY: get_random_string(),
                QUANTITY_KEY: get_random_string(),
                PRICE_KEY: get_random_string(),
                RFQ_ID_KEY: get_random_string(),
            }
            # WHEN
            self.rfq_test_action._trade(rfq_json_response=random_rfq_response)
            # THEN
            body = httpretty.last_request().body
            expected_json_response = json.dumps(random_rfq_response)
            self.assertEqual(expected_json_response,
                             body)

    ####################################################################################################################
    # Error Code Handling Tests
    ####################################################################################################################
    def test_request_for_quote_error_codes(self):
        self._update_request_for_quote_url(quantity=100,
                                           side='buy',
                                           instrument='BTCGBP')
        self._test_error_codes(method=httpretty.POST,
                               relative_url=B2C2_REQUEST_FOR_QUOTE_URL,
                               function_to_test=self.rfq_test_action._request_for_quote)

    def test_trade_error_codes(self):
        body = self._update_request_for_quote_url(quantity=100,
                                                  side='buy',
                                                  instrument='BTCGBP')
        self._update_trade_url(instrument=get_random_string(length=10),
                               side=get_random_string(length=10),
                               quantity=get_random_string(length=10),
                               price=get_random_string(length=10),
                               rfq_id=get_random_string(length=10))
        self._test_error_codes(method=httpretty.POST,
                               relative_url=B2C2_TRADE_URL,
                               function_to_test=self.rfq_test_action._trade,
                               kwargs={'rfq_json_response': body})

    def test_get_balance_error_codes(self):
        self._update_balance_url()
        self._test_error_codes(method=httpretty.GET,
                               relative_url=B2C2_BALANCE_URL,
                               function_to_test=self.rfq_test_action._get_balance)

    ####################################################################################################################
    # End to End Tests
    ####################################################################################################################
    @patch('actions.request_for_quote_action.is_allowed_to_proceed', return_value=False)
    def test_rfq_without_autorisation_to_continue(self, input):
        # GIVEN
        instrument = u'BTCGBP'
        side = u'sell'
        quantity = 222
        sys.argv = ['toreda.py', '--instrument', instrument, '--side', side, '--quantity', str(quantity)]
        self._update_request_for_quote_url(quantity=quantity,
                                           side=side,
                                           instrument=instrument)
        # WHEN
        with capture(main) as output:
            pass
        # THEN
        # 1. The correct request is made
        body = httpretty.last_request().body
        json_body = json.loads(body)
        expected_minimum_request = {
            INSTRUMENT_KEY: instrument,
            SIDE_KEY: side,
            QUANTITY_KEY: str(quantity),
        }
        self.assertDictContainsSubset(expected_minimum_request,
                                      json_body)
        # 2. The correct output is printed
        expected_output = """Received quote: {u'valid_until': u'2017-01-01T19:45:22.025464Z', u'price': u'700.00000000', u'instrument': u'BTCGBP', u'rfq_id': u'd4e41399-e7a1-4576-9b46-349420040e1a', u'side': u'sell', u'client_rfq_id': u'149dc3e7-4e30-4e1a-bb9c-9c30bd8f5ec7', u'quantity': u'222'}"""
        self.assertIn(expected_output,
                      output)

    @patch('actions.request_for_quote_action.is_allowed_to_proceed', return_value=True)
    def test_rfq_with_autorisation_to_continue(self, input):
        # GIVEN
        instrument = u'BTCGBP'
        side = u'sell'
        quantity = 222
        sys.argv = ['toreda.py', '--instrument', instrument, '--side', side, '--quantity', str(quantity)]
        self._update_request_for_quote_url(quantity=quantity,
                                           side=side,
                                           instrument=instrument)
        price = "700.00000000"
        rfq_id = u"d4e41399-e7a1-4576-9b46-349420040e1a"
        self._update_trade_url(instrument=instrument,
                               side=side,
                               quantity=quantity,
                               price=price,
                               rfq_id=rfq_id)
        self._update_balance_url()
        # WHEN
        with capture(main) as output:
            # THEN
            expected_output = ("""Received quote: {u'valid_until': u'2017-01-01T19:45:22.025464Z', u'price': u'700.00000000', u'instrument': u'BTCGBP', u'rfq_id': u'd4e41399-e7a1-4576-9b46-349420040e1a', u'side': u'sell', u'client_rfq_id': u'149dc3e7-4e30-4e1a-bb9c-9c30bd8f5ec7', u'quantity': u'222'}
Trade: {u'created': u'2016-09-27T11:27:46.599039Z', u'price': u'700.00000000', u'instrument': u'BTCGBP', u'trade_id': u'5c7e90cc-a8d6-4db5-8348-44053b2dcbdf', u'rfq_id': u'd4e41399-e7a1-4576-9b46-349420040e1a', u'side': u'sell', u'quantity': u'222'}
Balance: {u'USD': u'0', u'BTC': u'0', u'JPY': u'0', u'GBP': u'0', u'ETH': u'0', u'EUR': u'0', u'CAD': u'0'}
""")
            self.assertEqual(expected_output,
                             output)