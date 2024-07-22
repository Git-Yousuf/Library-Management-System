from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from config import Config
from models.book_model import BookModel
import datetime

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)
book_model = BookModel(mysql)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books')
def books():
    books = book_model.get_all_books()
    return render_template('books.html', books=books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        book_model.add_book(title, author, year)
        return redirect(url_for('books'))
    return render_template('add_book.html')

@app.route('/search_books', methods=['GET'])
def search_books():
    query = request.args.get('query')
    books = book_model.search_books(query)
    return render_template('books.html', books=books)

@app.route('/borrow_book', methods=['GET', 'POST'])
def borrow_book():
    if request.method == 'POST':
        book_id = request.form['book_id']
        borrower_name = request.form['borrower_name']
        borrow_date = datetime.date.today()
        book_model.borrow_book(book_id, borrower_name, borrow_date)
        return redirect(url_for('borrowed_books'))
    books = book_model.get_all_books()
    return render_template('borrow_book.html', books=books)

@app.route('/return_book', methods=['GET', 'POST'])
def return_book():
    if request.method == 'POST':
        book_id = request.form['book_id']
        return_date = datetime.date.today()
        book_model.return_book(book_id, return_date)
        return redirect(url_for('borrowed_books'))
    borrowed_books = book_model.get_borrowed_books()
    return render_template('return_book.html', borrowed_books=borrowed_books)

@app.route('/borrowed_books')
def borrowed_books():
    borrowed_books = book_model.get_borrowed_books()
    return render_template('borrowed_books.html', borrowed_books=borrowed_books)

if __name__ == '__main__':
    app.run(debug=True)
