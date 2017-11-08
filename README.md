# b2c2 CLI Trading Client

This repository contains a fully tested and easily extendable [b2c2](https://www.b2c2.com/) command-line interface trading client.
The trading client is coded against the [b2c2 sandbox API](https://sandboxapi.b2c2.net) and


1. Requests a quote for given a instrument, side, and quantity
2. Asks the user for permission to execute the trade on the returned RFQ ("Request for Quote") data
3. If permission is denied, the program is terminated immeditately
4. If permission is granted, the trade is executed
5. Upon successful trade, the total balance is displayed

Note: Should any of the above steps fail due to an _error status code received from the server_ then the program fails and displays the corresponding error code.


## Prerequisits


In order for the b2c2 CLI trading client to work, it is necessary to

1. Obtain a token for the b2c2 sandbox API and
2. Whitelist the IP of the client machine


## Setup Instructions

First, please provide an `API_TOKEN` in module `settings.py`; nothing will work without it. There is also an assertion in case this step is skipped.

After creating a Python 2.7 virtualenv, install all requirements via
```
pip install -r requirements.txt
```


## Running the Tests

Once the setup has been completed, run the tests (which use a mock HTTP server) from the base directory of this project via
```
python -m unittest discover tests/
```

Note that the test will contain output saying

> "TypeError: string indices must be integers"

and

>"toreda.py: error: argument --instrument: expected one argument"

This is purely logging information and _does not impact the success of the tests_.

## Listing Instruments

All available instruments, can be queried using `list_instruments.py` via
```
python list_instruments.py
```
The output is exactly what is returned from the server.


## Requesting Quotes and Executing Trades

The main program `toreda.py` (which apprently means 'Trader' in Japanese) can be run via
```
python toreda.py --instrument <instrument of choice> --side {buy, sell} --quantity <integer>
```
Note that the parameters

 - `--instrument` (one of the available instruments)
 - `--side` (either `buy` or `sell`)
 - `--quantity` (an integer)

are required. Should any parameter be missing or be in an incorrect format, then the programme will print an error message and exit.


## FAQs

This section lists frequently asked questions and tries to provide an answer.


### Why is there no time checking before executing a trade after the RFQ phase?

This is done on purpose as the main question is: _Which time should actually be used for that?!_

There is a decent chance that the host machine's clock is out of sync with the server's clock. Moreover, the single time that counts is the one on the server! By executing the request, regardless of the current time, we let the server return an error code and handle the error code accordingly.

Here, we follow the basic principle that it's easier to ask forgiveness than permission and eliminate false positives that way. One important side effect is that we might squeeze some trades through that would have otherwise not been executed due to clock synchronisation issues.


### Why is there no instruments checking before executing a trade?

There are two distinct endpoints:
 - one for receiving the list of available instruments
 - one for executing a trade, providing a specific instrument

While the two endpoints seem closely related I could not find a guarantee that the set of instruments match. Moreover, what's really important is that the trade is executed. Again, we let the server decided incorrect instruments and react accordingly.


### Why is the output just plain JSON as received from the server?

As the task was to a develop a CLI trading client, an MVP solution might very well simply parrot the JSON received from the server.
It's readable by a human, even though it's probably not the most user friendly presentation.
For me, it's about functionality and ensuring that the core functionality works reliably before beautifying things.


### What's the testing strategy?

The main idea is to test _end-to-end on the functionality guaranteed_ -- and not the implementation. This is the reasons why the `connection.py` module is not explicitly tested. Its functionalities are heavily used (for things like error detection in responses) but can easily be swapped out with something that achieves the same goals via different means.

Moreover, as many tests as possible verify that the agreed protocol standards (i.e. request payload) are as expected on the edge of the system. This means that tests are in place that the input parameters eventually arrive at a mock server in the correct format - how they are created is irrelevant (and therefore untested).

The following four components are tested:

 - listing instruments
 - requesting a quote and potentially executing it
 - settings (as any change in the settings could potentially bring the whole application down)
 - asking a user for permission to proceed (as this is mocked in the end-to-end tests)

### Why is there no computation of the balance before receiving it from the b2c2 engine?

There are mainly two reasons:

1. I chose to prioritise the main functionality and make it as solid as possible, given the time I had.
3. The task to "compute the balance before actually receiving it from the b2c2 engine" is actually more complicated than it sounds as first. Sure, a little bookkeeping is easy to do when everything goes well but what if things go wrong? What if a trade falls trough? There is no reliable a priori way of telling until the server has responded. Moreover, any functionality would have to be thoroughly tested before being shipped.


## Potential Improvements

Some of the tests can be improved by moving more tests to the boundary of the system. Currently, the functionality is guaranteed by checking the output but that's not really a great idea. Ideally, there would be dynamic URL endpoints set up with the help of `httpretty` that verify that successive requests perform as expected.

In general, I would prefer to get rid of the output testing as it is rather error prone. If you have a better way, please let me know.

The `connection.py` module has a currently unused `expected_status_codes` parameter. Future extensions would provide a list of expected HTTP status codes and fail faster should anything outside the expected happen.

## Miscellaneous

The following Python 2.7 packages were used for developing and testing:

- `requests`
- `httpretty`
- `mock`

The documentation was written in Markdown and compiled via [`grip`](https://github.com/joeyespo/grip).

Made on a Mac using PyCharm and two cups of coffee.
