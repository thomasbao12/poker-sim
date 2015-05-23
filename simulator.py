# coding: utf-8


cards_values = list(range(2,11))
cards_values.extend(['J', 'Q', 'K', 'A'])
suits = ['h','d','c','s']
cards = [ ''.join([str(x), y])  for x in cards_values for y in suits]




dict_cards = dict(zip(cards, range(8,60)))


dict_hands = {
    (1,1,5,1): ["straight flush",9],
    (0,0,2,4): ["four",8],
    (0,0,2,3): ["full-house",7],
    (0,1,4,2): ["flush",6],
    (0,1,5,1): ["flush",6],
    (1,0,5,1): ["straight",5],
    (0,0,3,3): ["three",4],
    (0,0,3,2): ["two pairs",3],
    (0,0,4,2): ["pair",2],
    (0,0,5,1): ["high card",1]
}



class Hand():
    def __init__(self):
        pass

