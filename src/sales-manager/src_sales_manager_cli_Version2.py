import click
from decimal import Decimal
from src_sales_manager_db_Version2 import Session, init_db
from src_sales_manager_service_Version2 import SalesService

@click.group()
def cli():
    """Sales Manager CLI"""
    pass

@cli.command("init-db")
def init_db_cmd():
    init_db()
    click.echo("Initialized database.")

@cli.command("add-product")
@click.option('--name', prompt='Tên sản phẩm', help='Nhập tên sản phẩm') #("--name", required=True, help="Product name")
@click.option('--price', prompt='Giá sản phẩm', help='Nhập Giá sản phẩm') #("--price", required=True, type=float, help="Price")
@click.option('--stock', prompt='Loại sản phẩm', help='Nhập loại sản phẩm') #("--stock", required=True, type=int, help="Initial stock")
def add_product(name, price, stock):
    session = Session()
    try:
        service = SalesService(session)
        p = service.create_product(name, Decimal(str(price)), stock)
        #click.echo(f"Added product id={p.id} name={p.name} stock={p.stock}")
        click.echo(f"Đã thêm sản phẩm: id={p.id} name={p.name} stock={p.stock} price={p.price}")
    except Exception as e:
        click.echo(f"Error: {e}")
    finally:
        session.close()

@cli.command("list-products")
def list_products():
    session = Session()
    try:
        service = SalesService(session)
        for p in service.list_products():
            click.echo(f"{p.id}: {p.name} price={p.price} stock={p.stock}")
    finally:
        session.close()

@cli.command("add-customer")
@click.option("--first", "first_name", required=True)
@click.option("--last", "last_name", required=True)
@click.option("--email", required=True)
def add_customer(first_name, last_name, email):
    session = Session()
    try:
        service = SalesService(session)
        c = service.create_customer(first_name, last_name, email)
        click.echo(f"Added customer id={c.id} email={c.email}")
    except Exception as e:
        click.echo(f"Error: {e}")
    finally:
        session.close()

@cli.command("create-order")
@click.option("--customer", "customer_id", required=True, type=int, help="Customer ID")
@click.option("--items", required=True, help="Items format product_id:qty,product_id:qty  (e.g. 1:2,2:1)")
def create_order(customer_id, items):
    session = Session()
    try:
        service = SalesService(session)
        parsed = []
        for part in items.split(","):
            pid_str, qty_str = part.split(":")
            parsed.append({"product_id": int(pid_str.strip()), "quantity": int(qty_str.strip())})
        order = service.create_order(customer_id, parsed)
        click.echo(f"Created order id={order.id} total={order.total}")
    except Exception as e:
        # rollback already handled by session if exception occurs before commit; explicit rollback:
        session.rollback()
        click.echo(f"Error: {e}")
    finally:
        session.close()

@cli.command("list-orders")
def list_orders():
    session = Session()
    try:
        service = SalesService(session)
        for o in service.list_orders():
            click.echo(f"{o.id}: customer={o.customer_id} total={o.total} items={len(o.items)}")
    finally:
        session.close()

@cli.command("get-order")
@click.option("--id", "order_id", required=True, type=int)
def get_order(order_id):
    session = Session()
    try:
        service = SalesService(session)
        o = service.get_order(order_id)
        if not o:
            click.echo("Not found")
            return
        click.echo(f"Order {o.id} customer={o.customer_id} total={o.total}")
        for it in o.items:
            click.echo(f" - product={it.product_id} qty={it.quantity} price={it.price}")
    finally:
        session.close()