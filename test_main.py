import pytest
from main import app, db, Book

@pytest.fixture(scope='function')
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.session.remove()
            db.drop_all()

def test_main_route(test_client):
    rv = test_client.get('/')
    assert rv.status_code == 200
    assert rv.data == "😼".encode('utf-8')

def test_get_books(test_client):
    rv = test_client.get('/book')
    assert rv.status_code == 200
    assert rv.get_json() == []

def test_create_book(test_client):
    book_data = {
        "isbn": "12345",
        "author": "Author",
        "title": "Title",
        "genre": "Genre",
        "price": 9.99,
        "quantity": 5
    }
    rv = test_client.post('/book', json=book_data)
    assert rv.status_code == 201
    json_data = rv.get_json()
    assert json_data["isbn"] == book_data["isbn"]
    assert json_data["author"] == book_data["author"]
    assert json_data["title"] == book_data["title"]
    assert json_data["genre"] == book_data["genre"]
    assert json_data["price"] == book_data["price"]
    assert json_data["quantity"] == book_data["quantity"]

def test_get_book_by_id(test_client):
    book_data = {
        "isbn": "12345",
        "author": "Author",
        "title": "Title",
        "genre": "Genre",
        "price": 9.99,
        "quantity": 5
    }
    rv = test_client.post('/book', json=book_data)
    book_id = rv.get_json()["id"]
    rv = test_client.get(f'/book/{book_id}')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data["id"] == book_id
    assert json_data["isbn"] == book_data["isbn"]
    assert json_data["author"] == book_data["author"]
    assert json_data["title"] == book_data["title"]
    assert json_data["genre"] == book_data["genre"]
    assert json_data["price"] == book_data["price"]
    assert json_data["quantity"] == book_data["quantity"]

def test_update_book(test_client):
    book_data = {
        "isbn": "12345",
        "author": "Author",
        "title": "Title",
        "genre": "Genre",
        "price": 9.99,
        "quantity": 5
    }
    rv = test_client.post('/book', json=book_data)
    book_id = rv.get_json()["id"]
    updated_data = {
        "isbn": "67890",
        "author": "New Author",
        "title": "New Title",
        "genre": "New Genre",
        "price": 19.99,
        "quantity": 10
    }
    rv = test_client.put(f'/book/{book_id}', json=updated_data)
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data["isbn"] == updated_data["isbn"]
    assert json_data["author"] == updated_data["author"]
    assert json_data["title"] == updated_data["title"]
    assert json_data["genre"] == updated_data["genre"]
    assert json_data["price"] == updated_data["price"]
    assert json_data["quantity"] == updated_data["quantity"]

def test_delete_book(test_client):
    book_data = {
        "isbn": "12345",
        "author": "Author",
        "title": "Title",
        "genre": "Genre",
        "price": 9.99,
        "quantity": 5
    }
    rv = test_client.post('/book', json=book_data)
    book_id = rv.get_json()["id"]
    rv = test_client.delete(f'/book/{book_id}')
    assert rv.status_code == 204
    rv = test_client.get(f'/book/{book_id}')
    assert rv.status_code == 404
