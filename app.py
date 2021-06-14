import os
from flask import (Flask, render_template,
    redirect, request, session, url_for, flash)
from flask_pymongo import PyMongo
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


# App route for login

# App route for logout

# app route for register

# app route for library

# app route for home page(index)

# App route for character page

# app route for about page


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)