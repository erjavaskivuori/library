import secrets
from db import db
from flask import session, abort, request
from werkzeug.security import check_password_hash, generate_password_hash

def register(username, password, role):
    hash_value = generate_password_hash(password)

    try:
        sql = """INSERT INTO users (username, password, role) 
                 VALUES (:username, :password, :role)"""
        db.session.execute(sql, {"username":username, "password":hash_value, "role":role})
        db.session.commit()
    except:
        return False
    return login(username, password)


def login(username, password):
    sql = "SELECT id, username, password, role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if user == "":
        return False
    if not check_password_hash(user[2], password):
        return False

    session["user_id"] = user[0]
    session["username"] = username
    session["user_role"] = user[3]
    session["csrf_token"] = secrets.token_hex(16)
    return True
    
def logout():
    del session["user_id"]
    del session["username"]
    del session["user_role"]

def require_role(role):
    if role > session.get("user_role", 0):
        abort(403)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)