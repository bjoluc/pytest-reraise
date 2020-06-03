__version__ = "1.0.2"

import pytest

from pytest_reraise import reraise
from pytest_reraise.reraise import Reraise

__all__ = ["reraise", "Reraise", "__version__"]

pytest.register_assert_rewrite("pytest_reraise.reraise")
