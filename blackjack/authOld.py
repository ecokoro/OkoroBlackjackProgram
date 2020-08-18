import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date

from blackjack.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        dbcur = db.cursor()
        dbcur.execute('SELECT user_id FROM users WHERE username = %s', (username,)
        )
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif dbcur.fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            dbcur.execute(
                'INSERT INTO users (username, password) VALUES (%s, %s)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        db.close()
        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        dbcur = db.cursor()
        error = None
        dbcur.execute(
            'SELECT * FROM users WHERE username = %s', (username,)
        )
        user = dbcur.fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[2], password):
            error = 'Incorrect password.'

        if error is None:
            

            session.clear()
            session['user_id'] = user[0]
            # session['date'] = date.today()
            session['wins'] = 0
            session['losses'] = 0
            session['ties'] = 0

            dbcur.execute(
                'SELECT MAX(session_id) FROM stats WHERE user_id=%s',(session['user_id'],))
            max = dbcur.fetchone()
            if max[0] is None:
                session['session_id'] = 1
            else:   
                session['session_id'] = max[0] + 1

            return redirect(url_for('play.begin'))

        db.close()
        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    db = get_db()
    dbcur = db.cursor()

    if user_id is None:
        g.user = None
    else:
        dbcur.execute(
            'SELECT * FROM users WHERE user_id = %s', (user_id,)
        )
        g.user = dbcur.fetchone()

@bp.route('/logout')
def logout():
    'Send the session stats to the database.'

    session['totalRounds'] = session['wins'] + session['losses'] + session['ties']
    dateToday = str(date.today())

    db = get_db()
    dbcur = db.cursor()
    dbcur.execute(
        'INSERT INTO stats (session_id, user_id, date, wins, losses, ties, totalRounds) VALUES(%s,%s,%s,%s,%s,%s,%s)',(session['session_id'],session['user_id'],dateToday, session['wins'], session['losses'], session['ties'],session['totalRounds'],)
    )
    db.commit()
    db.close()
    session.clear()
    
    flash('Thanks for playing! Your session stats were saved.')  # flash a 'session stats saved' message
    
    return redirect(url_for('welcome.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view