import pytest
from fastapi.testclient import TestClient
from main import app
from app.database import RESTAURANT_ID, TABLE_1_ID, DISH_BRUSCHETTA_ID

client = TestClient(app)


class TestHealth:
    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "Passione" in response.json()["message"]

    def test_health(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestMenu:
    def test_get_menu(self):
        response = client.get(f"/api/restaurants/{RESTAURANT_ID}/menu")
        assert response.status_code == 200
        data = response.json()
        assert "categories" in data
        assert len(data["categories"]) > 0

    def test_get_menu_english(self):
        response = client.get(f"/api/restaurants/{RESTAURANT_ID}/menu?lang=en")
        assert response.status_code == 200
        data = response.json()
        # Check that English names are used
        assert any("Antipasti" in cat["name"] for cat in data["categories"])

    def test_get_menu_not_found(self):
        fake_id = "99999999-9999-9999-9999-999999999999"
        response = client.get(f"/api/restaurants/{fake_id}/menu")
        assert response.status_code == 404

    def test_get_dishes(self):
        response = client.get("/api/dishes")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) > 0

    def test_get_dish(self):
        response = client.get(f"/api/dishes/{DISH_BRUSCHETTA_ID}")
        assert response.status_code == 200
        data = response.json()
        assert "Брускетта" in data["name"]


class TestTables:
    def test_get_table_by_qr(self):
        response = client.get("/api/tables/qr/passione-table-1")
        assert response.status_code == 200
        data = response.json()
        assert data["table_number"] == "1"

    def test_get_table_by_qr_not_found(self):
        response = client.get("/api/tables/qr/invalid-qr")
        assert response.status_code == 404

    def test_get_table(self):
        response = client.get(f"/api/tables/{TABLE_1_ID}")
        assert response.status_code == 200


class TestSession:
    def test_create_session(self):
        response = client.post("/api/sessions", json={
            "table_id": str(TABLE_1_ID),
            "device_id": "test-device-123",
            "language": "ru"
        })
        assert response.status_code == 201
        data = response.json()
        assert "session_token" in data
        assert data["language"] == "ru"

    def test_create_session_invalid_table(self):
        response = client.post("/api/sessions", json={
            "table_id": "99999999-9999-9999-9999-999999999999",
            "device_id": "test-device",
            "language": "ru"
        })
        assert response.status_code == 404


class TestCartAndOrder:
    def test_full_order_flow(self):
        # 1. Create session
        session_response = client.post("/api/sessions", json={
            "table_id": str(TABLE_1_ID),
            "device_id": "test-device-order",
            "language": "ru"
        })
        assert session_response.status_code == 201
        session_id = session_response.json()["id"]

        # 2. Get cart (should be empty)
        cart_response = client.get(f"/api/carts/{session_id}")
        assert cart_response.status_code == 200
        assert cart_response.json()["total_amount"] == 0

        # 3. Add item to cart
        add_item_response = client.post(f"/api/carts/{session_id}/items", json={
            "dish_id": str(DISH_BRUSCHETTA_ID),
            "quantity": 2,
            "comment": "без лука"
        })
        assert add_item_response.status_code == 201
        item_id = add_item_response.json()["id"]

        # 4. Check cart updated
        cart_response = client.get(f"/api/carts/{session_id}")
        assert cart_response.status_code == 200
        cart_data = cart_response.json()
        assert cart_data["total_amount"] == 900  # 450 * 2
        assert len(cart_data["items"]) == 1

        # 5. Update cart item quantity
        update_response = client.patch(f"/api/cart-items/{item_id}", json={
            "quantity": 3
        })
        assert update_response.status_code == 200
        assert update_response.json()["quantity"] == 3

        # 6. Create order
        order_response = client.post("/api/orders", json={
            "session_id": session_id,
            "comment": "Быстрее пожалуйста"
        })
        assert order_response.status_code == 201
        order_data = order_response.json()
        assert order_data["status"] == "PENDING"
        assert order_data["total_amount"] == 1350  # 450 * 3
        order_id = order_data["id"]

        # 7. Check cart is empty after order
        cart_response = client.get(f"/api/carts/{session_id}")
        assert cart_response.json()["total_amount"] == 0

        # 8. Get order status
        status_response = client.get(f"/api/orders/{order_id}/status")
        assert status_response.status_code == 200
        assert status_response.json()["status"] == "PENDING"

        # 9. Update order status (staff action)
        update_status = client.patch(f"/api/orders/{order_id}/status", json={
            "status": "CONFIRMED"
        })
        assert update_status.status_code == 200
        assert update_status.json()["status"] == "CONFIRMED"

        # 10. Get all orders
        orders_response = client.get("/api/orders")
        assert orders_response.status_code == 200
        assert len(orders_response.json()["data"]) > 0


class TestOrders:
    def test_get_orders_filter_by_status(self):
        response = client.get("/api/orders?status=PENDING")
        assert response.status_code == 200

    def test_get_order_not_found(self):
        fake_id = "99999999-9999-9999-9999-999999999999"
        response = client.get(f"/api/orders/{fake_id}")
        assert response.status_code == 404
