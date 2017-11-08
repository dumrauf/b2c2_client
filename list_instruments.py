from actions.list_instruments import ListInstrumentsAction
from settings import API_TOKEN, B2C2_BASE_URL


def list_instruments():
    list_intstruments_action = ListInstrumentsAction(b2c2_base_url=B2C2_BASE_URL,
                                                     api_token=API_TOKEN)
    result = list_intstruments_action.run()
    return result


if __name__ == "__main__":
    list_instruments()
