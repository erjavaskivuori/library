from app import app
from flask import render_template, redirect, request
import users, books

@app.route("/")
def index():
    return render_template("index.html", books=books.get_all_books())

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not users.login(username, password):
            return render_template("error.html", error="Väärä käyttäjätunnus tai salasana")

        return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 3 or len(username) > 20:
            return render_template("error.html", error="Käyttäjätunnuksen tulee olla 3-20 merkkiä")

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", error="Salasanat eroavat")
        if len(password1) < 3 or password1 == "":
            return render_template("error.html", error="Salasanan tulee sisältää 3-20 merkkiä")

        role = request.form["role"]
        if role not in ("0", "1"):
            return render_template("error.html", error="Tuntematon käyttäjärooli")

        if users.register(username, password1, role):
            return redirect("/")
        else:
            return render_template("error.html", error="Rekisteröinti epäonnistui")


@app.route("/book{<int:book_id>}")
def show_book(book_id):
    details = books.get_book_details(book_id)

    return render_template("book.html", id=book_id, name=details[1], 
    author=details[2], year=details[3], genre=details[4])

@app.route("/add", methods=["GET", "POST"])
def add_book():
    users.require_role(1)

    if request.method == "GET":
        return render_template("add.html")

    if request.method == "POST":
        users.check_csrf()

        name = request.form["name"]
        if name == "":
                return render_template("error.html", error="Nimi on tyhjä")

        author = request.form["author"]
        if author == "":
            return render_template("error.html", error="Nimi on tyhjä")

        year = request.form["year"]
        if year == "" or len(year) != 4:
            return render_template("error.html", error="Kirjoita julkaisuvuosi muodossa VVVV")

        genre = request.form["genre"]
        if genre == "":
            return render_template("error.html", error="Genre on tyhjä")

        book_id = books.add_book(name, author, year, genre)
        return redirect("/book/"+str(book_id))

#toimintoja lisätään