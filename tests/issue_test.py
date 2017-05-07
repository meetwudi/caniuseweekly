import pytest

from caniuseweekly.issue import default_previous_sha
from caniuseweekly.issue import DefaultPreviousSHANotDefinedError


def test_default_previous_sha_not_defined():
    with pytest.raises(DefaultPreviousSHANotDefinedError):
        default_previous_sha()
