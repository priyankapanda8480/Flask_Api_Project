from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    published_date = db.Column(db.Date)
    isbn = db.Column(db.String(13), unique=True, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'published_date': self.published_date.isoformat() if self.published_date else None,
            'isbn': self.isbn
        }

# Create all database tables
with app.app_context():
    db.create_all()

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify(book.to_dict())

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    isbn = data.get('isbn')
    published_date_str = data.get('published_date')

    try:
        published_date = datetime.strptime(published_date_str, '%Y-%m-%d').date() if published_date_str else None
    except ValueError:
        return jsonify({'error': 'Invalid date format. Date should be in YYYY-MM-DD format.'}), 400

    book = Book(title=title, author=author, published_date=published_date, isbn=isbn)
    db.session.add(book)

    try:
        db.session.commit()
        return jsonify(book.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Book with this ISBN already exists'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()

    title = data.get('title', book.title)
    author = data.get('author', book.author)
    isbn = data.get('isbn', book.isbn)
    published_date_str = data.get('published_date', book.published_date)

    try:
        published_date = datetime.strptime(published_date_str, '%Y-%m-%d').date() if published_date_str else None
    except ValueError:
        return jsonify({'error': 'Invalid date format. Date should be in YYYY-MM-DD format.'}), 400

    book.title = title
    book.author = author
    book.isbn = isbn
    book.published_date = published_date

    try:
        db.session.commit()
        return jsonify(book.to_dict())
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Book with this ISBN already exists'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
