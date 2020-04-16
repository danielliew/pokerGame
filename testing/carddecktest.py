import random

def initDeck():
    deck = []
    suits = ['diamonds','clubs','hearts','spades']
    ranks = [' A',' 2',' 3',' 4',' 5',' 6',' 7',' 8',' 9','10',' J',' Q',' K']
    grade = [1,2,3,4,5,6,7,8,9,10,11,12,13]
    for s in range(4):
        for r in range(13):
            nextCard = ranks[r] + ' ' + 'of' + ' ' + suits[s]
            deck.append(nextCard)
            deck.append(grade[r])
    finalDeck = []
    for i in range(0,104,2):
        x = []
        x.append(deck[i])
        x.append(deck[i+1])
        finalDeck.append(x)
    return finalDeck

def shuffleDeck(deck):
    for i in range(52):
        x = random.randint(0,51)
        temp = deck[i]
        deck[i] = deck[x]
        deck[x] = temp
    print(deck)

deck = initDeck()
print(deck)
print('\n')
shuffleDeck(deck)
