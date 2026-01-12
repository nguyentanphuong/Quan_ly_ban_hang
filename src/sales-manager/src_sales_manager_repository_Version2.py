from typing import List, Optional
from sqlalchemy.orm import Session
from src_sales_manager_models_Version2 import Product, Customer, Order, OrderItem

class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, product: Product) -> Product:
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def get(self, product_id: int) -> Optional[Product]:
        return self.session.get(Product, product_id)

    def list(self, limit: int = 100, offset: int = 0) -> List[Product]:
        return self.session.query(Product).order_by(Product.id).limit(limit).offset(offset).all()

    def update_stock(self, product_id: int, delta: int) -> Optional[Product]:
        p = self.get(product_id)
        if not p:
            return None
        p.stock += delta
        self.session.commit()
        self.session.refresh(p)
        return p

class CustomerRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, customer: Customer) -> Customer:
        self.session.add(customer)
        self.session.commit()
        self.session.refresh(customer)
        return customer

    def get(self, customer_id: int) -> Optional[Customer]:
        return self.session.get(Customer, customer_id)

    def get_by_email(self, email: str) -> Optional[Customer]:
        return self.session.query(Customer).filter_by(email=email).one_or_none()

class OrderRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, order: Order) -> Order:
        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)
        return order

    def get(self, order_id: int) -> Optional[Order]:
        return self.session.get(Order, order_id)

    def list(self, limit: int = 100, offset: int = 0) -> List[Order]:
        return self.session.query(Order).order_by(Order.id.desc()).limit(limit).offset(offset).all()