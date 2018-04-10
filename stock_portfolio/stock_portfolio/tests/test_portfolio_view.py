def test_default_response_portfolio_view(dummy_request):
    """Test portfolio view default behavior."""
    from ..views.portfolio import get_portfolio_view

    response = get_portfolio_view(dummy_request)
    assert isinstance(response, dict)
    assert response['stocks'] == []


def test_get_stock_detail_view(dummy_request):
    """Test stock detail request."""
    from ..views.portfolio import get_detail_view
    request = dummy_request
    request.matchdict['symbol'] = 'AMD'
    response = get_detail_view(request)
    assert isinstance(response, dict)


def test_detail_empty(dummy_request):
    """Test detail view with no symbol argument."""
    from ..views.portfolio import get_detail_view
    from pyramid.httpexceptions import HTTPNotFound

    response = get_detail_view(dummy_request)
    assert isinstance(response, HTTPNotFound)


def test_detail_not_found(dummy_request):
    """Test detail view with bad symbol argument."""
    from ..views.portfolio import get_detail_view

    request = dummy_request
    request.matchdict = {'symbol': 12343252}
    response = get_detail_view(request)
    assert isinstance(response, KeyError)


def test_default_response_search_view(dummy_request):
    """Test default response on searching fo a stock."""
    from ..views.portfolio import get_stock_view
    request = dummy_request
    request.GET = {'symbol': 'MSFT'}
    response = get_stock_view(dummy_request)
    assert type(response) == dict


def test_valid_post_to_stock_view(dummy_request):
    """Test a valid post request returns status code."""
    from ..views.portfolio import get_stock_view
    from pyramid.httpexceptions import HTTPFound

    dummy_request.method = 'POST'
    dummy_request.POST = {
        'symbol': 'CRAY',
        'companyName': 'Cray Inc',
        'exchange': 'Nasdaq Global Select',
        'industry': 'Computer Hardware',
        'website': 'http://www.cray.com',
        'description': 'Cray Inc designs, develops',
        'CEO': 'Peter J. Ungaro',
        'issueType': 'cs',
        'sector': 'Technology'
    }

    response = get_stock_view(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


def test_valid_post_to_stock_view_adds_record_to_db(dummy_request, db_session):
    """Test valid post request adds record to the database."""
    from ..views.portfolio import get_stock_view
    from ..models import Stock

    dummy_request.method = 'POST'
    dummy_request.POST = {
        'symbol': 'CRAY',
        'companyName': 'Cray Inc',
        'exchange': 'Nasdaq Global Select',
        'industry': 'Computer Hardware',
        'website': 'http://www.cray.com',
        'description': 'Cray Inc designs, develops',
        'CEO': 'Peter J. Ungaro',
        'issueType': 'cs',
        'sector': 'Technology'
    }

    assert len(db_session.query(Stock).all()) == 0

    get_stock_view(dummy_request)
    query = db_session.query(Stock)
    one = query.first()
    assert one.symbol == 'CRAY'
    assert one.companyName == 'Cray Inc'
    assert type(one.id) == int


def test_invalid_post_to_stock_view(dummy_request):
    """Test an invalid post raises an error."""
    import pytest
    from ..views.portfolio import get_stock_view
    from pyramid.httpexceptions import HTTPBadRequest

    dummy_request.method = 'POST'
    dummy_request.POST = {
        'exchange': 'Nasdaq Global Select',
        'industry': 'Computer Hardware',
        'website': 'http://www.cray.com',
        'description': 'Cray Inc designs, develops',
        'CEO': 'Peter J. Ungaro',
        'issueType': 'cs',
        'sector': 'Technology'
    }

    with pytest.raises(HTTPBadRequest):
        response = get_stock_view(dummy_request)
        assert isinstance(response, HTTPBadRequest)
