```markdown
# Sales Manager (Python) — Mẫu đơn giản

Ứng dụng mẫu quản lý bán hàng (Product, Customer, Order) bằng Python + SQLAlchemy + Click.

Tính năng:
- Quản lý sản phẩm (tên, giá, tồn kho)
- Quản lý khách hàng (tên, email)
- Tạo đơn hàng (Order + OrderItem), kiểm tra tồn kho và giảm tồn kho khi tạo đơn
- CLI để thao tác: init-db, add-product, list-products, add-customer, create-order, list-orders, get-order
- Tests cơ bản với pytest (SQLite in-memory)

Cài đặt:
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Khởi tạo database:
```bash
python -m src.sales_manager.main init-db
```

Ví dụ dùng CLI:
```bash
# Thêm sản phẩm
python -m src.sales_manager.main add-product --name "Widget" --price 9.99 --stock 100

# Thêm khách hàng
python -m src.sales_manager.main add-customer --first "Nguyen" --last "Phuong" --email "phuong@example.com"

# Tạo đơn: chỉ định customer_id và các cặp product_id:quantity (cách nhau bằng dấu phẩy)
python -m src.sales_manager.main create-order --customer 1 --items "1:2,2:1"

# Liệt kê đơn
python -m src.sales_manager.main list-orders
python -m src.sales_manager.main get-order --id 1
```

Chạy tests:
```bash
pytest
```

Mở rộng:
- Dùng Alembic cho migration, chuyển sang PostgreSQL cho production.
- Thêm endpoint REST (FastAPI) sử dụng cùng `service`.
- Thêm tính năng thanh toán, trạng thái đơn (pending, paid, shipped), báo cáo doanh thu.
```