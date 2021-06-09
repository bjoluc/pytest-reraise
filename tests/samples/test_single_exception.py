"""
All tests should fail.
"""
from threading import Thread


def test_reraise(reraise):
    def run():
        with reraise:
            assert False

    Thread(target=run).start()


def test_reraise_wrap(reraise):
    def run():
        assert False

    Thread(target=reraise.wrap(run)).start()


def test_reraise_wrap_decorator(reraise):
    @reraise.wrap
    def run():
        assert False

    Thread(target=run).start()


def test_exception(reraise):
    assert False
