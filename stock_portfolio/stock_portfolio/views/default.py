from pyramid.response import Response
from pyramid.view import view_config
from ..sample_data import MOCK_DATA
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from ..models import Stock
import requests
from . import DB_ERR_MSG
from sqlalchemy.exc import DBAPIError


API_URL = 'https://api.iextrading.com/1.0'


@view_config(route_name='home', renderer='../templates/base.jinja2')
def home_view(request):
    """Returns homepage."""
    return {}


@view_config(route_name='auth', renderer='../templates/auth.jinja2')
def get_auth_view(request):
    """GET and POST routes for registration and login."""
    if request.method == 'GET':
        try:
            username = request.GET['username']
            password = request.GET['password']
            print('User: {}, Pass: {}'.format(username, password))

            return HTTPFound(location=request.route_url('portfolio'))

        except KeyError:
            return {}

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print('User: {}, Pass: {}'.format(username, password))

        return HTTPFound(location=request.route_url('portfolio'))

    return HTTPNotFound()


@view_config(route_name='stock', renderer='../templates/stock-add.jinja2')
def get_stock_view(request):
    """GET and POST routes for stock search and adding new stock to portfolio."""
    if request.method == 'GET':
        try:
            symbol = request.GET['symbol']
        except KeyError:
            return {}
        try:
            response = requests.get(API_URL + '/stock/{}/company'.format(symbol))
            data = response.json()
            return {'company': data}
        except ValueError:
            return{'message': 'That stock symbol does not exist!'}

    if request.method == 'POST':
        try:
            symbol = request.POST['symbol']
        except KeyError:
            return {}

        response = requests.get(API_URL + '/stock/{}/company'.format(symbol))
        data = response.json()
        query = request.dbsession.query(Stock)
        e = Stock(**data)
        if query.filter(Stock.symbol == data['symbol']).first() is None:
            request.dbsession.add(e)
        else:
            request.dbsession.query(Stock).update(e)
        return HTTPFound(location=request.route_url('portfolio'))


@view_config(route_name='portfolio', renderer='../templates/portfolio.jinja2')
def get_portfolio_view(request):
    """Load portfolio from database and display it."""
    try:
        query = request.dbsession.query(Stock)
        all_entries = query.all()

    except DBAPIError:
        return DBAPIError(DB_ERR_MSG, content_type='text/plain', status=500)

    return{'stocks': all_entries}


@view_config(route_name='portfolio/detail', renderer='../templates/stock-detail.jinja2')
def get_detail_view(request):
    """Display details of selected stock."""
    try:
        symbol = request.matchdict['symbol']
    except IndexError:
        return HTTPNotFound()

    try:
        query = request.dbsession.query(Stock)
        stock_detail = query.filter(Stock.symbol == symbol).first()
    except DBAPIError:
        return DBAPIError(DB_ERR_MSG, content_type='text/plain', status=500)
    return {'stock': stock_detail}
