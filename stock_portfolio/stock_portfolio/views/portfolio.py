from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPBadRequest
from ..models import Stock
import requests
from . import DB_ERR_MSG
from sqlalchemy.exc import DBAPIError

API_URL = 'https://api.iextrading.com/1.0'


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
            raise HTTPNotFound()

    if request.method == 'POST':

        symbol = request.POST['symbol']
        if symbol is None:
            raise HTTPBadRequest()

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


@view_config(route_name='detail', renderer='../templates/stock-detail.jinja2')
def get_detail_view(request):
    """Display details of selected stock."""
    try:
        symbol = request.matchdict['symbol']
    except KeyError:
        return HTTPNotFound()

    try:
        query = request.dbsession.query(Stock)
        stock_detail = query.filter(Stock.symbol == symbol).first()
    except DBAPIError:
        return KeyError('That stock symbol is not in the database.')

    return {'stock': stock_detail}
