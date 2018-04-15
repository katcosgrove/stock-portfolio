from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from ..models import Stock
from ..models import Junction
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
            return {'message': 'That stock symbol does not exist.'}

    if request.method == 'POST':

        instance = Stock(
            symbol=request.POST['symbol'],
            companyName=request.POST['company'],
            exchange=request.POST['exchange'],
            industry=request.POST['industry'],
            website=request.POST['website'],
            description=request.POST['description'],
            CEO=request.POST['CEO'],
            issueType=request.POST['issueType'],
            sector=request.POST['sector'],
        )

        junction = Junction(
            account_id=request.authenticated_userid,
            stock_id=instance.symbol
        )

        try:
            stock_query = request.dbsession.query(Stock)
            if stock_query.filter(Stock.symbol == instance.symbol).first() is None:
                request.dbsession.add(instance)

            if stock_query.filter(instance.symbol == Junction.stock_id, junction.account_id == Junction.account_id).first() is None:
                request.dbsession.add(junction)
            else:
                return{'message': 'You already have that in your portfolio.'}

        except DBAPIError:
            return Response(DB_ERR_MSG, content_type='text/plain', status=500)

        return HTTPFound(location=request.route_url('portfolio'))


@view_config(route_name='portfolio', renderer='../templates/portfolio.jinja2')
def get_portfolio_view(request):
    """Load portfolio from database and display it."""
    try:
        query = request.dbsession.query(Stock)
        user_stocks = query.filter(Junction.account_id == request.authenticated_userid, Junction.stock_id == Stock.symbol)

    except DBAPIError:
        raise DBAPIError(DB_ERR_MSG, content_type='text/plain', status=500)

    return{'stocks': user_stocks}


@view_config(route_name='detail', renderer='../templates/stock-detail.jinja2')
def get_detail_view(request):
    """Display details of selected stock."""
    try:
        symbol = request.matchdict['symbol']
    except KeyError:
        raise HTTPNotFound()

    try:
        query = request.dbsession.query(Stock)
        stock_detail = query.filter(Junction.account_id == request.authenticated_userid).filter(Stock.symbol == symbol).one_or_none()

    except DBAPIError:
        raise KeyError('That stock symbol is not in the database.')

    if stock_detail is None:
        raise HTTPNotFound()

    return {'stock': stock_detail}
