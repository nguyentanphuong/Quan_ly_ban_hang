import pytest
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.sales_manager.models import Base
from src.sales_manager.service import SalesService

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, expire_on_commit=False, future=True)
    s = Session()
    yield s
    s.close()

def test_create_product_and_customer(session):
    svc = SalesService(session)
    p = svc.create_product("Gadget", Decimal("19.99"), 10)
    assert p.id is not None
    c = svc.create_customer("A", "B", "a@b.com")
    assert c.id is not None

def test_create_order_reduces_stock(session):
    svc = SalesService(session)
    p = svc.create_product("Gizmo", Decimal("5.00"), 5)
    c = svc.create_customer("John", "Doe", "john@example.com")
    order = svc.create_order(c.id, [{"product_id": p.id, "quantity": 3}])
    assert order.total == Decimal("15.00")
    # Refresh product
    refreshed = session.get(type(p), p.id)
    assert refreshed.stock == 2

def test_insufficient_stock_raises(session):
    svc = SalesService(session)
    p = svc.create_product("Limited", Decimal("10.00"), 1)
    c = svc.create_customer("Mary", "Ann", "mary@example.com")
    with pytest.raises(ValueError):
        svc.create_order(c.id, [{"product_id": p.id, "quantity": 2}])