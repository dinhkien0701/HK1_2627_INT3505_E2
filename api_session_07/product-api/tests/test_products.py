from sqlalchemy import event
from product_api.extensions import db

def test_create_product_post(client):
    """YÊU CẦU 1: Test endpoint POST /api/v1/products"""
    res = client.post("/api/v1/products", json={
        "sku": "NEW01", 
        "name": "Sản phẩm mới", 
        "price_cents": 5000
    })
    assert res.status_code == 201
    assert res.json["sku"] == "NEW01"
    assert res.json["id"] is not None

def test_get_order_eager_loading(client):
    """YÊU CẦU 2: Test endpoint GET /api/v1/orders/<id> có sử dụng eager loading"""
    # 1. Tạo 1 đơn hàng mua 2 sản phẩm (sản phẩm mẫu id=1 đã tạo ở conftest)
    res_create = client.post("/api/v1/orders", json={
        "items": [{"product_id": 1, "quantity": 2}]
    })
    order_id = res_create.json["id"]
    
    # 2. Gọi GET để lấy chi tiết đơn hàng
    res_get = client.get(f"/api/v1/orders/{order_id}")
    
    # 3. Kiểm tra kết quả
    assert res_get.status_code == 200
    assert res_get.json["id"] == order_id
    assert len(res_get.json["items"]) == 1
    assert res_get.json["items"][0]["quantity"] == 2

def test_query_count_no_n_plus_1(client):
    """YÊU CẦU 3 (Khuyến khích): Đếm số truy vấn để phát hiện N+1"""
    # Tạo đơn hàng
    res_create = client.post("/api/v1/orders", json={"items": [{"product_id": 1, "quantity": 2}]})
    order_id = res_create.json["id"]
    
    # Đếm số query khi gọi GET
    query_count = 0
    def count_queries(conn, cursor, statement, parameters, context, executemany):
        nonlocal query_count
        query_count += 1
        
    event.listen(db.engine, "before_cursor_execute", count_queries)
    
    client.get(f"/api/v1/orders/{order_id}")
    
    event.remove(db.engine, "before_cursor_execute", count_queries)
    
    print(f"\n[Số lượng truy vấn SQL]: {query_count}")
    # Nếu dùng selectinload, số query thường là 2 (1 cho Order, 1 cho OrderItem)
    # Nếu bị N+1, số query sẽ tăng vọt lên (1 + N)
    assert query_count <= 2 