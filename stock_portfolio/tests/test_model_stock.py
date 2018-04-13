def test_constructed_entry_added_to_database(db_session):
    """Test adding a complete stock entry."""
    from ..models import Stock

    assert len(db_session.query(Stock).all()) == 0
    stock = Stock(
        symbol='TEST',
        companyName='Advanced TEST Wats Inc',
        exchange='NASWAT TEST Market',
        industry='TESTconductors',
        website='http://www.zombo.com',
        description='AnyTEST is possible',
        CEO='Larry TEST David',
        issueType='cs',
        sector='Technology'
    )
    db_session.add(stock)
    assert len(db_session.query(Stock).all()) == 1


def test_constructed_entry_with_incomplete_added(db_session):
    """Test adding incomplete data but with required fields."""
    from ..models import Stock

    assert len(db_session.query(Stock).all()) == 0
    stock = Stock(
        symbol='TEST2',
        companyName='Test Conglomerate'
    )
    db_session.add(stock)
    assert len(db_session.query(Stock).all()) == 1


def test_entry_with_no_symbol_throws_error(db_session):
    """Test adding stock with required field empty."""
    from ..models import Stock
    import pytest
    from sqlalchemy.exc import IntegrityError

    assert len(db_session.query(Stock).all()) == 0
    stock = Stock(
        companyName='Evil Test Conglomerate',
        CEO='Aleister Crowley',
        description='Tests designed to break your code.'
    )
    with pytest.raises(IntegrityError):
        db_session.add(stock)
        assert db_session.query(Stock).one_or_none() is None
