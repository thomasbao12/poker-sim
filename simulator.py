# coding: utf-8


cards_values = list(range(2,11))
cards_values.extend(['J', 'Q', 'K', 'A'])
suits = ['h','d','c','s']
cards = [ ''.join([str(x), y])  for x in cards_values for y in suits]




dict_cards = dict(zip(cards, range(8,60)))


dict_hands = {
    (): ["straight flush"],
    (): ["four"],
    (): ["full-house"],
    (): ["flush"],
    (): ["flush"],
    (): ["straight"],
    (): ["three"],
    (): ["two pairs"],
    (): ["pair"],
    (): ["high card"]
}



class Hand():
    def __init__(self):
        pass

