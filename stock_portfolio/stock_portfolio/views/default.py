from pyramid.response import Response
from pyramid.view import view_config
from ..sample_data import MOCK_DATA
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
import requests

API_URL = 'https://api.iextrading.com/1.0'


@view_config(route_name='home', renderer='../templates/base.jinja2')
def home_view(request):
    return {}


@view_config(route_name='auth', renderer='../templates/auth.jinja2')
def get_auth_view(request):
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
    if request.method == 'GET':
        try:
            symbol = request.GET['symbol']
        except KeyError:
            return {}
        response = requests.get(API_URL + '/stock/{}/company'.format(symbol))
        data = response.json()
        return {'company': data}
    if request.method == 'POST':
        try:
            symbol = request.POST['symbol']
        except KeyError:
            return {}
        response = requests.get(API_URL + '/stock/{}/company'.format(symbol))
        data = response.json()
        MOCK_DATA.append(data)
        return HTTPFound(location=request.route_url('portfolio'))


@view_config(route_name='portfolio', renderer='../templates/portfolio.jinja2')
def get_portfolio_view(request):
    return{'stocks': MOCK_DATA}


@view_config(route_name='portfolio/detail', renderer='../templates/stock-detail.jinja2')
def get_detail_view(request):
    symbol = request.matchdict['symbol']
    print(symbol)
    return {'stocks': MOCK_DATA,
            'symbol': symbol}
