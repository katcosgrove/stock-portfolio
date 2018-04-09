from pyramid import testing
from pyramid.response import Response


def test_default_behavior_of_base_view(dummy_request):
    """Test default homepage behavior."""
    from ..views.default import home_view
    response = home_view(dummy_request)
    assert isinstance(response, dict)


def test_default_behavior_of_portfolio_view(dummy_request):
    """Test default portfolio behavior."""
    from ..views.default import get_portfolio_view
    response = get_portfolio_view(dummy_request)
    assert isinstance(response, dict)
    assert response['stocks'][0]['symbol'] == 'AMD'


def test_get_stock_view_status(dummy_request):
    """Test default stock view behavior."""
    from ..views.default import get_stock_view
    response = get_stock_view(dummy_request)
    assert isinstance(response, dict)


def test_get_auth_view(dummy_request):
    """Test default auth page behavior."""
    from ..views.default import get_auth_view
    response = get_auth_view(dummy_request)
    assert isinstance(response, dict)


# def test_sign_in_to_auth(dummy_auth_request):
#     """Test login behavior."""
#     # test HTTPfound and 302
#     from ..views.default import get_auth_view
#     from pyramid.httpexceptions import HTTPFound
#     response = get_auth_view(dummy_auth_request)
#     assert isinstance(response, HTTPFound)


def test_get_stock_detail_view(dummy_request):
    """Test specific stock detail request."""
    from ..views.default import get_detail_view
    request = dummy_request
    request.matchdict['symbol'] = 'AMD'
    response = get_detail_view(request)
    assert isinstance(response, dict)
