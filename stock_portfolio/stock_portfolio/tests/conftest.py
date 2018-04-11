# import os
import pytest
from pyramid import testing
from ..models.meta import Base
from ..models import Stock
from ..models import Account


@pytest.fixture
def test_entry():
    """Test stock entry."""
    return Stock(
        symbol='WAT',
        companyName='Advanced Micro Wats Inc',
        exchange='NASWAT Capital Market',
        industry='Semiconductors',
        website='http://www.zombo.com',
        description='Anything is possible',
        CEO='Larry David',
        issueType='cs',
        sector='Technology'
    )


def test_account():
    """Test account entry."""
    return Account(
        username='kat',
        password='1234',
        email='kat.cosgrove@gmail.com'
    )


@pytest.fixture
def configuration(request):
    """Setup a database for testing purposes."""
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres://localhost:5432/stocks_test'
        # 'sqlalchemy.url': os.environ['TEST_DATABASE_URL']
    })
    config.include('stock_portfolio.models')
    config.include('stock_portfolio.routes')

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture
def db_session(configuration, request):
    """Create a database session for interacting with the test database."""
    SessionFactory = configuration.registry['dbsession_factory']
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Create a dummy GET request with a dbsession."""
    return testing.DummyRequest(dbsession=db_session)
