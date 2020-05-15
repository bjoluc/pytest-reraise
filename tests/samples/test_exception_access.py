from threading import Thread

import pytest


class ExceptionA(Exception):
    pass


class ExceptionB(Exception):
    pass


# Should pass
def test_exception_access(reraise):
    def run():
        reraise.exception = ExceptionA()

    t = Thread(target=run)
    t.start()
    t.join()

    assert type(reraise.exception) is ExceptionA
    with pytest.raises(ExceptionA):
        reraise()

    assert reraise.exception is None
    assert reraise.reset() is None

    reraise.exception = ExceptionB()
    assert type(reraise.reset()) is ExceptionB
    assert reraise.exception is None
