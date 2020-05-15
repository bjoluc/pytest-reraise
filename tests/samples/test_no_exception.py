"""
All tests should pass.
"""
from threading import Thread


def test_reraise_no_exception(reraise):
    def run():
        with reraise:
            pass

    Thread(target=run).start()


def test_no_exception(reraise):
    pass
