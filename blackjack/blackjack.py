from random import shuffle

class Game:
    'represents an instance of a blackjack game'

    def __init__(self):
        'initialize new game with deck and hands'
        self.deck = Deck()
        self.playerHand = Hand()
        self.dealerHand = Hand()
        self.result = 'none'

    def beginDeal(self):
        'deal 2 cards to each player to begin game'
        self.playerHand.cards.append(self.deck.dealCard())
        self.dealerHand.cards.append(self.deck.dealCard())
        self.playerHand.cards.append(self.deck.dealCard())
        self.dealerHand.cards.append(self.deck.dealCard())

    def hitPlayer(self):
        'deal another card to player'
        self.playerHand.cards.append(self.deck.dealCard())

    def dealerTurn(self):
        'execute dealer turn, following defined strategy'
        while self.dealerHand.getValue() < 17:
            self.dealerHand.cards.append(self.deck.dealCard())

    def storeToSession(self,session):
        'store all the current values to session'
        session['gameDeck']=self.deck.deck
        session['deckSize']=len(self.deck.deck)
        session['playerHand']=self.playerHand.cards
        session['dealerHand']=self.dealerHand.cards
        session['playerHandValue']=self.playerHand.getValue()
        session['dealerHandValue']=self.dealerHand.getValue()

    def restoreGame(self,session):
        're-create game with deck, playerHand, dealerHand'
        self.deck.deck = session['gameDeck']
        self.playerHand.cards = session['playerHand']
        self.dealerHand.cards = session['dealerHand']

    def clearHands(self):
        'clear cards from player and dealer hands'
        self.playerHand.clear()
        self.dealerHand.clear()
        # clear result

    def findWinner(self,session):
        'determine game result, from player perspective'

        if self.playerHand.isBust():
            session['losses'] += 1
            session['gameResult'] = 'playerBust' #'You busted. Dealer wins!'
        elif self.dealerHand.isBust():
            session['wins'] += 1
            session['gameResult'] = 'dealerBust' #'Dealer busted. You win!'
        elif self.dealerHand.isBlackjack() and (self.playerHand.isBlackjack() == False):
            session['losses'] += 1
            session['gameResult'] = 'dealerBlackjack' #'The dealer got a blackjack...Dealer wins!' # house wins with a blackjack
        elif self.playerHand.isBlackjack() and (self.dealerHand.isBlackjack() == False):
            session['wins'] += 1
            session['gameResult'] = 'playerBlackjack' #'You got a blackjack...You win!'
        elif self.dealerHand.getValue() > self.playerHand.getValue():
            session['losses'] += 1
            session['gameResult'] = 'playerLoss' #'Sorry...you lost.'
        elif self.dealerHand.getValue() < self.playerHand.getValue():
            session['wins'] += 1
            session['gameResult'] = 'playerWin' #'Congrats...you win!'
        else:
            session['ties'] += 1
            session['gameResult'] = 'tie'

    def __repr__(self):
        'return canonical string representation of the game'
        deck = self.deck
        playerHand = self.playerHand
        dealerHand = self.dealerHand
        result = self.result

class Hand():
    'represent a dealer or player hand'

    def __init__(self):
        'initialize a hand object'
        self.cards = []

    def getValue(self):
        'calculate total value of hand'
        values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8,
                  '9':9, '10':10, 'J':10, 'Q':10, 'K':10, 'A':11}
        result = 0
        numAces = 0
    
        # add up the values of cards in hand, plus number of aces
        for card in self.cards:
            result += values[card[0]]          
            if card[0] == 'A':
                numAces += 1
        # while value of hand is > 21 and there is an ace
        # in the hand with value 11, convert its value to 1
        while result > 21 and numAces > 0:
            result -= 10
            numAces -= 1
        return result

    def isBust(self):
        'return true if a player\'s hand is bust (greater than 21).'
        return self.getValue() > 21

    def isBlackjack(self):
        'return true if a player\'s hand is 2 cards with a value of 21.'
        if (self.getValue() == 21) & (len(self) == 2):
            return True
        else:
            return False

    def clear(self):
        'clear cards from the player\'s hand'
        self.cards = []

    def __repr__(self):
        'return canonical string representation'
        return str(self.cards)

    def __len__(self):
        'return number of cards in the hand'
        return len(self.cards)



class Deck(list):
    'represents a standard deck of 52 playing cards.'

    suits = {'Hearts','Spades','Clubs','Diamonds'}
    ranks = {'2','3','4','5','6','7','8','9','10','J','Q','K','A'}

    def __init__(self):
        'initialize a standard 52-card deck'
        self.deck = []
        ''' Create the deck as an instance variable, assigning an empty
            list to it, since we'll be adding to it and every instance
            of Deck will be different.'''

        # iterate through every suit and rank
        for suit in Deck.suits: # looping through the class variable suits
            for rank in Deck.ranks:  # looping through the class variable ranks
                # create card with given rank,suit; add to deck
                self.deck.append((rank,suit))
                '''for each iteration, append a tuple of rank and suit'''
        self.shuffle()
    def dealCard(self):
        'deal the next card'
        return self.deck.pop()

    def isEmpty(self):
        'check if deck is empty'
        return self.deck == []

    def shuffle(self):
        'shuffle the deck'
        shuffle(self.deck)  # Notice that we've imported 'shuffle' from random up top

    def __eq__(self):
        'return True if exact same cards remain in same order'
        return self.deck == other.deck
    
    def __repr__(self):
        'return canonical string representation'
        return 'Remaining deck:'+str(self.deck)

    def __len__(self):
        'return number of cards in the deck'
        return len(self.deck)