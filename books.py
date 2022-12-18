from db import db


def get_all_books():
    sql = """SELECT id, name, author, year, genre FROM books
             WHERE visible='True'"""
    return db.session.execute(sql).fetchall()


def get_book_details(book_id):
    sql = "SELECT * FROM books WHERE id=:id"
    return db.session.execute(sql, {"id": book_id}).fetchone()


def search_books_by_name(name):
    sql = """SELECT id, name, author, year, genre FROM books
             WHERE visible = 'True' AND name ILIKE :name"""
    return db.session.execute(sql, {"name": "%"+name+"%"}).fetchall()


def search_books_by_author(author):
    sql = """SELECT id, name, author, year, genre FROM books
             WHERE visible = 'True' AND author ILIKE :author"""
    return db.session.execute(sql, {"author": "%"+author+"%"}).fetchall()


def search_books_by_year(year):
    sql = """SELECT id, name, author, year, genre FROM books
             WHERE visible = 'True' AND year=:year"""
    return db.session.execute(sql, {"year": year}).fetchall()


def search_books_by_genre(genre):
    sql = """SELECT id, name, author, year, genre FROM books
             WHERE visible = 'True' AND genre ILIKE :genre"""
    return db.session.execute(sql, {"genre": "%"+genre+"%"}).fetchall()


def add_book(name, author, year, genre):

    try:
        sql = """INSERT INTO books (name, author, year, genre, visible)
                VALUES (:name, :author, :year, :genre, 'True')"""
        db.session.execute(sql, {"name": name, "author": author,
                                 "year": year, "genre": genre})
        db.session.commit()
    except:
        return False
    return True


def remove_book(book_id):
    sql = """UPDATE books SET visible='False' WHERE id=:id"""
    db.session.execute(sql, {"id": book_id})
    db.session.commit()

    return True

def get_removed_books():
    sql = """SELECT id, name, author, year, genre FROM books
             WHERE visible='False'"""
    return db.session.execute(sql).fetchall()

def restore_book(book_id):
    sql = """UPDATE books SET visible='True' WHERE id=:id"""
    db.session.execute(sql, {"id": book_id})
    db.session.commit()

    return True

def wish_for_book(user_id, name, author):
    sql = """INSERT INTO wishlist (user_id, name, author)
            VALUES (:user_id, :name, :author)"""
    db.session.execute(
        sql, {"user_id": user_id, "name": name, "author": author})
    db.session.commit()

    return True


def get_wishes():
    sql = """SELECT username, name, author FROM users INNER JOIN wishlist
            ON users.id=user_id"""
    return db.session.execute(sql).fetchall()


def add_review(book_id, user_id, score, comment):
    try:
        sql = """INSERT INTO reviews (book_id, user_id, score, comment)
                 VALUES (:book_id, :user_id, :score, :comment)"""
        db.session.execute(sql, {"book_id": book_id, "user_id": user_id,
                                 "score": score, "comment": comment})
        db.session.commit()
        return True
    except:
        return False


def get_reviews(book_id):
    sql = """SELECT username, score, comment FROM users INNER JOIN reviews
            ON users.id=user_id AND book_id=:book_id"""
    return db.session.execute(sql, {"book_id": book_id}).fetchall()
