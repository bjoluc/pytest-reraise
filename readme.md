# pytest-reraise

[![PyPI version fury.io](https://badge.fury.io/py/pytest-reraise.svg)](https://pypi.python.org/pypi/pytest-reraise/)
[![Build Status](https://travis-ci.com/bjoluc/pytest-reraise.svg?branch=master)](https://travis-ci.com/bjoluc/pytest-reraise)
[![codecov](https://codecov.io/gh/bjoluc/pytest-reraise/branch/master/graph/badge.svg)](https://codecov.io/gh/bjoluc/pytest-reraise)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pytest-reraise.svg)](https://pypi.python.org/pypi/pytest-reraise/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Let's assume you write a pytest test case that includes assertions in another thread, like so:

```python
from threading import Thread

def test_assert():

    def run():
        assert False

    Thread(target=run).start()
```

This test will pass, as the `AssertionError` is not raised in the main thread.
`pytest-reraise` is here to help you capture the exception and raise it in the main thread:

```sh
pip install pytest-reraise
```

```python
from threading import Thread

def test_assert(reraise):

    def run():
        with reraise:
            assert False

    Thread(target=run).start()
```

The above test will fail, as `pytest-reraise` captures the exception and raises it at the end of the test case.

## Advanced Usage and Special Cases

### Manual Re-raising

By default, the captured exception (if any) is raised at the end of the test case.
If you want to raise it before then, call `reraise()` in your test case.
If an exception has been raised within a `with reraise` block by then, `reraise()` will raise it right away:

```python
def test_assert(reraise):

    def run():
        with reraise:
            assert False

    reraise() # This will not raise anything yet

    t = Thread(target=run)
    t.start()
    t.join()

    reraise() # This will raise the assertion error
```

As seen in the example above, `reraise()` can be called multiple times during a test case. Whenever an exception has been raised in a `with reraise` block since the last call, it will by raised on the next call.

### Multiple Exceptions

When the `reraise` context manager is used multiple times in a single test case, only the first-raised exception will be re-raised in the end.
In the below example, both threads raise an exception but only one of these exceptions will be re-raised.

```python
def test_assert(reraise):

    def run():
        with reraise:
            assert False

    for _ in range(2):
        Thread(target=run).start()
```

### Catching Exceptions

By default, the `reraise` context manager does not catch exceptions, so they will not be hidden from the thread in which they are raised.
If you want to change this, use `reraise(catch=True)` instead of `reraise`:

```python
def test_assert(reraise):

    def run():
        with reraise(catch=True):
            assert False
        print("I'm alive!")

    Thread(target=run).start()
```

Note that you cannot use `reraise()` (without the `catch` argument) as a context manager, as it is used to raise exceptions.

### Exception Priority

If `reraise` captures an exception and the main thread raises an exception as well, the exception captured by `reraise` will mask the main thread's exception unless that exception was already re-raised.
The objective behind this is that the outcome of the main thread often depends on the work performed in other threads.
Thus, failures in in other threads are likely to cause failures in the main thread, and other threads' exceptions (if any) are of greater importance for the developer than main thread exceptions.

The example below will report `assert False`, not `assert "foo" == "bar"`.

```python
def test_assert(reraise):

    def run():
        with reraise:
            assert False # This will be reported

    t = Thread(target=run)
    t.start()
    t.join()

    assert "foo" == "bar" # This won't
```

### Accessing and Modifying Exceptions

`reraise` provides an `exception` property to retrieve the exception that was captured, if any.
`reraise.exception` can also be used to assign an exception if no exception has been captured yet.
In addition to that, `reraise.reset()` returns the value of `reraise.exception` and resets it to `None` so that the exception will not be raised anymore.

Here's a quick demonstration test case that passes:

```python
def test_assert(reraise):

    def run():
        with reraise:
            assert False

    t = Thread(target=run)
    t.start()
    t.join()

    # Return the captured exception:
    assert type(reraise.exception) is AssertionError

    # This won't do anything, since an exception has already been captured:
    reraise.exception = Exception()

    # Return the exception and set `reraise.exception` to None:
    assert type(reraise.reset()) is AssertionError

    # `Reraise` will not fail the test case because
    assert reraise.exception is None
```
