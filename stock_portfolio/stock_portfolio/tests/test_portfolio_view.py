from pyramid.httpexceptions import HTTPNotFound
import pytest


def test_default_response_portfolio_view(dummy_request):
    """Test portfolio view default behavior."""
    from ..views.portfolio import get_portfolio_view

    response = get_portfolio_view(dummy_request)
    assert isinstance(response, dict)


# def test_get_stock_detail_view(dummy_request):
#     """Test stock detail request."""
#     from ..views.portfolio import get_detail_view
#     request = dummy_request
#     request.matchdict['symbol'] = 'AMD'
#     response = get_detail_view(request)
#     assert isinstance(response, dict)


def test_detail_empty(dummy_request):
    """Test detail view with no symbol argument."""
    from ..views.portfolio import get_detail_view

    with pytest.raises(HTTPNotFound):
        request = dummy_request
        response = get_detail_view(request)
        assert isinstance(response, HTTPNotFound)


def test_detail_not_found(dummy_request):
    """Test detail view with bad symbol argument."""
    from ..views.portfolio import get_detail_view

    with pytest.raises(KeyError):
        request = dummy_request
        request.matchdict = {'symbol': 12343252}
        get_detail_view(request)


def test_default_response_search_view(dummy_request):
    """Test default response on searching for a stock."""
    from ..views.portfolio import get_stock_view

    request = dummy_request
    request.GET = {'symbol': 'MSFT'}
    response = get_stock_view(dummy_request)
    assert type(response) == dict


def test_valid_post_to_stock_view(dummy_request):
    """Test a valid post request returns status code."""
    from ..views.portfolio import get_stock_view
    # from ..views.auth import get_auth_view
    from pyramid.httpexceptions import HTTPFound

    dummy_request.method = 'POST'
    dummy_request.POST = {
        'symbol': 'CRAY',
        'company': 'Cray Inc',
        'exchange': 'Nasdaq Global Select',
        'industry': 'Computer Hardware',
        'website': 'http://www.cray.com',
        'description': 'Cray Inc designs, develops',
        'CEO': 'Peter J. Ungaro',
        'issueType': 'cs',
        'sector': 'Technology'
    }

    response = get_stock_view(dummy_request)
    assert isinstance(response, HTTPFound)


# def test_valid_post_to_stock_view_adds_record_to_db(dummy_request, db_session):
#     """Test valid post request adds record to the database."""
#     from ..views.portfolio import get_stock_view
#     from ..views.auth import get_auth_view
#     from ..models import Stock

#     dummy_request.POST = {'username': 'kat', 'password': '1234', 'email': 'kat@kat.com'}
#     dummy_request.method = 'POST'
#     get_auth_view(dummy_request)

#     dummy_request.GET = {'username': 'kat', 'password': '1234'}
#     dummy_request.method = 'GET'
#     get_auth_view(dummy_request)

#     dummy_request.method = 'POST'
#     dummy_request.POST = {
#         'symbol': 'CRAY',
#         'company': 'Cray Inc',
#         'exchange': 'Nasdaq Global Select',
#         'industry': 'Computer Hardware',
#         'website': 'http://www.cray.com',
#         'description': 'Cray Inc designs, develops',
#         'CEO': 'Peter J. Ungaro',
#         'issueType': 'cs',
#         'sector': 'Technology'
#     }

#     dummy_request.authenticated_userid = 'kat'

#     get_stock_view(dummy_request)
#     query = db_session.query(Stock)
#     one = query.first()
#     assert one.symbol == 'CRAY'
#     assert one.company == 'Cray Inc'


def test_invalid_post_to_stock_view(dummy_request):
    """Test an invalid post raises an error."""
    import pytest
    from ..views.portfolio import get_stock_view

    dummy_request.method = 'POST'
    dummy_request.POST = {'symbol': None}

    with pytest.raises(KeyError):
        get_stock_view(dummy_request)
