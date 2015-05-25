# coding: utf-8

import itertools as it
import numpy as np
import scipy as sp

# Creating a dictionary which maps cards in strings to numbers
cards_values = list(range(2,11))
cards_values.extend(['J', 'Q', 'K', 'A'])
suits = ['h','d','c','s']
cards = [ ''.join([str(x), y])  for x in cards_values for y in suits]

dict_cards = dict(zip(cards, range(8,60)))


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
            print(i)
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
  
    def result(self):
        ways = self.n_loss/self.n_games
        print("You have lost " +  str(ways) + " times in " + str(self.n_games) + " games!\n")

#maos = input("Qual e a sua mao?")
#jogadores = int(input("Quantos sao os jogadores?"))

maos = 'Ah Ad'
jogadores = 2

v = RoundPoker(maos, jogadores)
v.simulate(10000)
v.result()


