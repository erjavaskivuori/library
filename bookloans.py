from db import db


def borrow_book(book_id, user_id, date):
    sql = """INSERT INTO loans (book_id, user_id, date)
            VALUES (:book_id, :user_id, :date)"""
    db.session.execute(
        sql, {"book_id": book_id, "user_id": user_id, "date": date})
    db.session.commit()
    return True


def return_book(book_id):
    sql = "DELETE FROM loans WHERE book_id=:book_id"
    db.session.execute(sql, {"book_id": book_id})
    db.session.commit()
    return True


def get_users_loans(user_id):
    sql = "SELECT * FROM loans WHERE user_id=:user_id"
    return db.session.execute(sql, {"user_id": user_id}).fetchall()


def get_loans_info(book_id):
    sql = "SELECT * FROM loans WHERE book_id=:book_id"
    return db.session.execute(sql, {"book_id": book_id}).fetchone()


def get_all_loans():
    sql = """SELECT username, name, author, date FROM users INNER JOIN loans ON users.id=user_id
            INNER JOIN books ON books.id=book_id"""
    return db.session.execute(sql).fetchall()