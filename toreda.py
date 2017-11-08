import argparse
import sys

from actions.request_for_quote_action import RequestForQuoteAction
from settings import B2C2_BASE_URL, BUY_COMMAND, SELL_COMMAND, API_TOKEN


def _parse_args(args):
    parser = argparse.ArgumentParser(description='Toreda - A RFQ Trader Client for the b2c2 Sandbox API')
    parser.add_argument('--instrument',
                        required=True,
                        type=str,
                        help='The instrument to use (e.g. BTCUSD, BTCJPY)')
    parser.add_argument('--side',
                        required=True,
                        type=str,
                        choices=[BUY_COMMAND,
                                 SELL_COMMAND],
                        help='The side to execute; options are {choices}'.format(choices=[BUY_COMMAND,
                                                                                          SELL_COMMAND]))
    parser.add_argument('--quantity',
                        required=True,
                        type=int,
                        help='The quantity to trade')
    args = parser.parse_args()
    return args


def _request_for_quote(instrument, side, quantity):
    request_for_quote_action = RequestForQuoteAction(b2c2_base_url=B2C2_BASE_URL,
                                                     api_token=API_TOKEN,
                                                     instrument=instrument,
                                                     side=side,
                                                     quantity=quantity)
    result = request_for_quote_action.run()
    return result


def main():
    parser = _parse_args(sys.argv[1:])
    result = _request_for_quote(instrument=parser.instrument,
                                side=parser.side,
                                quantity=parser.quantity)
    return result


if __name__ == "__main__":
    main()
