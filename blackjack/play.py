from flask import (
    Blueprint, flash, g, redirect, render_template, request,
    url_for, session
)
from werkzeug.exceptions import abort

from blackjack.auth import login_required
from blackjack.db import get_db
from blackjack.blackjack import *

bp = Blueprint('play', __name__, url_prefix='/play')

@bp.route('/begin', methods=('GET', 'POST'))
@login_required
def begin():

	if request.method == 'POST':		# if form of method POST was submitted:
	 	if "newGame" in request.form:		  # if player clicked on this button:
	 		return redirect(url_for('play.game'))	# execute the route
	 	elif "statistics" in request.form:		  # if player clicked on this button:
	 		return redirect(url_for('welcome.statistics'))	# execute the route

	return render_template('play/begin.html')

@bp.route('/game', methods=('GET', 'POST'))
@login_required
def game():

	game = Game()				  # create a new game

	if 'gameDeck' in session:     # if a game is already in progress
		game.restoreGame(session) # restore the state of the game
		game.clearHands()		  # clear the player/dealer hands

	if request.method == 'GET':			  # if user arrived directly via game route 
		if len(game.deck.deck) < 10:	  # if there aren't at least 10 cards in deck,
			flash('Playing with a new deck...')  # flash a 'new deck' message
			game = Game()				  # then instantiate a new Game (w. new deck)

		game.beginDeal()				  # deal 2 cards to player and dealer
		game.storeToSession(session)	  # store the game state to session

		# if either player has a blackjack:
		if game.playerHand.isBlackjack() or game.dealerHand.isBlackjack():
			game.findWinner(session)	  # evaluate game result
			game.storeToSession(session)  # store the game state to session
			return redirect(url_for('play.result'))	# execute the result route
					# in this case, the player won't see game page

	elif request.method == 'POST':		# if user clicked Hit/Stand button

		game.restoreGame(session)		  # restore the state of the game

		if "hit" in request.form:		  # if player clicked on "Hit":
			game.hitPlayer()			  # deal 1 card to player
			game.storeToSession(session)  # store the game state to session
		
			if game.playerHand.isBust():	# if playerHand is over 21:
				game.findWinner(session)	# evaluate game result
				game.storeToSession(session)  # store the game state to session
				return redirect(url_for('play.result'))	# execute the result route

		elif "stand" in request.form:		# if player clicked on "Stand"

			game.dealerTurn()				# run dealer strategy
			game.findWinner(session)		# evaluate game result
			game.storeToSession(session)    # store the game state to session
			
			return redirect(url_for('play.result'))	# execute the result route

	return render_template('play/game.html',	# render the game template
		playerHand = session['playerHand'], dealerPartialHand = session['dealerHand'][1:],
		playerHandValue = session['playerHandValue'], dealerHandValue = session['dealerHandValue'],
		gameDeck = session['gameDeck'], deckSize = session['deckSize'],
		userChoice = ['hit','stand']
	)


@bp.route('/result', methods=('GET', 'POST'))	# user arrives here after game is completed
@login_required
def result():
    
	if request.method == 'POST':		# if form of method POST was submitted:
	 	if "playAgain" in request.form:		  # if player clicked on this button:
	 		return redirect(url_for('play.game'))	# execute the route
	 	elif "statistics" in request.form:		  # if player clicked on this button:
	 		return redirect(url_for('welcome.statistics'))	# execute the route
	 	elif "logout" in request.form:		  # if player clicked on this button:
	 		return redirect(url_for('auth.logout'))	# execute the route

	return render_template('play/results.html',	# render the result template
		playerHand = session['playerHand'], dealerHand = session['dealerHand'],
		playerHandValue = session['playerHandValue'], dealerHandValue = session['dealerHandValue'],
		gameDeck = session['gameDeck'], deckSize = session['deckSize'],
		gameResult = session['gameResult']
	)