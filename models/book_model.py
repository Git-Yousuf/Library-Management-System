from flask_mysqldb import MySQL

class BookModel:
    def __init__(self, mysql):
        self.mysql = mysql

    def get_all_books(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM books")
        books = cur.fetchall()
        cur.close()
        return books

    def add_book(self, title, author, year):
        cur = self.mysql.connection.cursor()
        cur.execute("INSERT INTO books (title, author, year) VALUES (%s, %s, %s)", (title, author, year))
        self.mysql.connection.commit()
        cur.close()

    def search_books(self, query):
        cur = self.mysql.connection.cursor()
        query = f"%{query}%"  # For partial matching
        cur.execute("SELECT * FROM books WHERE title LIKE %s OR author LIKE %s OR year LIKE %s", (query, query, query))
        books = cur.fetchall()
        cur.close()
        return books

    def borrow_book(self, book_id, borrower_name, borrow_date, borrower_phone , borrower_address):
        cur = self.mysql.connection.cursor()
        cur.execute("INSERT INTO borrowers (book_id, borrower_name, borrow_date, borrower_phone, borrower_address) VALUES (%s, %s, %s, %s, %s)",
                    (book_id, borrower_name, borrow_date, borrower_phone, borrower_address))
        cur.execute("UPDATE books SET borrowed = TRUE WHERE id = %s", [book_id])
        self.mysql.connection.commit()
        cur.close()

    def return_book(self, book_id, return_date):
        cur = self.mysql.connection.cursor()
        cur.execute("UPDATE borrowers SET return_date = %s WHERE book_id = %s AND return_date IS NULL",
                    (return_date, book_id))
        cur.execute("UPDATE books SET borrowed = FALSE WHERE id = %s", [book_id])
        self.mysql.connection.commit()
        cur.close()

    def get_borrowed_books(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT b.id, b.title, b.author, br.borrower_name, br.borrow_date, br.borrower_phone, br.borrower_address FROM books b "
                    "JOIN borrowers br ON b.id = br.book_id WHERE b.borrowed = TRUE AND br.return_date IS NULL")
        borrowed_books = cur.fetchall()
        cur.close()
        return borrowed_books
    
    def get_all_borrowed_books(self):
        cur = self.mysql.connection.cursor()
        cur.execute("""
            SELECT b.id, b.title, b.author, br.borrower_name, br.borrow_date, br.return_date, br.borrower_phone, br.borrower_address 
            FROM books b 
            JOIN borrowers br ON b.id = br.book_id
        """)
        all_borrowed_books = cur.fetchall()
        cur.close()
        return all_borrowed_books