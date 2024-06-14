import os
import config
import pandas as pd
from flask import redirect, render_template, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from pydantic import BaseModel
from cs50 import SQL


class Createdb(SQL):
    def __init__(self):
        db_file = "database/database.db"
        if not os.path.exists(db_file):
            open(db_file, 'a').close()  # Create an empty file if it doesn't exist
        super().__init__("sqlite:///" + db_file)

    def create_table(self):
        customers_query = '''CREATE TABLE IF NOT EXISTS customers (
                        CustomerId INTEGER PRIMARY KEY NOT NULL,
                        Surname TEXT NOT NULL,
                        CreditScore INTEGER NOT NULL,
                        Geography TEXT NOT NULL,
                        Gender TEXT NOT NULL,
                        Age INTEGER NOT NULL,
                        Tenure INTEGER NOT NULL,
                        Balance REAL NOT NULL,
                        NumOfProducts INTEGER NOT NULL,
                        HasCrCard INTEGER NOT NULL,
                        IsActiveMember INTEGER NOT NULL,
                        EstimatedSalary REAL NOT NULL
                    )'''

        users_query = '''CREATE TABLE IF NOT EXISTS users (
                        username TEXT NOT NULL UNIQUE,
                        hash TEXT NOT NULL
                    )'''

        self.execute(users_query)
        self.execute(customers_query)

    def insert_user(self, new_user):
        add_user = "INSERT INTO users (username, hash) VALUES (?, ?)"
        self.execute(add_user, new_user.username, new_user.hashed_password)

    def lookup_user(self, username, password):
        lookup = "SELECT * FROM users WHERE username = ?"

        user_check = self.execute(lookup, username)
        if len(user_check) != 1 or not check_password_hash(user_check[0]["hash"], password):
            return 1
        else:
            return user_check


class ChurnCustomer(BaseModel):
    CustomerId: int
    Surname: str
    CreditScore: int
    Geography: str
    Gender: str
    Age: float
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.hashed_password = generate_password_hash(password)


class Customer:
    def __init__(self, CustomerData):
        self.CustomerId = CustomerData.CustomerId
        self.Surname = CustomerData.Surname
        self.CreditScore = CustomerData.CreditScore
        self.Geography = CustomerData.Geography
        self.Gender = CustomerData.Gender
        self.Age = CustomerData.Age
        self.Tenure = CustomerData.Tenure
        self.Balance = CustomerData.Balance
        self.NumOfProducts = CustomerData.NumOfProducts
        self.HasCrCard = CustomerData.HasCrCard
        self.IsActiveMember = CustomerData.IsActiveMember
        self.EstimatedSalary = CustomerData.EstimatedSalary

    def CustomerDataFrame(self):
        data = {
            'RowNumber': 0,
            'CustomerId': [self.CustomerId],
            'Surname': [self.Surname],
            'CreditScore': [self.CreditScore],
            'Geography': [self.Geography],
            'Gender': [self.Gender],
            'Age': [self.Age],
            'Tenure': [self.Tenure],
            'Balance': [self.Balance],
            'NumOfProducts': [self.NumOfProducts],
            'HasCrCard': [self.HasCrCard],
            'IsActiveMember': [self.IsActiveMember],
            'EstimatedSalary': [self.EstimatedSalary],
        }
        return pd.DataFrame.from_dict(data)


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def check_form(form):
    """Checks for missing form data."""
    for feature in config.FEATURES:
        if not form.get(feature):
            return 1


def create_customers(form):
    """Creates a new customer from form data."""
    customer = ChurnCustomer(
        CustomerId=form.get('CustomerId'),
        Surname=form.get('Surname'),
        CreditScore=form.get('CreditScore'),
        Geography=form.get('Geography'),
        Gender=form.get('Gender'),
        Age=form.get('Age'),
        Tenure=form.get('Tenure'),
        Balance=form.get('Balance'),
        NumOfProducts=form.get('NumOfProducts'),
        HasCrCard=form.get('HasCrCard'),
        IsActiveMember=form.get('IsActiveMember'),
        EstimatedSalary=form.get('EstimatedSalary')
    )
    return customer
