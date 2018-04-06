import pytest
from pyramid import testing


@pytest.fixture
def dummy_request():
    return testing.DummyRequest()
