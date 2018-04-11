from pyramid import testing
from pyramid.response import Response


def test_default_behavior_of_base_view(dummy_request):
    """Test default homepage behavior."""
    from ..views.base import home_view
    response = home_view(dummy_request)
    assert len(response) == 0
    assert type(response) == dict


# def test_base_view_status_code(dummy_request):
#     """Test default homepage behavior."""
#     from ..views.base import home_view
#     response = home_view(dummy_request)
#     assert response.status_code == 200
