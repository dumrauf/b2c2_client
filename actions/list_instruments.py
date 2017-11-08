from actions.basic_action import BasicAction
from settings import B2C2_INSTRUMENTS_URL, KNOWN_ERROR_CODES


class ListInstrumentsAction(BasicAction):
    def _get_instruments(self):
        self.logger.info('Getting instruments...')
        response = self._connection.get_from_url(relative_url=B2C2_INSTRUMENTS_URL,
                                                 data={},
                                                 known_error_codes=KNOWN_ERROR_CODES)
        json_response = response.json()
        self.logger.info('... received instruments: {json_response}'.format(json_response=json_response))
        return json_response

    def _print_available_instruments(self, instruments_json_response):
        instruments = []
        for instruments_dict in instruments_json_response:
            try:
                instruments.append(instruments_dict['name'])
            except (KeyError, TypeError) as e:
                self.logger.exception('Malformed response dictionary '
                                      '{instruments_dict}!'.format(instruments_dict=instruments_dict))
        print 'Available instruments: {instruments}'.format(instruments=instruments)

    def run(self):
        instruments_json_response = self._get_instruments()
        self._print_available_instruments(instruments_json_response=instruments_json_response)
