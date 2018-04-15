stock_portfolio [![Build Status](https://travis-ci.org/katcosgrove/stock-portfolio.svg?branch=master)](https://travis-ci.org/katcosgrove/stock-portfolio)
===============
Getting Started
---------------

- Change directory into your newly created project.

    cd stock_portfolio

- Create a Python virtual environment.

    python3 -m venv env

- Upgrade packaging tools.

    env/bin/pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.

    env/bin/pip install -e ".[testing]"

- Configure the database.

    env/bin/initialize_stock_portfolio_db development.ini

- Run your project's tests.

    env/bin/pytest

- Run your project.

    env/bin/pserve development.ini
