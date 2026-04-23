from flask import Flask, render_template, request, redirect, session, url_for, flash
from data_manage import DataManager
from models import *
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:dlyaraboty_Python2026@localhost:5432/postgres"

db.init_app(app)

with app.app_context():
    db.create_all()

app.secret_key = 'flashkey'
data_manager = DataManager()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def login():
    username = request.form.get('username').strip().lower()
    password = request.form.get('password').strip()

    try:
        user = data_manager.user_authorisation(name=username, password=password)
        session['user_id'] = user.user_id
        session['username'] = user.name

        flash(f"Welcome back, {user.name}!")
        return redirect(url_for('user_page', username=user.name))

    except ValueError as e:
        flash(str(e))
        return redirect(url_for('index'))

@app.route('/user/<username>')
def user_page(username):
    return render_template('user_page.html', username=username)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username').strip().lower()
        password = request.form.get('password').strip()

        if not username or not password:
            flash("Please fill in all fields")
            return redirect(url_for('register'))

        try:
            data_manager.add_user(name=username, password=password)
            flash(f"User '{username}' was created successfully")
            return redirect(url_for('index'))

        except ValueError as e:
            flash(str(e))

        except SQLAlchemyError as e:
            flash(f"Database error: {str(e)}")

        except Exception:
            flash("Some error occurred. Please try again.")

        return render_template('register.html')

    if request.method == 'GET':
        return render_template('register.html')


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