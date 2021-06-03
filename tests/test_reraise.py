from _pytest.pytester import HookRecorder
from _pytest.reports import TestReport

import pytest


@pytest.fixture
def recorder(testdir: "pytest.Testdir"):
    """
    HookRecorder from a sample test session from the `samples` directory
    """
    testdir.copy_example()
    yield testdir.inline_run()


def assert_failure_contains(function_name: str, failure: TestReport, string: str):
    """
    Given a test function name, the corresponding failure TestReport object, and an
    arbitrary string, makes sure that the TestReport belongs to the specified function
    name and the failure text contains the string.
    """
    assert failure.nodeid.split("::")[-1] == function_name
    assert string in failure.longreprtext


def test_no_exception(recorder: HookRecorder):
    recorder.assertoutcome(passed=2)


def test_single_exception(recorder: HookRecorder):
    recorder.assertoutcome(failed=2)

    failures = recorder.getfailures()
    assert_failure_contains("test_reraise", failures[0], "assert False")
    assert_failure_contains("test_exception", failures[1], "assert False")


def test_multiple_exceptions(recorder: HookRecorder):
    recorder.assertoutcome(failed=4)

    failures = recorder.getfailures()
    assert_failure_contains("test_reraise_first", failures[0], "assert False")
    assert_failure_contains("test_reraise_last", failures[1], "assert False")
    assert_failure_contains(
        "test_reraise_multiple_threads_first", failures[2], "assert 0 == -1"
    )
    assert_failure_contains(
        "test_reraise_multiple_threads_last", failures[3], "assert 0 == -1"
    )


def test_in_nested_fixture(recorder: HookRecorder):
    recorder.assertoutcome(passed=1, failed=3)

    failures = recorder.getfailures()
    assert_failure_contains("test_reraise_setup_fixture", failures[0], "assert False")
    assert_failure_contains("test_reraise_in_fixture", failures[1], "assert False")
    assert_failure_contains(
        "test_reraise_teardown_fixture", failures[2], "assert False"
    )


def test_exception_access(recorder: HookRecorder):
    recorder.assertoutcome(passed=1, failed=1)

    failures = recorder.getfailures()
    assert_failure_contains(
        "test_manual_reraise_precedence", failures[0], "Exception: A"
    )


def test_catching(recorder: HookRecorder):
    recorder.assertoutcome(passed=3)
