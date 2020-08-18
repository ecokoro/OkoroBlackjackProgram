from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from blackjack.auth import login_required
from blackjack.db import get_db


bp = Blueprint('welcome', __name__, url_prefix='/')

@bp.route('/', methods=('GET', 'POST'))
@bp.route('/index', methods=('GET', 'POST'))

# no login required
def index():

	if request.method == 'POST':		# if form of method POST was submitted:
	 	if "existingUser" in request.form:		  # if player clicked on this button:
	 		return redirect(url_for('auth.login'))	# execute the route
	 	elif "newUser" in request.form:		  # if player clicked on this button:
	 		return redirect(url_for('auth.register'))	# execute the route

	return render_template('welcome.html')




@bp.route('/statistics', methods=('GET', 'POST'))
@login_required
def statistics():

	if request.method == 'POST':		# if form of method POST was submitted:
	 	if "play" in request.form:		  # if player clicked on this button:
	 		return redirect(url_for('play.game'))	# execute the route
	 	elif "logout" in request.form:		  # if player clicked on this button:
	 		return redirect(url_for('auth.logout'))	# execute the route

	db = get_db()
	dbcur = db.cursor()

	dbcur.execute(
		'CALL getuserstats(%s)',(session['user_id'],)
		)
	stats = dbcur.fetchall()
	return render_template('statistics.html', stats=stats, userChoice=['playAgain','logout'])
