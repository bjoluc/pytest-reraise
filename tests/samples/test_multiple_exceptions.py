"""
All tests should fail.
"""

from threading import Thread


def test_reraise_first(reraise):
    def run():
        with reraise:
            assert False

    t = Thread(target=run)
    t.start()
    t.join()
    assert "foo" == "bar"


def test_reraise_last(reraise):
    def run():
        with reraise:
            assert False

    Thread(target=run).start()
    assert "foo" == "bar"


# test_reraise_multiple_threads_first – abbreviation to prevent truncating in stdout
def test_reraise_mtf(reraise):
    def run(thread_id: int):
        with reraise:
            assert thread_id == -1

    threads = [Thread(target=run, args=(thread_id,)) for thread_id in range(2)]
    for thread in threads:
        thread.start()
        thread.join()

    assert "foo" == "bar"


# test_reraise_multiple_threads_last – abbreviation to prevent truncating in stdout
def test_reraise_mtl(reraise):
    def run(thread_id: int):
        with reraise:
            assert thread_id == -1

    for thread_id in range(2):
        Thread(target=run, args=(thread_id,)).start()
    assert "foo" == "bar"
