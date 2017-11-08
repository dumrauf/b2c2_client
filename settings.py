# API Token
API_TOKEN = ''
assert API_TOKEN, "'API_TOKEN' must be set."

# B2C2 URLS
B2C2_BASE_URL = 'https://sandboxapi.b2c2.net'
B2C2_INSTRUMENTS_URL = '/instruments/'
B2C2_REQUEST_FOR_QUOTE_URL = '/request_for_quote/'
B2C2_TRADE_URL = '/trade/'
B2C2_BALANCE_URL = '/balance/'

ERROR_CODES_TO_MEANING_MAPPING = {
    400: "Bad Request - Incorrect parameters.",
    401: "Unauthorized - Wrong Token.",
    404: "Not Found - The specified endpoint could not be found.",
    405: "Method Not Allowed - You tried to access an endpoint with an invalid method.",
    406: "Not Acceptable - Incorrect request format.",
    500: "Internal Server Error - We had a problem with our server. Try again later."
}

KNOWN_ERROR_CODES = ERROR_CODES_TO_MEANING_MAPPING.keys()

# API protocol keys
BUY_COMMAND = 'buy'
SELL_COMMAND = 'sell'

INSTRUMENT_KEY = 'instrument'
SIDE_KEY = 'side'
QUANTITY_KEY = 'quantity'
CLIENT_RFQ_ID_KEY = 'client_rfq_id'
PRICE_KEY = 'price'
RFQ_ID_KEY = 'rfq_id'


# Standard Python Logging Configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
    },

    "loggers": {
        "my_module": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": "no"
        }
    },

    "root": {
        "level": "INFO",
        "handlers": ["console"]
    }
}
