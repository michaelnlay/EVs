from flask_app.models.car import Car
from flask_app.models.user import User
from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("index.html")

# =============================================
# Register Route
# =============================================


@app.route("/register", methods=["POST"])
def register_user():
    # 1 -- validate form info
    if not User.validate_register(request.form):
        return redirect("/")

    # 2 aside, convert password by bcrypt
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    # 2 - collect data from form
    query_data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash,

    }

    # 3 - run query to database (INSERT) or you can say call on query from our model file
    new_user_id = User.create_user(query_data)

    # 3A - add user id to session
    session["user_id"] = new_user_id

    # 4 - redirect elsewhere
    return redirect("/dashboard")

# =============================================
# Login Route
# =============================================


@app.route("/login", methods=["POST"])
def login():

    # 1 -- validate form info
    if not User.validate_login(request.form):
        return redirect("/")

    # 2 - query based on data
    query_data = {
        "email": request.form["email"]
    }
    logged_in_user = User.get_by_email(query_data)

    # 3 - put user_id into session
    session["user_id"] = logged_in_user.id

    # 4 - redirect elsewhere
    return redirect("/dashboard")

# =============================================
# Dashboard
# =============================================


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please login or register before entering site!")
        return redirect("/")

    data = {
        "user_id": session["user_id"]
    }
    user = User.get_by_id(data)
    all_cars = Car.get_all()

    return render_template("dashboard.html", user=user, all_cars=all_cars)

# =============================================
# Logout
# =============================================


@app.route("/logout")
def logout():
    session.clear()
    flash("Successfully logged out!")
    return redirect("/")
