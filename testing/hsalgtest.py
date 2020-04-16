import random

def handstrength(firstcard, secondcard):
    c1 = firstcard[1]
    c2 = secondcard[1]
    finalhs = 0
    # handstrengthArray array of [green sets, brown sets, blue sets]
    handstrengthArray = [
        [
        [[2,7],[2,8],[2,9],[2,10],[3,8]],
        [[2,11],[2,12],[2,13],[3,9],[3,10],[3,11],[3,12],[4,9],[4,10],[4,11],[5,10]],
        [[3,13],[4,12],[4,13],[5,11],[5,12],[5,13],[6,11],[6,12],[6,13],[7,12]],
        [[6,1],[7,13],[7,1],[8,13]],
        [[8,1],[9,1]]
            ],
        [
        [[2,3],[2,4],[2,5],[2,6],[3,4],[3,5],[3,6],[4,5]],
        [[3,7],[4,6],[4,7],[4,8],[5,6],[5,7],[5,8],[6,7]],
        [[5,9],[6,8],[6,9],[6,10],[7,8],[7,9],[7,10],[8,9]],
        [[7,11],[8,10],[8,11],[8,12],[9,10],[9,11],[9,12],[2,1],[3,1]],
        [[9,13],[10,12],[10,13],[10,1],[11,12],[11,13],[11,1],[12,13],[4,1],[5,1]],
        [[12,1],[13,1]],
            ],
        [
        [[2,2],[3,3],[4,4]],
        [[5,5],[6,6],[7,7]],
        [[8,8],[9,9]],
        [[10,10],[11,11]],
        [[12,12]],
        [[13,13],[1,1]]
            ]
    ]
    if c1 == c2:
        finalhs += 3
    else:
        if (abs(c1-c2) <= 4):
            finalhs += 2
        else:
            finalhs += 1
    if c1 == 1 or c2 == 1:
        finalhs = 0
        if c1 == 1:
            c1 = 14
        if c2 == 1:
            c2 = 14
        if c1 == c2:
            finalhs += 3
        else:
            if (abs(c1-c2) <= 4):
                finalhs += 2
            else:
                finalhs += 1

    def find(cards, colourRating):
        rated = False
        i, j = 0, 0
        while (i < len(handstrengthArray[colourRating-1])) and (not rated):
            while (j < len(handstrengthArray[colourRating-1][i])) and (not rated):
                if handstrengthArray[colourRating-1][i][j] == cards:
                    rated = True
                j += 1
            i += 1
        return i-1
    arr_pos = find([c1,c2], finalhs)
    added_rating = arr_pos/6
    finalhs += added_rating
    c1 = convertCard(firstcard)
    c2 = convertCard(secondcard)
    # check if suited
    if (c1-int(c1)) == (c2-int(c2)):
        finalhs += 1
    finalhs = finalhs/5
    return finalhs

def convertCard(card):
    # e.g. [' A of spades', 1] =: 1.75
    rank = card[1]
    current_suit = card[0][6:]
    if current_suit == 'diamonds':
        suit = 0
    if current_suit == 'clubs':
        suit = 0.25
    if current_suit == 'hearts':
        suit = 0.5
    if current_suit == 'spades':
        suit = 0.75
    finalrank = (rank + suit)/14
    return finalrank

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
    return deck

deek = initDeck()
deek = shuffleDeck(deek)


for i in range (0, 20, 2):
    hs = handstrength(deek[i], deek[i+2])
    print(deek[i])
    print(deek[i+1])
    print(hs)
    print('\n')
