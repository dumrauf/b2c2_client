import httpretty

from list_instruments import list_instruments
from settings import B2C2_INSTRUMENTS_URL
from tests.basic_http_request import BasicHTTPRequest
from tests.testing_utils import capture


class TestListInstruments(BasicHTTPRequest):
    def setUp(self):
        httpretty.enable()
        self.expected_list_of_instruments = self._update_instruments_url()

    def tearDown(self):
        httpretty.reset()

    def test_list_instruments(self):
        with capture(list_instruments) as output:
            expected_response = "Available instruments: [u'BTCUSD', u'BTCEUR', u'BTCGBP', u'ETHBTC', u'ETHUSD', u'EURUSD']\n"
            self.assertEqual(expected_response,
                             output)

    def test_error_codes(self):
        self._test_error_codes(method=httpretty.GET,
                               relative_url=B2C2_INSTRUMENTS_URL,
                               function_to_test=list_instruments)

    def test_authorisation_token(self):
        self._test_authorisation_token(method=httpretty.GET,
                                       relative_url=B2C2_INSTRUMENTS_URL,
                                       function_to_test=list_instruments,
                                       args=[],
                                       kwargs={})
