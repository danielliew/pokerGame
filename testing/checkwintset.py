
import random
import time


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

    deck = finalDeck

    for i in range(52):
        x = random.randint(0,51)
        temp = deck[i]
        deck[i] = deck[x]
        deck[x] = temp
    return deck

def checkHand(hand):

    hand_array = hand
    n = len(hand_array)
    verdict = None

    # sort array using quicksort
    def quickSort(hand_array, first, last):
        if first < last:
            partition_index = partition(hand_array,first, last)
            quickSort(hand_array, first, partition_index-1)
            quickSort(hand_array, partition_index+1, last)
    def partition(hand_array, first, last):
        i = first-1
        pivot = hand_array[last][1]
        for x in range(first, last):
            if hand_array[x][1] <= pivot:
                i += 1
                hand_array[i], hand_array[x] = hand_array[x], hand_array[i]
        hand_array[i+1], hand_array[last] = hand_array[last], hand_array[i+1]
        return (i+1)
    quickSort(hand_array, 0, n-1)

    # check for flush part 1
    flush = False
    diamonds = 0
    clubs = 0
    hearts = 0
    spades = 0
    for i in range(n):
        current_suit = hand_array[i][0][6:]
        if current_suit == 'diamonds':
            diamonds += 1
        if current_suit == 'clubs':
            clubs += 1
        if current_suit == 'hearts':
            hearts += 1
        if current_suit == 'spades':
            spades += 1

    # add the ace
    for a in range(4):
        if hand_array[a][1] == 1:
            ace_card = hand_array[a][0]
            hand_array.append([ace_card,14])
            n += 1

    # check for flush part 2
    suit_count = [diamonds, clubs, hearts, spades]
    for j in suit_count:
        if j >= 5:
            flush = True
    flush_array = []
    if diamonds >= 5:
        y = 0
        for i in range(n):
            current_suit = hand_array[i][0][6:]
            if current_suit == 'diamonds':
                flush_array.append(hand_array[i][1])
    if clubs >= 5:
        y = 1
        for i in range(n):
            current_suit = hand_array[i][0][6:]
            if current_suit == 'clubs':
                flush_array.append(hand_array[i][1])
    if hearts >= 5:
        y = 2
        for i in range(n):
            current_suit = hand_array[i][0][6:]
            if current_suit == 'hearts':
                flush_array.append(hand_array[i][1])
    if spades >= 5:
        y = 3
        for i in range(n):
            current_suit = hand_array[i][0][6:]
            if current_suit == 'spades':
                flush_array.append(hand_array[i][1])
    if flush:
        flush_array_length = len(flush_array)
        x_flush = flush_array[flush_array_length-1]

    # check for straight
    straight = False
    for i in range(n-4):
        start = hand_array[i][1]
        count = 1
        straight_array = []
        straight_array.append(hand_array[i][1])
        for j in range(i+1,n):
            next = start + 1
            if hand_array[j][1] == next:
                start += 1
                count += 1
                straight_array.append(hand_array[j][1])
                if count >= 5:
                    straight_suit = hand_array[j][0][6:]
                    if straight_suit == 'diamonds':
                        y_straight = 0
                    if straight_suit == 'clubs':
                        y_straight = 1
                    if straight_suit == 'hearts':
                        y_straight = 2
                    if straight_suit == 'spades':
                        y_straight = 3
                    straight = True
                    straight_array_len = len(straight_array)
                    x_straight = straight_array[straight_array_len-1]
        if straight:
            break

    # check for:
    # royal Flush
    # straight Flush
    # only flush / only Straight
    if (straight and flush) and (straight_array[-5:] == flush_array[-5:]):
        if (straight_array[-5:] == [10,11,12,13,14]) and (flush_array[-5:] == [10,11,12,13,14]):
            verdict = [9, y, 'Royal Flush']
            return verdict
        else:
            verdict = [8, x_straight, 'Straight Flush', y]
            return verdict
    else:
        if straight:
            verdict = [4, x_straight, 'Straight', y_straight]
        if flush:
            verdict = [5, y, 'Flush', x_flush]

    # remove ace_card if there is one
    for a in range(4):
        if hand_array[a][1] == 1:
            hand_array.pop(a)
            n -= 1

    # check doubles
    no_of_doubles = 0
    double = False
    x_double = []
    double_value = []
    for i in range(n-1):
        value = hand_array[i][1]
        if hand_array[i+1][1] == value:
            double = True
            no_of_doubles += 1
            x_double.append(hand_array[i][1])
            double_value.append(hand_array[i][1])
    # get kicker
    if double:
        index = 1
        kicker = hand_array[n-index][1]
        for double_card in x_double:
            if double_card == kicker:
                index += 2
                kicker = hand_array[n-index][1]

    # check three of a kind
    triple_value = []
    triple = False
    for i in range(n-2):
        value = hand_array[i][1]
        count = 1
        for j in range(i+1, n):
            if hand_array[j][1] == value:
                count += 1
            if count == 3:
                x_three = value
                triple = True
                triple_value.append(x_three)

    # check four of a kind
    quad_value = []
    four = False
    for i in range(n-3):
        value = hand_array[i][1]
        count = 1
        for j in range(i+1, n):
            if hand_array[j][1] == value:
                count += 1
            if count == 4:
                four = True
                x_four = value
                quad_value.append(x_four)

    # cross check for overlapping of doubles, triples, quads
    if four:
        for qv in quad_value:
            for tv in triple_value:
                if qv == tv:
                    triple = False
            for dv in double_value:
                if qv == dv:
                    double = False
            if len(double_value) > 3:
                double  = True
    if triple:
        for tv in triple_value:
            for dv in double_value:
                if tv == dv:
                    double = False
            if len(double_value) > 2:
                double = True

    # check for:
    # 4 of a kind
    # full house
    # 2 Pair/3 pair
    # pair
    # else: high card
    if four:
        verdict = [7, x_four, 'Four of a kind']
        return verdict
    else:
        if triple:
            if double:
                verdict = [6, x_three, 'Full house']
                return verdict
            else:
                if verdict != None:
                    return verdict
                else:
                    verdict = [3, x_three, 'Three of a kind']
        else:
            if verdict != None:
                return verdict
            if double:
                n_value = len(x_double)
                if no_of_doubles >= 2:
                    verdict = [2, x_double[n_value-1], 'Two pair', x_double[n_value-2], kicker]
                if no_of_doubles == 1:
                    verdict = [1, x_double[n_value-1], 'Pair', kicker]
    if verdict == None:
        verdict = [0, hand_array[n-1][1], 'High card', hand_array[n-2][1]]

    return (verdict)

def checkWin(pHand, bHand, commCards):

    pEval = pHand + commCards
    dEval = bHand + commCards
    pverdict = checkHand(pEval)
    dverdict = checkHand(dEval)

    win = False
    draw = False
    if pverdict[0] == dverdict[0]:
        if pverdict[1] == dverdict[1]:
            try:
                if pverdict[3] == dverdict[3]:
                    try:
                        if pverdict[4] > dverdict[4]:
                            # chips handling code commented out for testing
                            # c = float(self.currentChips) + float(self.pot)
                            outcome = pverdict[2]
                            win = True
                        else:
                            # d = float(self.botChips) + float(self.pot)
                            outcome = dverdict[2]
                    except IndexError:
                        # c = float(self.currentChips) + float(self.pot)/2
                        # d = float(self.botChips) + float(self.pot)/2
                        outcome = pverdict[2]
                        draw = True
                else:
                    if pverdict[3] > dverdict[3]:
                        # c = float(self.currentChips) + float(self.pot)
                        outcome = pverdict[2]
                        win = True
                    else:
                        # d = float(self.botChips) + float(self.pot)
                        outcome = dverdict[2]
            except  IndexError:
                # c = float(self.currentChips) + float(self.pot)/2
                # d = float(self.botChips) + float(self.pot)/2
                outcome = pverdict[2]
                draw = True
        else:
            if pverdict[1] > dverdict[1]:
                # c = float(self.currentChips) + float(self.pot)
                outcome = pverdict[2]
                win = True
            else:
                # d = float(self.botChips) + float(self.pot)
                outcome = dverdict[2]
    else:
        if pverdict[0] > dverdict[0]:
            # c = float(self.currentChips) + float(self.pot)
            outcome = pverdict[2]
            win = True
        else:
            # d = float(self.botChips) + float(self.pot)
            outcome = dverdict[2]
    if win:
        # self.currentChips = str(c)
        endText = 'You win with ' + outcome
    else:
        if draw:
            # self.currentChips = str(c)
            # self.botChips = str(d)
            endText = 'Draw. Both have ' + outcome
        else:
            # self.botChips = str(d)
            endText = 'Computer wins with ' + outcome
    return (endText)

if __name__ == '__main__':

    n = 100000
    testNo = 0

    print('TEST PART ONE')
    # testing part 1:
    for i in range(n):
        testNo += 1
        deck = initDeck()
        randomHand = deck[:7]
        handoutcome = checkHand(randomHand)
        print('Test no. ', testNo)
        print(randomHand)
        print(handoutcome)
        print('\n')

    testNo = 0

    print('TEST PART TWO')
    # testing part 2:
    for i in range(n):
        testNo += 1
        deck = initDeck()
        playerHand = [deck[0], deck[2]]
        dealerHand = [deck[1], deck[3]]
        commCards = deck[4:9]
        handoutcome = checkWin(playerHand, dealerHand, commCards)
        print('Test no. ', testNo)
        print(playerHand)
        print(dealerHand)
        print(commCards)
        print(handoutcome)
        print('\n')
