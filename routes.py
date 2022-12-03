from app import app
from flask import render_template, redirect, request
import datetime
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
        
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", error="Salasanat eroavat")
        
        role = request.form["role"]
        if role not in ("0", "1"):
            return render_template("error.html", error="Tuntematon käyttäjärooli")

        if users.register(username, password1, role):
            return redirect("/")
        else:
            return render_template("error.html", error="Rekisteröinti epäonnistui")


@app.route("/book/<int:book_id>")
def show_book(book_id):
    details = books.get_book_details(int(book_id))

    loan_info = books.get_loans_info(int(book_id))

    if loan_info is None:
        borrowable = True
    else:
        borrowable = False

    reviews = books.get_reviews(int(book_id))

    return render_template("book.html", id=details[0], name=details[1], 
    author=details[2], year=details[3], genre=details[4], loan_info=loan_info,
    borrowable=borrowable, reviews=reviews)

@app.route("/add", methods=["GET", "POST"])
def add_book():
    users.require_role(1)

    if request.method == "GET":
        return render_template("add.html")

    if request.method == "POST":
        users.check_csrf()

        name = request.form["name"]
        author = request.form["author"]
        year = request.form["year"]
        genre = request.form["genre"]

        if books.add_book(name, author, int(year), genre):
            return redirect("/")
        else:
            return render_template("error.html", error="Jokin meni pieleen")

@app.route("/remove", methods=["POST"])
def remove_book():
    users.require_role(1)
    users.check_csrf()
    book_id = request.form["book_id"]

    if books.remove_book(int(book_id)):
        return "<p>Kirjan poistaminen onnistui. </p><a href='/'>Palaa etusivulle</a>"
    else:
        return render_template("error.html", error="Jokin meni pieleen. Yritä uudelleen.")

@app.route("/bookwish", methods=["GET", "POST"])
def wish_for_book():
    users.require_role(0)

    if request.method == "GET":
        return render_template("bookwish.html")

    if request.method == "POST":
        users.check_csrf()

        name = request.form["name"]
        if name == "":
            return render_template("error.html", error="Nimi on tyhjä")
        author = request.form["author"]
        if author == "":
            return render_template("error.html", error="Nimi on tyhjä")

        if books.wish_for_book(users.get_current_user(), name, author):
            return "<p>Toive tallennettu! </p><a href='/'>Palaa etusivulle</a>"
        else:
            return render_template("error.html", error="Jokin meni pieleen")

@app.route("/search", methods=["GET", "POST"])
def search_book():
    # needs to be updated so that the letter case doesn't matter
    if request.method == "GET":
            return render_template("search.html")

    if request.method == "POST":

        search_type = request.form["search_type"]
        if search_type == "0":
            query = request.form["query"]
            results = books.search_books_by_name(query)
            return render_template("result.html", results=results)
        if search_type == "1":
            query = request.form["query"]
            results = books.search_books_by_author(query)
            return render_template("result.html", results=results)
        if search_type == "2":
            query = request.form["query"]
            results = books.search_books_by_year(query)
            return render_template("result.html", results=results)
        if search_type == "3":
            query = request.form["query"]
            results = books.search_books_by_genre(query)
            return render_template("result.html", results=results)

        return render_template("error.html", error="Jokin meni pieleen. Yritä uudelleen.")

@app.route("/review", methods=["POST"])
def give_review():
    users.check_csrf()

    book_id = request.form["book_id"]

    score = int(request.form["score"])
    if score < 1 or score > 5:
        return render_template("error.html", error="Tuntematon pistemäärä. Valitse 1-5.")

    comment = request.form["comment"]
    if len(comment) < 1:
        return render_template("error.html", error="Anna kommentti")
    if len(comment) > 1000:
        return render_template("error.html", error="Antamasi kommentti on liian pitkä.")

    if books.add_review(int(book_id), users.get_current_user(), score, comment):
        return redirect(f"/book/{str(book_id)}")
    else:
        return render_template("error.html", error="Jokin meni pieleen. Yritä uudelleen.")

@app.route("/book-wishes")
def show_book_wishes():
    users.require_role(1)
    return render_template("book_wishes.html", wishes = books.get_wishes())
