import pytest


@pytest.fixture
def result(testdir):
    """
    Result of running a sample test session from the `samples` directory
    """
    testdir.copy_example()
    yield testdir.runpytest()


def test_no_exception(result):
    result.assert_outcomes(passed=2)


def test_single_exception(result):
    result.assert_outcomes(failed=2)
    result.stdout.re_match_lines_random(
        [
            "FAILED .*:test_reraise - assert False",
            "FAILED .*:test_exception - assert False",
        ]
    )


def test_multiple_exceptions(result):
    result.assert_outcomes(failed=4)
    result.stdout.re_match_lines_random(
        [
            "FAILED .*:test_reraise_first - assert False",
            "FAILED .*:test_reraise_last - assert False",
            "FAILED .*:test_reraise_mtf - assert 0 == -1",
            "FAILED .*:test_reraise_mtl - assert 0 == -1",
        ]
    )


def test_in_nested_fixture(result):
    result.assert_outcomes(failed=2, passed=1, error=1)
    result.stdout.re_match_lines_random(
        [
            "FAILED .*:test_reraise_setup_fixture - assert False",
            "FAILED .*:test_reraise_in_fixture - assert False",
            "ERROR .*:test_reraise_teardown_fixture - assert False",
        ],
    )


def test_exception_access(result):
    result.assert_outcomes(passed=1)


def test_catching(result):
    result.assert_outcomes(passed=3)
