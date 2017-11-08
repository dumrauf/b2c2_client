import random
import string

import sys
from StringIO import StringIO
from contextlib import contextmanager


def get_random_string(length=10):
    return ''.join([random.choice(string.ascii_letters) for _ in xrange(length)])


@contextmanager
def capture(command, *args, **kwargs):
    out, sys.stdout = sys.stdout, StringIO()
    try:
        command(*args, **kwargs)
        sys.stdout.seek(0)
        yield sys.stdout.read()
    finally:
        sys.stdout = out
