import pytest
from pyramid import testing


@pytest.fixture
def dummy_request():
    return testing.DummyRequest()


@pytest.fixture
def dummy_auth_request():
    from pyramid.request import Request
    request = testing.DummyRequest()
    request.method = 'POST'
    request.POST = {'username': 'dummy', 'password': '1234'}

    return request
