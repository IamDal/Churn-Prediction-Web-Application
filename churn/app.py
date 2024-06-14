import TrainModel as TrainModel
import os
import config
from predict import Predict, predict_csv
from flask import Flask, flash, redirect, render_template, request, session, send_file
from flask_session import Session
from helpers import apology, login_required, create_customers, Createdb, User, check_form

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Set secret key
app.secret_key = config.SECRET_KEY

# Configure CS50 Library to use SQLite database
db = Createdb()
db.create_table()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        if session.get("user") is None:
            return render_template("landing.html")
        else:
            return render_template("index.html", username=session["user"])
    elif request.method == "POST":
        if 'file' not in request.files:
            if check_form(request.form) == 1:
                flash('Error. Please fill out entire form.', 'error')
            else:
                customer = create_customers(request.form)
                pred = Predict(customer)
                percentage = pred[0] * 100
                flash(f'Customer {customer.Surname} has a {percentage:.2f}% chance of churning!', 'success')
            return redirect("/")
        else:
            file = request.files['file']
            file.save(os.path.join(config.UPLOAD_PATH))
            return redirect("/download")
    else:
        return render_template("index.html")


@app.route('/download')
@login_required
def download_file():
    if not os.path.exists(config.UPLOAD_PATH):
        return 'No CSV file uploaded'
    if os.path.exists(config.RESULTS):
        os.remove(config.RESULTS)
    predict_csv(config.UPLOAD_PATH)
    # Get the file path
    file_path = os.path.join(config.RESULTS)
    # Check if the file exists
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        # Send the file to the client
        return send_file(file_path, as_attachment=True)
    else:
        return 'File not found or empty'


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        # Ensure username exists and password is correct
        user_check = db.lookup_user(request.form.get('username'), request.form.get("password"))
        if user_check == 1:
            return apology("invalid username and/or password", 403)
        # Remember which user has logged in
        session["user"] = user_check[0]["username"]
        # Redirect user to home page
        render_template("index.html", username=session["user"])
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # Ensure all required fields are submitted
        if not username or not password or not confirmation:
            return apology("All fields are required", 400)
        # Ensure the username hasn't already been taken
        if db.execute("SELECT username FROM users WHERE username = ?", username):
            return apology("Username already taken", 400)
        # Ensure the passwords match
        if password != confirmation:
            return apology("Passwords must match", 400)
        # Ensure password length is at least 8 characters
        if len(password) < 8:
            return apology("Password too short (min 8 characters)", 400)
        # Create a User object
        new_user = User(username=username, password=password)
        # Insert new user into the database
        db.insert_user(new_user)
        session["user"]=username
        return redirect("/")
    # For GET requests, render the registration form
    return render_template("register.html")


@app.route("/landing", methods=["GET", "POST"])
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


@app.route("/about", methods=["GET", "POST"])
def about():
    if request.method == "GET":
        return render_template("about.html", username=session["user"])
    else:
        return render_template("about.html")


if __name__ == '__main__':
    TrainModel.train()
