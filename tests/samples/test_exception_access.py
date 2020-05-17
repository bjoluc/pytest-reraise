import pytest


class ExceptionA(Exception):
    pass


class ExceptionB(Exception):
    pass


# Should pass
def test_exception_access(reraise):
    reraise.exception = ExceptionA()
    assert type(reraise.exception) is ExceptionA
    with pytest.raises(ExceptionA):
        reraise()

    assert reraise.exception is None
    assert reraise.reset() is None

    reraise.exception = ExceptionB()
    assert type(reraise.reset()) is ExceptionB
    assert reraise.exception is None


# Should fail
def test_manual_reraise_precedence(reraise):
    reraise.exception = Exception("A")

    try:
        reraise()  # This exception should be reported,
    finally:
        reraise.exception = Exception("B")  # not this one
