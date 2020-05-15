import pytest
from threading import Thread


# Raising an exception from a fixture during the setup phase
@pytest.fixture
def reraise_setup_fixture(reraise):
    def run():
        with reraise:
            assert False

    t = Thread(target=run)
    t.start()
    t.join()


# Should fail
def test_reraise_setup_fixture(reraise_setup_fixture):
    pass


# Raising an exception from a fixture during the test itself
@pytest.fixture
def reraise_in_fixture(reraise):
    def run():
        with reraise:
            assert False

    t = Thread(target=run)
    yield t


# Should fail
def test_reraise_in_fixture(reraise_in_fixture):
    reraise_in_fixture.start()
    reraise_in_fixture.join()


# Raising an exception from a fixture during the teardown phase
@pytest.fixture
def reraise_teardown_fixture(reraise):
    def run():
        with reraise:
            assert False

    yield
    t = Thread(target=run)
    t.start()
    t.join()


# Should pass, but the teardown should error
def test_reraise_teardown_fixture(reraise_teardown_fixture):
    pass
