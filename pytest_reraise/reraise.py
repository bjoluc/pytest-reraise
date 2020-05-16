import pytest
from pytest import Item
from typing import Union


class Reraise:
    def __init__(self):
        self._catch = False
        self._exception = None
        self._origin = self

    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.exception = exc_value
        return self._catch  # Raise the exception if catch is false

    @property
    def exception(self):
        """
        The exception that has been captured by this `Reraise` instance, if any.
        """
        return self._origin._exception

    @exception.setter
    def exception(self, e: Exception):
        """
        Set the exception that this `Reraise` instance raises, if no exception has been
        captured or set yet.
        """
        if self._origin._exception is None:
            self._origin._exception = e

    def reset(self):
        """
        Resets the exception that was previously captured, if any, and returns it.
        """
        if self.exception is not None:
            e = self.exception
            self._origin._exception = None
            return e

    def __call__(self, catch: bool = None) -> Union["Reraise", None]:
        """
        If called without arguments, raises the first exception that has been captured
        by this `Reraise` context manager since the last call to `reraise()`. Note that
        this is automatically done at the end of each test case that uses `reraise`, and
        during the teardown phase of these test cases. You can manually do it if you
        wish to interrupt your main thread instead.

        If called with the `catch` argument, returns a context manager that catches
        exceptions, or forwards them, depending on the value of the catch argument.
        """
        if catch is None:
            e = self.reset()
            if e is not None:
                raise e
        else:
            child = Reraise()
            child._catch = catch
            child._origin = self._origin
            return child


@pytest.fixture
def reraise():
    reraise = Reraise()
    yield reraise
    # If `reraise` has captured an exception during the teardown phase, it was not
    # handled by the pytest_runtest_call wrapper.
    reraise()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_call(item: Item):
    yield
    # If an exception was captured, override any exception in the main thread by
    # re-raising the captured exception
    if "reraise" in item.funcargs:
        item.funcargs["reraise"]()
