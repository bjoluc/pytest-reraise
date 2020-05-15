"""
All tests should pass.
"""
from threading import Thread


def test_catching(reraise):
    flag = False

    def run():
        nonlocal flag
        with reraise(catch=True):
            assert False
        flag = True

    t = Thread(target=run)
    t.start()
    t.join()

    assert flag is True
    assert type(reraise.reset()) is AssertionError


def test_no_catching(reraise):
    flag = False

    def run():
        nonlocal flag
        with reraise(catch=False):
            assert False
        flag = True

    t = Thread(target=run)
    t.start()
    t.join()

    assert flag is False
    assert type(reraise.reset()) is AssertionError


def test_catching_child_exception_access(reraise):
    child = reraise(catch=True)

    def run():
        with child:
            assert False

    t = Thread(target=run)
    t.start()
    t.join()

    assert type(child.exception) is AssertionError
    assert type(reraise.exception) is AssertionError
    assert child.exception is child.reset()
    assert reraise.exception is None
