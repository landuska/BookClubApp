from flask import Flask, render_template, request, redirect,  url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from sqlalchemy.exc import SQLAlchemyError
from models import *
from data_manage import DataManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:dlyaraboty_Python2026@localhost:5432/postgres"

db.init_app(app)

with app.app_context():
    db.create_all()

app.secret_key = 'flashkey'
login_manager = LoginManager(app)
login_manager.login_view = 'login'
data_manager = DataManager()


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def login():
    username = request.form.get('username').strip().lower()
    password = request.form.get('password').strip()

    try:
        user = data_manager.user_authorisation(name=username, password=password)
        if user:
            login_user(user)
            flash(f"Welcome back, {user.name}!")
            return redirect(url_for('user_page', username=user.name))

    except ValueError as e:
        flash(str(e))
        return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user_page(username):
    return render_template('user_page.html', username=username)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username').strip().lower()
        password = request.form.get('password').strip()

        if not username or not password:
            flash("Please fill in all fields")
            return render_template('register.html')

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