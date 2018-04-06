def test_default_behavior_of_base_view(dummy_request):
    from ..views.default import home_view
    from pyramid.response import Response

    request = dummy_request
    response = home_view(request)
    assert response == 'you did the thing'


def test_default_behavior_of_portfolio_view(dummy_request):
    from ..views.default import get_portfolio_view
    request = dummy_request
    response = get_portfolio_view(dummy_request)
    assert type(response) == dict
    assert response['stocks'][0]['symbol'] == 'AMD'


def test_get_stock_view(dummy_request):
    from ..views.default import get_stock_view
    request = dummy_request
    response = get_stock_view(dummy_request)
    assert type(response) == dict


# def test_get_stock_view(dummy_request):
#     from ..views.default import get_stock_view
#     request = dummy_request
#     response = get_stock_view(dummy_request)
#     assert type(response) == dict


# def test_get_stock_view(dummy_request):
#     from ..views.default import get_stock_view
#     request = dummy_request
#     response = get_stock_view(dummy_request)
#     assert type(response) == dict


# def test_get_stock_view(dummy_request):
#     from ..views.default import get_stock_view
#     request = dummy_request
#     response = get_stock_view(dummy_request)
#     assert type(response) == dict
