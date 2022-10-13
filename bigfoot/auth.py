import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from bigfoot.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Register view - associates the URL /register with the register view function
@bp.route('/register', methods=('GET', 'POST'))
def register():
    # request.form is a special type of dict mapping submitted form keys and values
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:  # Validate that username is not empty
            error = 'Username is required.'
        elif not password:  # Validate that password is not empty
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),  # SHA256 hash with salt 8 by default :)
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

# Login View - associates the URL /login with the login view function
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # session is a dict that stores data across requests
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

# load_logged_in_user() registers a function that runs before the view function, regardless of what URL is requested
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        # gets the user’s data from the database, storing it on g.user
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

# To logout remove the user id from the session
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Require Authentication in Other Views
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))  # generate the URL to a view based on a name and arguments

        return view(**kwargs)

    return wrapped_view