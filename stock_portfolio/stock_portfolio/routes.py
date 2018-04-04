def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('auth', '/auth')
    config.add_route('register', '/register')
    config.add_route('stock', '/stock')
    config.add_route('portfolio', '/portfolio')
    config.add_route('portfolio/{symbol}', '/portfolio/{symbol}')
