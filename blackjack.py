import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8,'Nine':9, 'Ten':10, 
          'Jack':10, 'Queen':10, 'King':10, 'Ace':11}
playing = True


class Card():
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.rank + " of " + self.suit

class Deck():
    
    def __init__(self):
        self.deck = []
        
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit,rank)
                self.deck.append(created_card)
    
    def shuffle(self):
        random.shuffle(self.deck)
    
    def deal(self):
        single_card = self.deck.pop()
        return single_card
    
    def __str__(self):
        deck_cards = ''
        for card in self.deck:
            deck_cards +='\n'+card.__str__()
        return 'The deck has:' + deck_cards

class Hand():
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
        while self.value > 21 and self.aces:
            self.value = self.value-10
            self.aces = self.aces-1

class Chips():
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total+=self.bet
    
    def lose_bet(self):
        self.total-=self.bet


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("How much would you like to bet? "))
        except ValueError:
            print("I'm sorry, I do not understand. Please input an integer if you would like to bet.")
        else:
            if chips.bet > chips.total:
                print("Sorry, your bet can't exceed",chips.total)
            elif chips.bet < 0:
                print("Stop trying to steal money.")
            else:
                break

def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    while True:
        x = input(f"\nYou have {hand.value}. Would you like to Hit or Stand? Enter h or s: ")
        if x.lower()[0]== 'h':
            hit(deck,hand)
        elif x.lower()[0] == 's':
            print("\nPLAYER IS STANDING. \n\nDealer will now hit if their total is less than 17. \nDealer will continue to hit until their total is equal to or greater than 17.")
            playing = False
        else:
            print("Sorry, please try again.")
            continue
        break

def show_some(player,dealer):
    print("\nDEALER'S HAND: ")
    print("<card hidden>")
    print(dealer.cards[1])
    print("\nPLAYER'S HAND: ",*player.cards, sep ='\n')
    
def show_all(player,dealer):
    print("\nDEALER'S HAND: ",*dealer.cards, sep ='\n')
    print(f"Dealer has hit a total value of {dealer.value}.")
    print("\nPLAYER'S HAND: ",*player.cards, sep ='\n')
    print(f"Player has hit a total value of {player.value}.")

def player_busts(player,dealer,chips):
    print ("\nPLAYER BUTSTS! Player has hit a total value of: ",player.value)
    chips.lose_bet()
    

def player_wins(player,dealer,chips):
    print("\nPLAYER WINS!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("\nDEALER BUSTS!")
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print("\nDEALER WINS!")
    chips.lose_bet()
    
def push(player,dealer):
    print("\nDEALER AND PLAYER TIE. IT'S A PUSH!")

        
# I have set up the Player's chips outside the loop in order to keep count of total chips should the player replay
player_chips = Chips()

while True:
    # Print an opening statement
    print("Welcome to BlackJack! Get as close to 21 as you can without going over!\nDealer hits until they reach 17. Aces count as 1 or 11.")
    
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    print(f"\nYou have {player_chips.total} chips.")
    
  
    
    # Prompt the Player for their bet
    take_bet(player_chips)
    
    # Show cards (but keep one dealer card hidden)
    #show_some(player_hand,dealer_hand)
    
    while playing:  # recall this variable from our hit_or_stand function
        show_some(player_hand,dealer_hand)
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand)
        
        # Show cards (but keep one dealer card hidden)
        #show_some(player_hand,dealer_hand) 
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            show_all(player_hand,dealer_hand)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)    
    
        # Show all cards
        show_all(player_hand,dealer_hand)
        
        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)
    
    # Inform Player of their chips total 
    print(f"\nYou have {player_chips.total} chips.")
    
    # Ask to play again
    if player_chips.total >0:
        new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")
    
        if new_game[0].lower()=='y':
            playing=True
            continue
        else:
            print("\nThanks for playing!")
            break
    else:
        print("\nThanks for playing!")
        break