from app.extensions import db
from app.models import Product, StockMovement

def test_login_required(client):
    response = client.get("/")
    assert response.status_code == 302

def test_create_product_and_low_stock(logged_client, app):
    response = logged_client.post("/products/new", data={
        "name": "Óleo de cozinha 900 ml", "code": "OLE004",
        "price": "7,50", "quantity": "3", "minimum_stock": "5"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Estoque baixo" in response.get_data(as_text=True)
    with app.app_context():
        product = Product.query.filter_by(code="OLE004").first()
        assert product.quantity == 3
        assert product.low_stock is True

def test_entry_updates_balance_and_records_movement(logged_client, app):
    logged_client.post("/products/new", data={
        "name": "Café Tradicional 500 g", "code": "CAF001",
        "price": "18,90", "quantity": "4", "minimum_stock": "5"
    })
    response = logged_client.post("/movements/new", data={
        "product_id": "1", "movement_type": "entrada", "quantity": "3"
    }, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        product = Product.query.filter_by(code="CAF001").first()
        assert product.quantity == 7
        assert StockMovement.query.filter_by(product_id=product.id).count() == 1

def test_exit_cannot_make_stock_negative(logged_client, app):
    logged_client.post("/products/new", data={
        "name": "Arroz", "code": "ARR001", "price": "20,00",
        "quantity": "2", "minimum_stock": "1"
    })
    response = logged_client.post("/movements/new", data={
        "product_id": "1", "movement_type": "saida", "quantity": "3"
    }, follow_redirects=True)
    assert "Estoque insuficiente" in response.get_data(as_text=True)
    with app.app_context():
        assert Product.query.filter_by(code="ARR001").first().quantity == 2
