#Milestone Project 2
import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}
total = 100
playing = True

### CLASSES DEFINITIONS:  ###
class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return f'{self.rank} of {self.suit}'

class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):
        for x in self.deck:
            print(x)
        return 'Deck'

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop(0)

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        if(card.rank == 'Ace'):
            self.aces +=1
        self.value += values[card.rank]
        self.adjust_for_ace()
            
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
                self.aces -= 1
                self.value -= 10

class Chips:
    
    def __init__(self,total=100):
        self.total = total  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
        global total
        total = self.total

    
    def lose_bet(self):
        self.total -= self.bet
        global total
        total = self.total

### PLAYING FUNCTIONS : ###
def take_bet(chips):
    
    while True:
        try:
            chips.bet = int(input('Please set your bet : A number that is less or equal to your balance only!'))
            
        except:
            print('Error: Bad input.... , You can only insert integers')
        else:
        	if(chips.total == 0):
        		print('Ohh no... you aint got no money..... GET A JOB budy!!!')
        		exit(1)
        	if chips.bet > chips.total:
        		print('Sorry, you do not have enough chips, you have : {}'.format(chips.total))
        	else:
        		print(f'\nYou choose to bet on : {chips.bet}$ \n')
        		break
def hit(deck,hand):
    newcard = deck.deal()
    hand.add_card(newcard)

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    while True:
        x = input('Hit or Stand ? enter h or s :')
        if x[0].lower() == 'h':
            hit(deck,hand)
        elif x[0].lower()== 's':
        	print('\n')
        	print('Pleayer stands, Dealers turn :')
        	print('\n')
        	playing = False
        else:
            print('Sorry I did not understand that.... please enter h or s only !')
            continue
        break
def show_some(player,dealer):
    print('\nDEALERS Hand :')
    print('One Card Hidden....')
    print(dealer.cards[1])
    print('\n')
    print('PLAYER Hand :')
    for x in player.cards:
        print(x)
    print('\n')
    
def show_all(player,dealer):
    print('\nDEALERS Hand :')
    for x in dealer.cards:
        print(x)
    print('\n')
    print('PLAYER Hand :')
    for x in player.cards:
        print(x)
def player_busts(player,dealer,chips):
    print('\nPlayer BUSTS!\n')
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print('\nPlayer Wins!\n')
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print('\nPlayer Wins!, Dealer BUST\n')
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print('\nDealer wins!\n')
    chips.lose_bet()
    
def push(player,dealer):
    print('\nDealer and Player Tie - PUSH!\n')


########################################
#######         GAME ON !!!     ########
########################################

while True:
    # Print an opening statement
    print('\n############################################')
    print('######    WELCOME TO BLACKJACK !!!    ######')
    print('############################################\n')
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    
        
    # Set up the Player's chips
    #global total
    player_chips = Chips(total)
    
    # Prompt the Player for their bet
    take_bet(player_chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand)
        
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21 :
            player_busts(player_hand,dealer_hand,player_chips)

            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if dealer_hand.value <= 21:
            
        while dealer_hand.value < 17 :
        	hit(deck,dealer_hand)
    
        # Show all cards
        show_all(player_hand,dealer_hand)
        # Run different winning scenarios
        if dealer_hand.value > 21 :
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value == player_hand.value :
            push(player_hand,dealer_hand)
        elif dealer_hand.value > player_hand.value :
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value :
            player_wins(player_hand,dealer_hand,player_chips)
    
    # Inform Player of their chips total 
    print('\n Players total chips are : {}'.format(player_chips.total))
    # Ask to play again
    new_game = input('Would you like to play another game y/n ?')
    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print('Thank you for playing !')
        break


