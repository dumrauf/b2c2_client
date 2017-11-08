from unittest import TestCase

import settings


SETTING_ATTRIBUTES_TO_VALUE_MAPPING = {
    # B2C2 URLS
    'B2C2_BASE_URL': 'https://sandboxapi.b2c2.net',
    'B2C2_REQUEST_FOR_QUOTE_URL': '/request_for_quote/',
    'B2C2_TRADE_URL': '/trade/',
    'B2C2_BALANCE_URL': '/balance/',
    'B2C2_INSTRUMENTS_URL': '/instruments/',
    'ERROR_CODES_TO_MEANING_MAPPING': {
        400: "Bad Request - Incorrect parameters.",
        401: "Unauthorized - Wrong Token.",
        404: "Not Found - The specified endpoint could not be found.",
        405: "Method Not Allowed - You tried to access an endpoint with an invalid method.",
        406: "Not Acceptable - Incorrect request format.",
        500: "Internal Server Error - We had a problem with our server. Try again later."
    },

    # API protocol keys
    'BUY_COMMAND': 'buy',
    'SELL_COMMAND': 'sell',

    'INSTRUMENT_KEY': 'instrument',
    'SIDE_KEY': 'side',
    'QUANTITY_KEY': 'quantity',
    'CLIENT_RFQ_ID_KEY': 'client_rfq_id',
    'PRICE_KEY': 'price',
    'RFQ_ID_KEY': 'rfq_id',
}


class TestSettings(TestCase):
    def test_attributes(self):
        for attribute, expected_value in SETTING_ATTRIBUTES_TO_VALUE_MAPPING.items():
            attribute_value = getattr(settings, attribute)
            self.assertEqual(attribute_value,
                             expected_value)

    def test_known_error_codes(self):
        known_error_codes = settings.ERROR_CODES_TO_MEANING_MAPPING.keys()
        self.assertEqual(settings.KNOWN_ERROR_CODES,
                         known_error_codes)
