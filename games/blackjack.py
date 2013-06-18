""" Blackjack game. *Note: not quite a Vegas version of blackjack. 
Try it out. You have options to hit, stand, and deal to start a new game. 
This game implemented object-oriented programming. 
* (Ace means 1 not 11)
* Dependency: run this code on codeskulptor.org
By Yuttanant Suwansiri 13 Jun 2013
"""

# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score_str = ""
status = ""
score = 0
# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand_array = []	
        self.hand = ""  
    
    def __str__(self):
        s  = "Hand contains " + self.hand
        return s 

    def add_card(self, card):
        # add a card object to a hand
        self.hand = ""
        self.hand_array.append(card) 
        for i in range(len(self.hand_array)):
            self.hand += str(self.hand_array[i])
            self.hand += " "
            
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        j = 0
        hand_value = 0
        value = []
        for i in range(len(self.hand)):
            if (self.hand[i].isdigit() or self.hand[i] == 'A' or self.hand[i] == 'T' or self.hand[i] == 'J' or self.hand[i] == 'Q' or self.hand[i] == 'K'):
                #print self.hand[i]
                converted = VALUES.get(self.hand[i])
                value.append(converted)  
        for i in range(len(value)):
            hand_value += value[i]
        return hand_value
    
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for i in range(len(self.hand)):
            if i == 0:
                card = Card(self.hand[i], self.hand[i+1])
                card.draw(canvas, [100 / 2, pos])
            if i % 3 == 0 and i > 0:
                card = Card(self.hand[i], self.hand[i+1])
                card.draw(canvas, [50 + 100 * (i / 3), pos])
                
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck_array = range(len(RANKS) * len(SUITS))
        self.deck = "" 
        
        k = 0
        for i in range(len(SUITS)):
            for j in range(len(RANKS)):
                self.deck_array[k] = SUITS[i] + RANKS[j]  
                k += 1

    def shuffle(self):
        # add cards back to deck and shuffle
        # use random.shuffle() to shuffle the deck
        random.shuffle(self.deck_array)

    def deal_card(self):
        # deal a card object from the deck
        deal = self.deck_array.pop(len(self.deck_array) - 1)
        deal = Card(deal[0], deal[1])
        return deal
    
    def __str__(self):
        # return a string representing the deck
        self.deck = ""
        for i in range(len(self.deck_array)):
            self.deck += str(self.deck_array[i])
            self.deck += " "
        s = "Deck contains " + self.deck
        return s

#define event handlers for buttons
def deal():
    global outcome, in_play
    global deck, player_hand, dealer_hand, status
    
    if in_play == False: 
        outcome = ""
        # shuffle the cards from the deck
        deck = Deck()
        deal = deck.shuffle()
        
        # add cards to players and dealer hands
        player_hand = Hand()
        dealer_hand = Hand()
        
        player_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())
        # print "Player ", player_hand
        
        dealer_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        # print "Dealer ", dealer_hand
        
        status = "Hit or Stand?"
    
    in_play = True
        
def hit():
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
    global in_play, outcome, score_str, score
    
    if in_play == True:
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            print "You have busted"
            outcome = "You have busted"
            in_play = False
            score -= 1
            score_str = "Score " + str(score)
            status = "New Deal?"
            print "Player Value ", player_hand.get_value()
            print "Dealer Value ", dealer_hand.get_value()
    
def stand():
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    global in_play, score, outcome, score_str, status
    if in_play == True:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
            
        if dealer_hand.get_value() >= player_hand.get_value():
            if dealer_hand.get_value() > 21:
                print "Dealer have busted"
                print "Player have won"
                outcome = "Dealer have busted"
                score += 1
            else:
                print "Dealer have won"
                outcome = "Dealer wins"
                score -= 1
        else: 
            print "Player have won"
            outcome = "You win"
            score += 1 
    score_str = "Score " + str(score)
    in_play = False
    status = "New Deal?"
    print "Player Value ", player_hand.get_value()
    print "Dealer Value ", dealer_hand.get_value()
    
# draw handler    
def draw(canvas):
    # draw player and dealer hands
    player_hand.draw(canvas, 400)
    dealer_hand.draw(canvas, 200)
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [86, 250], CARD_BACK_SIZE)
    # draw texts
    canvas.draw_text("Blackjack", (50, 100), 48, "Blue")
    canvas.draw_text(score_str, (350, 100), 24, "Black")
    canvas.draw_text("Dealer", (50, 175), 24, "Black")
    canvas.draw_text(outcome, (250, 175), 24, "Black")
    canvas.draw_text("Player", (50, 375), 24, "Black")
    canvas.draw_text(status, (250, 375), 24, "Black")

# initialization frame

frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)

frame.set_draw_handler(draw)

# initialize objects
player_hand = Hand()
dealer_hand = Hand()

# get things rolling
frame.start()
deal()