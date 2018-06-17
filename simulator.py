# coding: utf-8

import itertools as it
import numpy as np
import scipy as sp
import math

# Creating a dictionary which maps cards in strings to numbers
cards_values = list(range(2,11))
cards_values.extend(['J', 'Q', 'K', 'A'])
suits = ['h','d','c','s']
cards = [ ''.join([str(x), y])  for x in cards_values for y in suits]

dict_cards = dict(zip(cards, range(8,60)))
reverse_dict_cards = {v:k for k, v in dict_cards.items()}

'''
class Card():

    @property
    

    def __init__(self, string):
        self.string = string        
'''


# A dictionary for Hands and its values
# Each key keeps a code in a tuple
# First int corresponds to is_straight, second int  is_flush
# Third int corresponds to number of different elements
# Fourth int corresponds to the number of occurences of the maximum element
dict_hands = {
    (True,True,5,1): ["straight flush",9],
    (False,False,2,4): ["four",8],
    (False,False,2,3): ["full-house",7],
    (False,True,4,2): ["flush",6],
    (False,True,5,1): ["flush",6],
    (True,False,5,1): ["straight",5],
    (False,False,3,3): ["three",4],
    (False,False,3,2): ["two pairs",3],
    (False,False,4,2): ["pair",2],
    (False,False,5,1): ["high card",1]
}


class Deck():
    def __init__(self):
        self.deck=list(range(8,60))    

    def remove_cards(self, cards):
        for i in cards: self.deck.remove(i)

    def take_card(self, n=1):
        x = np.random.choice(self.deck, n, replace=False) 
        for i in x: self.deck.remove(i)
        return x
        # Take a sample from self.deck with no replacement

    def take_w_replace(self, n=1):
        # Take a sample from self.deck with replacement
        return np.random.choice(self.deck, n=1)

class Hand():
    """
     Recebe a mao de dois valores e o flop
    e guarda o valor dela
    """
    def __init__(self, twocards, flop):
        self.twocards=twocards
        self.flop=flop
        self.best_hand()
         
    def is_flush(self, hand):
        f_suits  = [ i % 4 for i in hand ]
        if f_suits.count(f_suits[0]) == len(f_suits): # Fast Algorithm
            return True
        else:
            return False
    
    def is_straight(self, f_values):
        if ( len(set(f_values))==5 and ( f_values[4] - f_values[0] ) == 4 )  or f_values==[2, 3, 4, 5, 14]:
            return True
        else:
            return False
   
    def find_ocur_max(self, f_values):
        mode = max(set(f_values), key=f_values.count)
        return f_values.count(mode)    
    
    def evaluate_hand(self, hand):
        f_values = [ i // 4 for i in hand ]
        f_values.sort()
        key_hands =(self.is_straight(f_values), self.is_flush(hand), len(set(f_values)), self.find_ocur_max(f_values)) 
        initial_value = dict_hands[key_hands]
        draw_value = hand[0] * 10000 + hand[1] * 1000 + hand[2] * 100 + hand[3] * 10 + hand[4]
        final_value = initial_value[1]*100000 + draw_value
        return final_value

    def best_hand(self):
        hand = np.append(self.twocards,self.flop)
        hands = list(it.combinations(hand, 5))
        max_hand = hands[0]
        for i in hands:
            j = self.evaluate_hand(i)
            if j > self.evaluate_hand(max_hand):
                max_hand = i
        self.best=max_hand
        self.best_value=self.evaluate_hand(max_hand)

class RoundPoker():
    """ Cada objeto representa uma jogada de Poker
        Serao definidos numero de jogadores, flop e maos
    """
    def __init__(self, hand_player, n_players=2):
        self.hand_player = str.split(hand_player) # Remember to switch the strings
        self.hand_player = [ dict_cards[i] for i in self.hand_player ]
        print(hand_player)
        self.n_players = n_players

    def simulate(self, n_simulacao=1000):
        self.n_wins = 0
        self.n_draws = 0
        self.n_loss = 0
        self.n_games = 0
        for i in range(n_simulacao):
            self.n_games += 1
            self.deck = Deck()
            self.deck.remove_cards(self.hand_player)
            self.flop = self.deck.take_card(5)
            self.hand = Hand(self.hand_player, self.flop)
            for j in range(self.n_players):
                rival = Hand(self.deck.take_card(2), self.flop)
                if ( self.hand.best_value < rival.best_value ):
                    self.n_loss += 1
                    break
        self.ways = self.n_loss/self.n_games
            
    def simulate_with_mean(self, n_simulation=100, n_mean=10):
        total = np.array([])
        for i in range(n_mean):
            self.simulate(100)
            print(self.ways)
            total = np.append(total, self.ways)
        self.ways = np.average(total)

    def result(self):
        print("You have lost " +  str(self.ways) + " times in " + str(self.n_games) + " games!\n")


# v = RoundPoker(maos, jogadores)
# v.simulate(10000)
# v.result()


# list of 2 human readable card strings such as ['Ah', '10c']
def get_chen_formula(cards):

    def get_val(card):
        val = card[:-1]
        if val == "A":
            val = 14
        elif val == "K":
            val = 13
        elif val == "Q":
            val = 12
        elif val == "J":
            val = 11
        else:
            val = int(val)
        return val

    def get_suit(card):
        return card[-1:]

    def get_delta(card1, card2):
        val1 = get_val(card1)
        val2 = get_val(card2)
        delta = min(
            abs(val1 - val2),
            abs(min(val1, val2) - (max(val1, val2) - 13))
        )
        return delta

    score = 0
    for card in cards:
        val = card[:-1]
        if val == "A":
            val = 10
        elif val == "K":
            val = 8
        elif val == "Q":
            val = 7
        elif val == "J":
            val = 6
        else:
            val = float(val) / 2
        score = max(val, score)

    if get_val(cards[0]) == get_val(cards[1]):
        return max(5, score * 2)

    if get_suit(cards[0]) == get_suit(cards[1]):
        score += 2
    
    delta = get_delta(cards[0], cards[1])
    if delta == 1:
        score += 1
    elif delta == 2:
        score -= 1
    elif delta == 3:
        score -= 2
    elif delta == 4:
        score -= 4
    else:
        score -= 5
    
    return int(math.ceil(score))

# get chen score distribution
n = 10000
dp = 100.0 / n
chen_formula_counts = {}
for i in xrange(n):
    deck = Deck()
    cards = deck.take_card(n=2)
    cards = [reverse_dict_cards[card] for card in cards]
    score = get_chen_formula(cards)
    chen_formula_counts[score] = chen_formula_counts.get(score, 0) + dp

for k in sorted(chen_formula_counts.keys()):
    print "{}, {}%".format(k, chen_formula_counts.get(k))

print(chen_formula_counts)
