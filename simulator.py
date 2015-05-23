# coding: utf-8


valores_cartas = list(range(2,11))
valores_cartas.extend(['J', 'Q', 'K', 'A'])
naipes = ['p','e','c','o']
cartas = [ ''.join([str(x), y])  for x in valores_cartas for y in naipes]




dict_cartas = dict(zip(cartas, range(8,60)))


dict_jogadas = {
    (): [],
    (): [],


}

