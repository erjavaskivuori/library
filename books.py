from db import db

def get_all_books():
    sql = """SELECT id, name, author, year, genre FROM books
             WHERE visible = True"""
    return db.session.execute(sql).fetchall()

def get_book_details(book_id):
    sql = """SELECT id, name, author, year, genre FROM books 
             WHERE book_id=:book_id"""
    return db.session.execute(sql, {"book_id":book_id}).fetchone()

def order_books(order):
    sql = """SELECT id, name, author, year, genre FROM books 
             ORDER BY %s"""
    return db.session.execute(sql, {order}).fetchall()

def search_books_by_name(name):
    sql = """SELECT id, name, author, year, genre FROM books 
             WHERE visible = True AND name LIKE :name"""    
    return db.session.execute(sql, {"name":"%"+name+"%"}).fetchall()

def search_books_by_author(author):
    sql = """SELECT id, name, author, year, genre FROM books 
             WHERE visible = True AND author LIKE :author"""
    return db.session.execute(sql, {"author":"%"+author+"%"}).fetchall()

def search_books_by_year(year):
    sql = """SELECT id, name, author, year, genre FROM books 
             WHERE visible = True AND year=:year"""
    return db.session.execute(sql, {"year":year}).fetchall()

def search_books_by_genre(genre):
    sql = """SELECT id, name, author, year, genre FROM books 
             WHERE visible = True AND genre=:genre"""
    return db.session.execute(sql, {"genre":genre}).fetchall()

def add_book(name, author, year, genre):
    sql = """INSERT INTO books (name, author, year, genre, visible) 
            VALUES (:name, :author, :year, :genre, :visible)"""
    book = db.session.execute(sql, {"name":name, "author":author, +
            "year":year, "genre":genre, "visible":True}).fetchone()
    book_id = book[0]
    db.session.commit()

    return book_id

def remove_book(id):
    sql = """UPDATE books SET visible=FALSE WHERE id=:id"""
    db.session.execute(sql, {"id":id})
    db.session.commit()

    return True

