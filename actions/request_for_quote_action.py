from actions.basic_action import BasicAction
from settings import INSTRUMENT_KEY, SIDE_KEY, QUANTITY_KEY, CLIENT_RFQ_ID_KEY, B2C2_REQUEST_FOR_QUOTE_URL, PRICE_KEY, \
    RFQ_ID_KEY, B2C2_TRADE_URL, B2C2_BALANCE_URL, KNOWN_ERROR_CODES
from utils.prompt import is_allowed_to_proceed


class RequestForQuoteAction(BasicAction):
    def _request_for_quote(self):
        post_data = {
            INSTRUMENT_KEY: self.instrument,
            SIDE_KEY: self.side,
            QUANTITY_KEY: str(self.quantity),
            CLIENT_RFQ_ID_KEY: self.uuid
        }
        self.logger.info('Requesting quote with data {post_data}...'.format(post_data=post_data))
        response = self._connection.post_to_url(relative_url=B2C2_REQUEST_FOR_QUOTE_URL,
                                                data=post_data,
                                                known_error_codes=KNOWN_ERROR_CODES)
        json_response = response.json()
        self.logger.info('... received quote with data: {json_response}'.format(json_response=json_response))
        return json_response

    def _trade(self, rfq_json_response):
        post_data = {
            INSTRUMENT_KEY: rfq_json_response[INSTRUMENT_KEY],
            SIDE_KEY: rfq_json_response[SIDE_KEY],
            QUANTITY_KEY: rfq_json_response[QUANTITY_KEY],
            PRICE_KEY: rfq_json_response[PRICE_KEY],
            RFQ_ID_KEY: rfq_json_response[RFQ_ID_KEY],
        }
        self.logger.info('Requesting trade with data {post_data}...'.format(post_data=post_data))
        response = self._connection.post_to_url(relative_url=B2C2_TRADE_URL,
                                                data=post_data,
                                                known_error_codes=KNOWN_ERROR_CODES)
        json_response = response.json()
        self.logger.info('... received trade with data: {json_response}'.format(json_response=json_response))
        return json_response

    def _get_balance(self):
        self.logger.info('Getting balance...')
        response = self._connection.get_from_url(relative_url=B2C2_BALANCE_URL,
                                                 data={},
                                                 known_error_codes=KNOWN_ERROR_CODES)
        json_response = response.json()
        self.logger.info('... received balance: {json_response}'.format(json_response=json_response))
        return json_response

    def __init__(self, b2c2_base_url, api_token, instrument, side, quantity):
        super(RequestForQuoteAction, self).__init__(b2c2_base_url=b2c2_base_url,
                                                    api_token=api_token)
        self.instrument = instrument
        self.side = side
        self.quantity = quantity

    def run(self):
        rfq_json_response = self._request_for_quote()
        print 'Received quote: {rfq_json_response}'.format(rfq_json_response=rfq_json_response)
        if not is_allowed_to_proceed():
            self.logger.info('Permission to trade NOT granted. Terminating.')
            return
        else:
            self.logger.info('Permission to trade granted.')
            trade_json_response = self._trade(rfq_json_response=rfq_json_response)
            print 'Trade: {trade_json_response}'.format(trade_json_response=trade_json_response)
            balance_json_response = self._get_balance()
            print 'Balance: {balance_json_response}'.format(balance_json_response=balance_json_response)
