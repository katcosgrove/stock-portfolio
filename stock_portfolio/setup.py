import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'cryptacular',
    'plaster_pastedeploy',
    'psycopg2',
    'pyramid >= 1.9a',
    'pyramid_debugtoolbar',
    'pyramid_jinja2',
    'pyramid_retry',
    'pyramid_tm',
    'requests',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',
    'pytest-cov',
]

setup(
    name='stock_portfolio',
    version='0.0',
    description='stock_portfolio',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Kat Cosgrove',
    author_email='kat.cosgrove@gmail.com',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = stock_portfolio:main',
        ],
        'console_scripts': [
            'initialize_stock_portfolio_db = stock_portfolio.scripts.initializedb:main',
        ],
    },
)
