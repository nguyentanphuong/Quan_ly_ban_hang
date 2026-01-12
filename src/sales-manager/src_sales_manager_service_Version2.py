from typing import List, Dict, Optional
from decimal import Decimal
from sqlalchemy.orm import Session
from src_sales_manager_repository_Version2 import ProductRepository, CustomerRepository, OrderRepository
from src_sales_manager_models_Version2 import Product, Customer, Order, OrderItem

class SalesService:
    """
    Business rules implemented here:
    - When creating an order: verify customer exists, verify product stock >= requested qty.
    - Reserve/decrement stock when order is created (within same transaction).
    - Calculate order total based on product price at time of order.
    """

    def __init__(self, session: Session):
        self.session = session
        self.prod_repo = ProductRepository(session)
        self.cust_repo = CustomerRepository(session)
        self.order_repo = OrderRepository(session)

    def create_product(self, name: str, price: Decimal, stock: int) -> Product:
        p = Product(name=name, price=price, stock=stock)
        return self.prod_repo.add(p)

    def list_products(self, limit: int = 100, offset: int = 0) -> List[Product]:
        return self.prod_repo.list(limit=limit, offset=offset)

    def create_customer(self, first_name: str, last_name: str, email: str) -> Customer:
        existing = self.cust_repo.get_by_email(email)
        if existing:
            raise ValueError("Email already exists")
        c = Customer(first_name=first_name, last_name=last_name, email=email)
        return self.cust_repo.add(c)

    def create_order(self, customer_id: int, items: List[Dict[str, int]]) -> Order:
        """
        items: list of dicts with keys 'product_id' and 'quantity'
        Example: [{'product_id':1, 'quantity':2}, {'product_id':2, 'quantity':1}]
        """
        # Basic validations
        customer = self.cust_repo.get(customer_id)
        if not customer:
            raise ValueError("Customer not found")

        # We'll perform checks and stock updates in a transactional manner.
        # Using the same session ensures atomicity for our simple use-case.
        order = Order(customer_id=customer_id, total=0)
        total = Decimal("0.00")
        order_items = []

        for it in items:
            pid = int(it["product_id"])
            qty = int(it["quantity"])
            if qty <= 0:
                raise ValueError("Quantity must be positive")

            product = self.prod_repo.get(pid)
            if not product:
                raise ValueError(f"Product {pid} not found")
            if product.stock < qty:
                raise ValueError(f"Insufficient stock for product {product.name} (id={pid})")

            line_price = Decimal(product.price) * qty
            total += line_price

            # decrement stock
            product.stock -= qty
            # create order item with price snapshot
            oi = OrderItem(product_id=pid, quantity=qty, price=product.price)
            order_items.append(oi)

        order.total = total
        order.items = order_items

        # Persist: add order and commit; product stock changes are already in session
        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)
        return order

    def list_orders(self, limit: int = 100, offset: int = 0) -> List[Order]:
        return self.order_repo.list(limit=limit, offset=offset)

    def get_order(self, order_id: int) -> Optional[Order]:
        return self.order_repo.get(order_id)