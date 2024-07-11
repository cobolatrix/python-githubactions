from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:seguro1234@localhost/books"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Models

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'
    
with app.app_context():
    db.create_all()

# Routes

@app.route('/', methods=['GET'])
def main():
    return "😼", 200

@app.route('/book', methods=['GET'])
def get_books():
    books = Book.query.all()
    book_list = []
    for book in books:
        book_data = {
            "id": book.id,
            "isbn": book.isbn,
            "author": book.author,
            "title": book.title,
            "genre": book.genre,
            "price": book.price,
            "quantity": book.quantity
        }
        book_list.append(book_data)
    return jsonify(book_list), 200

@app.route('/book/<int:id>', methods=['GET'])
def get_book_by_id(id):
    book = db.session.get(Book, id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    book_data = {
        "id": book.id,
        "isbn": book.isbn,
        "author": book.author,
        "title": book.title,
        "genre": book.genre,
        "price": book.price,
        "quantity": book.quantity
    }
    return jsonify(book_data), 200

@app.route('/book', methods=['POST'])
def create_book():
    data = request.get_json()
    if 'isbn' not in data or 'author' not in data or 'title' not in data or 'genre' not in data or 'price' not in data or 'quantity' not in data:
        return jsonify({"error": "Missing information"}), 400
    new_book = Book(
        isbn=data['isbn'],
        author=data['author'],
        title=data['title'],
        genre=data['genre'],
        price=data['price'],
        quantity=data['quantity']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({
        "id": new_book.id,
        "isbn": new_book.isbn,
        "author": new_book.author,
        "title": new_book.title,
        "genre": new_book.genre,
        "price": new_book.price,
        "quantity": new_book.quantity
    }), 201

@app.route('/book/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()
    book = db.session.get(Book, id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    if 'isbn' in data:
        book.isbn = data['isbn']
    if 'author' in data:
        book.author = data['author']
    if 'title' in data:
        book.title = data['title']
    if 'genre' in data:
        book.genre = data['genre']
    if 'price' in data:
        book.price = data['price']
    if 'quantity' in data:
        book.quantity = data['quantity']
    db.session.commit()
    return jsonify({
        "id": book.id,
        "isbn": book.isbn,
        "author": book.author,
        "title": book.title,
        "genre": book.genre,
        "price": book.price,
        "quantity": book.quantity
    }), 200

@app.route('/book/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = db.session.get(Book, id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    db.session.delete(book)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run()
