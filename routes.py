import datetime
from string import ascii_letters, digits, printable
from flask import render_template, redirect, request
from app import app
import users
import books
import bookloans


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
            return render_template("message.html", message="Väärä käyttäjätunnus tai salasana!")

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
        for i in username:
            if i not in ascii_letters+digits+"åöäÅÖÄ":
                return render_template("message.html", message="""Käyttäjänimi voi sisältää vain 
                                    kirjaimia ja numeroita.""")

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("message.html", message="Salasanat eroavat.")

        for i in password1:
            if i not in ascii_letters+digits+"!?-_,.:;=+åöäÅÖÄ":
                return render_template("message.html", message="""Salasana voi sisältää vain
                                    kirjaimia, numeroita ja seuraavia merkkejä: !?-_,.:;=+""")

        role = request.form["role"]
        if role not in ("0", "1"):
            return render_template("message.html", message="Tuntematon käyttäjärooli.")

        if users.register(username, password1, role):
            return redirect("/")
            
    return render_template("message.html", message="Rekisteröinti epäonnistui.")


@app.route("/book/<int:book_id>")
def show_book(book_id):

    details = books.get_book_details(int(book_id))
    visible = details[5]

    if visible:

        loan_info = bookloans.get_loans_info(int(book_id))

        borrowable = loan_info is None

        reviews = books.get_reviews(int(book_id))

        return render_template("book.html", id=details[0], name=details[1],
                            author=details[2], year=details[3], genre=details[4],
                            loan_info=loan_info, borrowable=borrowable, reviews=reviews)

    return render_template("message.html", 
                        message="Tämä kirja on poistettu valikoimasta!")

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

        for i in name + author + genre:
            if i not in printable+"ÅÄÖåäö":
                return render_template("message.html", message="""Syötteet voivat sisältää vain kirjaimia, 
                                    numeroita ja seuraavia merkkejä: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~""")

        if books.add_book(name, author, int(year), genre):
            return redirect("/")

    return render_template("message.html", message="Jokin meni pieleen. Yritä uudelleen.")


@app.route("/remove", methods=["POST"])
def remove_book():
    users.require_role(1)
    users.check_csrf()
    book_id = request.form["book_id"]

    if books.remove_book(int(book_id)):
        return render_template("message.html", message="Kirjan poistaminen onnistui!")

    return render_template("message.html", message="Jokin meni pieleen. Yritä uudelleen.")

@app.route("/removed", methods=["GET", "POST"])
def removed_books():
    users.require_role(1)

    if request.method == "GET":
        return render_template("removed.html", removed_books=books.get_removed_books())

    if request.method == "POST":
        users.check_csrf()

        book_id = request.form["book_id"]

        if books.restore_book(book_id):
            return render_template("message.html", message="Kirjan palauttaminen onnistui!")
    
    return render_template("message.html", message="Jokin meni pieleen. Yritä uudelleen.")


@app.route("/bookwish", methods=["GET", "POST"])
def wish_for_book():
    users.require_role(0)

    if request.method == "GET":
        return render_template("bookwish.html")

    if request.method == "POST":
        users.check_csrf()

        name = request.form["name"]
        author = request.form["author"]
        if name == "" or author == "":
            return render_template("message.html", message="Anna kirjan ja kirjailijan nimi.")

        for i in name + author:
            if i not in printable+"åöäÅÖÄ":
                return render_template("message.html", message="""Nimet voivat sisältää vain kirjaimia, 
                                    numeroita ja seuraavia merkkejä: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~""")

        if books.wish_for_book(users.get_current_user(), name, author):
            return render_template("message.html", message="Toiveen tallentaminen onnistui!")

    return render_template("message.html", message="Jokin meni pieleen. Yritä uudelleen.")


@app.route("/search", methods=["GET", "POST"])
def search_book():
    if request.method == "GET":
        return render_template("search.html")

    if request.method == "POST":

        search_type = request.form["search_type"]
        if search_type not in ["0", "1", "2", "3"]:
            return render_template("message.html", message="Tuntematon hakuperuste.")
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

    return render_template("message.html", message="Jokin meni pieleen. Yritä uudelleen.")


@app.route("/review", methods=["POST"])
def give_review():
    users.check_csrf()

    book_id = request.form["book_id"]

    score = int(request.form["score"])
    if score < 1 or score > 5:
        return render_template("message.html", message="Tuntematon pistemäärä. Valitse 1-5.")

    comment = request.form["comment"]
    if len(comment) < 1:
        return render_template("message.html", message="Anna kommentti.")
    if len(comment) > 1000:
        return render_template("message.html", message="Antamasi kommentti on liian pitkä.")

    for i in comment:
        if i not in printable+"ÅÄÖåäö":
                return render_template("message.html", message="""Kommentti voi sisältää vain kirjaimia, 
                                    numeroita ja seuraavia merkkejä: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~""")

    if books.add_review(int(book_id), users.get_current_user(), score, comment):
        return redirect(f"/book/{str(book_id)}")

    return render_template("message.html", message="Jokin meni pieleen. Yritä uudelleen.")


@app.route("/book-wishes")
def show_book_wishes():
    users.require_role(1)
    return render_template("book_wishes.html", wishes=books.get_wishes())


@app.route("/borrow", methods=["POST"])
def borrow_book():
    users.require_role(0)
    users.check_csrf()

    book_id = request.form["book_id"]
    date = datetime.date.today()

    if bookloans.borrow_book(int(book_id), users.get_current_user(), str(date)):
        return redirect(f"/book/{str(book_id)}")

    return render_template("message.html", message="Jokin meni pieleen. Yritä uudelleen.")


@app.route("/return", methods=["POST"])
def return_book():
    users.require_role(0)
    users.check_csrf()

    book_id = request.form["book_id"]

    if bookloans.return_book(int(book_id)):
        return redirect(f"/book/{str(book_id)}")

    return render_template("message.html", message="Jokin meni pieleen. Yritä uudelleen.")


@app.route("/loans")
def show_loans():
    users.require_role(1)
    return render_template("loans.html", loans=bookloans.get_all_loans())
