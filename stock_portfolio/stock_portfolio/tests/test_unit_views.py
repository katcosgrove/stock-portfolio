from pyramid import testing
from pyramid.response import Response


# def test_default_behavior_of_base_view(dummy_request):
#     from ..views.default import home_view
#     request = testing.DummyRequest()
#     response = home_view(request)
#     assert isinstance(response, Response)


def test_default_behavior_of_portfolio_view(dummy_request):
    from ..views.default import get_portfolio_view
    response = get_portfolio_view(dummy_request)
    assert type(response) == dict
    assert response['stocks'][0]['symbol'] == 'AMD'


def test_get_stock_view(dummy_request):
    from ..views.default import get_stock_view
    response = get_stock_view(dummy_request)
    assert type(response) == dict


# def test_get_stock_view_status(dummy_request):
#     from ..views.default import get_stock_view
#     response = get_stock_view(dummy_request)
#     assert response.status_code == 200


def test_get_auth_view(dummy_request):
    from ..views.default import get_auth_view
    response = get_auth_view(dummy_request)
    assert type(response) == dict


# def test_get_stock_detail_view(dummy_request):
#     from ..views.default import get_detail_view
#     response = get_detail_view(dummy_request)
#     assert type(response) == dict
