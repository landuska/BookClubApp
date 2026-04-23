from flask import Flask, render_template, request, redirect, Response, url_for, flash
from data_manage import DataManager
from models import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:dlyaraboty_Python2026@localhost:5432/postgres"

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def index()-> str:
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
    """Custom error handler for 404 (Page Not Found) errors."""
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(error):
    """Custom error handler for 500 (Internal Server Error) errors."""
    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)