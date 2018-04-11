def test_get_auth_view(dummy_request):
    """Test default auth page behavior."""
    from ..views.auth import get_auth_view
    response = get_auth_view(dummy_request)
    assert isinstance(response, dict)


def test_auth_signup_view(dummy_request):
    """Test successful signup."""
    from ..views.auth import get_auth_view
    from pyramid.httpexceptions import HTTPFound

    dummy_request.POST = {'username': 'kat', 'password': '1234', 'email': 'kat@kat.com'}
    dummy_request.method = 'POST'
    response = get_auth_view(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


# def test_auth_signin_view(dummy_request):
#     """Test successful sign in."""
#     from ..views.auth import get_auth_view
#     from pyramid.httpexceptions import HTTPFound

#     dummy_request.GET = {'username': 'kat', 'password': '1234'}
#     response = get_auth_view(dummy_request)
#     assert response.status_code == 302
#     assert isinstance(response, HTTPFound)


def test_bad_request_auth_signup_view(dummy_request):
    """Test bad signup."""
    from ..views.auth import get_auth_view
    from pyramid.httpexceptions import HTTPBadRequest

    dummy_request.POST = {'password': 'whodat', 'email': 'wat@wat.com'}
    dummy_request.method = 'POST'
    response = get_auth_view(dummy_request)
    assert response.status_code == 400
    assert isinstance(response, HTTPBadRequest)


def test_bad_request_method_auth_signup_view(dummy_request):
    """Test bad method for signup."""
    from ..views.auth import get_auth_view
    from pyramid.httpexceptions import HTTPFound

    dummy_request.POST = {'password': 'whodat', 'email': 'wat@wat.com'}
    dummy_request.method = 'PUT'
    response = get_auth_view(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)
