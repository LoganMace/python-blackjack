import random

# Setting up the card properties.

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

# Created the classes for card, deck, hand, and chips.

class Card():

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return '{} of {}'.format(self.rank, self.suit)


class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
    
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n{}'.format(card.__str__())
        return 'The deck has: {}'.format(deck_comp)
            
    
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_ace(self):
        while self.aces and self.value > 21:
            self.value -= 10
            self.aces -+ 1


class Chips:

    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
    
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet


# Functionality for game actions.

def take_bet(chips):

    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet?'))
        except:
            print('Sorry, please provide an integer.')
        else:
            if chips.bet > chips.total:
                print('Not enough chips! Your total is: {}'.format(chips.total))
            else:
                break

                
def hit(deck,hand):
    
    new_card = deck.deal()
    hand.add_card(new_card)
    hand.adjust_for_ace()
    
    
def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    while True:
        x = input('Hit or stand? Enter h or s').lower()
        print(x)
        
        if x[0] == 'h':
            hit(deck, hand)
        elif x[0] == 's':
            print("Player stands, Dealer's turn")
            playing = False
        else:
            print('Sorry, I did not understand that. Please enter h or s only.')
            continue
        break
        
        
def show_some(player,dealer):
    
    print("Dealer's Hand:")
    print("One card hidden!")
    print(dealer.cards[1])
    print("Dealer's shown value is: {}".format(dealer.value))
    print("\n")
    print("Player's Hand:")
    for card in player.cards:
        print(card)
    print("Players's total value is: {}".format(player.value))
    
    
def show_all(player,dealer):
    
    print("Dealer's Hand:")
    for card in dealer.cards:
        print(card)
    print("Dealer's total value is: {}".format(dealer.value))
    print("\n")
    print("Player's Hand:")
    for card in player.cards:
        print(card)
    print("Players's shown value is: {}".format(player.value))
    
    
def player_busts(player, dealer, chips):
    print('Player Busts!')
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print('Player Wins!')
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print('Dealer Busts, Player Wins!')
    chips.win_bet()
    
def dealer_wins(player, dealer, chips):
    print('Dealer Wins!')
    chips.lose_bet()
    
def push(player, dealer):
    print('Dealer and Player draw! PUSH')



# RUN THE GAME BELOW

while True:
    # Print an opening statement
    print('WELCOME TO BLACKJACK')

    
    # Create & shuffle the deck, deal two cards to each player

    new_deck = Deck()
    new_deck.shuffle()
    
    # Player Hand
    
    player_hand = Hand()
    player_hand.add_card(new_deck.deal())
    player_hand.add_card(new_deck.deal())
    
    # Dealer Hand
    
    dealer_hand = Hand()
    dealer_hand.add_card(new_deck.deal())
    dealer_hand.add_card(new_deck.deal())
        
    # Set up the Player's chips
    
    player_chips = Chips()
    
    # Prompt the Player for their bet
    
    take_bet(player_chips)
    
    # Show cards (but keep one dealer card hidden)

    show_some(player_hand, dealer_hand)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        
        hit_or_stand(new_deck, player_hand)
        
        # Show cards (but keep one dealer card hidden)

        show_some(player_hand, dealer_hand)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    
    if player_hand.value <= 21:
        while dealer_hand.value < player_hand.value:
            hit(new_deck, dealer_hand)
    
        # Show all cards
        
        show_all(player_hand, dealer_hand)
    
        # Run different winning scenarios
        
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)
    
    # Inform Player of their chips total 
    
    print("\nPlayer's total chips are: {}".format(player_chips.total))
    
    # Ask to play again

    new_game = input('Would you like to play again? y/n').lower()
    if new_game[0] == 'y':
        playing = True
        continue
    else:
        print('Thanks for playing!')
    break