"""
All tests should fail.
"""
from threading import Thread


def test_reraise(reraise):
    def run():
        with reraise:
            assert False

    Thread(target=run).start()


def test_exception(reraise):
    assert False
