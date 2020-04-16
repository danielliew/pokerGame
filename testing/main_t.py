# run in terminal to launch app:
# python3.6 {filepath}

import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window

import random
import sqlite3
import numpy
from functools import partial
from keras.models import model_from_json

# set sql file path
sqlfilepath = '/Users/daniel/Desktop/code/PokerGame/useraccounts.db'

Window.size = (1440,900)
Builder.load_file('/Users/daniel/Desktop/code/PokerGame/kivy_poker_.kv')

class MenuScreen(Screen):
    pass

class AccountScreen(Screen):

    def __init_(self,**kwargs):
        super(AccountScreen, self).__init__(**kwargs)
        self.balance = 0
        self.username = ''

    def checkLoginDetails(self):
        found = False
        host = sqlite3.connect(sqlfilepath)
        cursor = host.cursor()
        username = self.ids['playerusername'].text
        cursor.execute('''
                SELECT balance, password FROM Accounts WHERE username=?
                ''',(username,))
        user = cursor.fetchone()
        host.commit()
        host.close()
        if user != None:
            password = user[1]
            if self.ids['playerpassword'].text == password:
                found = True
                self.username = username
                self.balance = user[0]
                pokerScreenManager.transition.direction = 'left'
                pokerScreenManager.current = 'play'
                pokerScreenManager.get_screen('play').initCurrent(0)
        return found

    def passDetails(self):
        added = False
        if self.balance <= 500:
            self.balance += 5000
            added = True
        return self.username, self.balance, added

class InitialMoneyPopup(Popup):
    pass

class CreateNewAccountScreen(Screen):

    def __init__(self,**kwargs):
        super(CreateNewAccountScreen, self).__init__(**kwargs)
        self.balance = 0
        self.username = ''

    def create(self):
        name = self.ids['name'].text
        self.username = self.ids['username'].text
        password = self.ids['password'].text
        password1 = self.ids['password1'].text
        if password == password1:
            self.balance = 10000
            # 10000 chips on the house
            host = sqlite3.connect(sqlfilepath)
            cursor = host.cursor()
            createCommands =  '''
                                INSERT INTO Accounts(name, username, password, balance)
                                VALUES(?,?,?,?)
                            '''
            cursor.execute(createCommands,(name, self.username, password, self.balance))
            host.commit()
            host.close()
            return True
        else:
            return False

    def passDetails1(self):
        return self.username, self.balance, True

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
    print(verdict)
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

    return verdict

class AddMoneyPopup(Popup):
    pass

class PregamePopup(Popup):

    def __init__(self, p, w):
        super().__init__()
        self.ids['name'].text = 'Hello ' + p + ', choose how much to buy-in to the game'
        self.ids['bet'].max = w
        self.ids['wallet'].text = self.ids['wallet'].text[:8] + str(w)

    def initUpdate(self):
        pokerScreenManager.get_screen('play').popupCallback(float(self.ids['finalBY'].text))

class GameOverPopup(Popup):

    def __init__(self, gameOverText):
        super().__init__()
        self.ids['gameOverText'].text = gameOverText

class PlayGameScreen(Screen):

    currentMove = StringProperty()
    pot = StringProperty()
    currentChips = StringProperty()
    currentBet = StringProperty()
    roundOverText = StringProperty()
    gameOverText = StringProperty()
    botChips = StringProperty()

    def __init__(self, **kwargs):
        super(PlayGameScreen, self).__init__(**kwargs)
        # game vars
        self.deck = None
        self.pot = str(0)
        self.currentBet = str(0)
        self.pHand = []
        self.bHand = []
        self.commCards = []
        self.deckNo = 4
        self.round = 1
        self.amount = None
        self.currentChips = '0'
        self.botChips = '0'
        self.gameNo = 0
        self.smallBlind = True
        self.playerTurn = True
        self.playerallin = False
        self.botallin = False
        self.playerPreviousMove = None
        self.botPreviousMove = None
        self.totalinGameChips = 0
        self.ids['pCard1'].source = 'PNG/Blank.png'
        self.ids['pCard2'].source = 'PNG/Blank.png'
        self.ids['bcard1'].source = 'PNG/Blank.png'
        self.ids['bcard2'].source = 'PNG/Blank.png'
        self.ids['flop1'].source = 'PNG/Blank.png'
        self.ids['flop2'].source = 'PNG/Blank.png'
        self.ids['flop3'].source = 'PNG/Blank.png'
        self.ids['turn'].source = 'PNG/Blank.png'
        self.ids['river'].source = 'PNG/Blank.png'

    def initCurrent(self, n):

        # player's account wallet initialised
        self.gameNo = 0
        addedMoney = False
        created = False
        if n == 2:
            if self.wallet <= 1000:
                self.wallet += 5000
                added = True
            p = self.username
            w = self.wallet
        if n == 1:
            p, w, created = self.manager.get_screen('CreateNewAccount').passDetails1()
        if n == 0:
            p, w, addedMoney = self.manager.get_screen('Account').passDetails()
        the_popup = PregamePopup(p, w)
        the_popup.open()
        if addedMoney:
            AddMoneyPopup().open()
        if created:
            InitialMoneyPopup().open()
        self.username = p
        self.wallet = w
        self.currentBet = str(0)
        self.ids['playername'].text = 'Player: ' + self.username

    def popupCallback(self, buyin):
        self.wallet -= buyin
        self.currentChips = str(buyin)
        # fair start to the bot and player
        self.botChips = self.currentChips
        print('013.e test pot value updated')
        self.initReset()
        self.reset()

    def passonExit(self):
        ended = False
        if self.gameNo == 5:
            ended = True
        return self.username, self.currentChips, self.wallet, ended

    def initGame(self):

        def initDeck(self):
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
            self.deck = finalDeck

        def shuffleDeck(self):
            deck = self.deck
            for i in range(52):
                x = random.randint(0,51)
                temp = deck[i]
                deck[i] = deck[x]
                deck[x] = temp
            self.deck = deck

        def initCards(self):
            self.ids['pCard1'].source = self.showImgs(self.deck[0])
            self.ids['pCard2'].source = self.showImgs(self.deck[2])
            self.ids['bcard1'].source = 'PNG/gray_back.png'
            self.ids['bcard2'].source = 'PNG/gray_back.png'
            #
            self.pHand.append(self.deck[0])
            self.pHand.append(self.deck[2])
            self.bHand.append(self.deck[1])
            self.bHand.append(self.deck[3])
            #
            self.updateCurrentStat(0)

        def blind(self):
            if self.smallBlind == True:
                self.currentChips = str(float(self.currentChips)-50)
                if float(self.currentChips) < 0:
                    self.currentChips = str(0)
                    print('nigger')
                self.botChips = str(float(self.botChips)-100)
                if float(self.botChips) < 0:
                    self.botChips = str(0)
            else:
                self.currentChips = str(float(self.currentChips)-100)
                if float(self.currentChips) < 0:
                    self.currentChips = str(0)
                self.botChips = str(float(self.botChips)-50)
                if float(self.botChips) < 0:
                    self.botChips = str(0)
                self.updateCurrentStat(0.5)
                Clock.schedule_once(partial(self.botMove),1.5)
                self.playerPreviousMove = None
            self.smallBlind = not self.smallBlind
            self.currentBet = str(float(self.currentBet)+150)
            self.ids['inGameBet'].max = self.currentChips

        initDeck(self)
        shuffleDeck(self)
        initCards(self)
        blind(self)

    def showImgs(self,card):
        cardRank = card[0][1:2]
        cardSuit = card[0][6:]
        if cardRank == '0':
            cardRank = '10'
        if cardSuit == 'diamonds':
            cs = 'D'
        if cardSuit == 'clubs':
            cs = 'C'
        if cardSuit == 'hearts':
            cs = 'H'
        if cardSuit == 'spades':
            cs = 'S'
        imgSrc = 'PNG/' + cardRank + cs + '.png'
        return imgSrc

    def check(self):
        if self.playerTurn:
            if self.round <= 4:
                if self.amount == None:
                    self.updateCurrentStat(-1)
                    self.playerPreviousMove = 1
                    if self.botPreviousMove == None:
                        self.updateCurrentStat(0.5)
                    else:
                        Clock.schedule_once(partial(self.checkRoundover),2)

    def fold(self):
        if self.playerTurn:
            self.updateCurrentStat(-2)
            self.gameNo += 1
            if (self.gameNo == 5) or (float(self.botChips) <= 0) or (float(self.currentChips) <= 0):
                self.wallet += float(self.currentChips)
                self.botChips = str(float(self.botChips) + float(self.pot))
                endText = 'You folded. Computer wins'
                self.gameOver(endText)
            else:
                d = float(self.botChips) + float(self.pot)
                self.botChips = str(d)
                self.gameNo += 1
                Clock.schedule_once(partial(self.reset),1)

    def Raise(self, amount):
        if self.playerTurn:
            if (self.round <= 4) and (float(self.currentChips) > 0):
                if float(amount) == float(self.currentChips):
                    Clock.schedule_once(partial(self.openAllinPopup),1.5)
                else:
                    self.currentChips = str(float(self.currentChips)-amount)
                    self.currentBet = str(float(self.currentBet)+amount)
                    self.amount = amount
                    self.updateCurrentStat(-3)
                    self.ids['inGameBet'].max = self.currentChips
                    self.playerPreviousMove = 3 + float(self.amount)/float(self.currentChips)
                    self.updateCurrentStat(0.5)

    def openAllinPopup(self,*args):
        self.ids['allinPopup'].open()

    def allIn(self, amount):
        self.updateCurrentStat(-4)
        self.currentChips = str(float(self.currentChips)-amount)
        self.currentBet = str(float(self.currentBet)+amount)
        self.amount = amount
        self.playerallin = True
        self.playerPreviousMove = 4
        Clock.schedule_once(partial(self.botMove),1.5)

    def confirmedallIn(self):
        if True:
            Clock.schedule_once(partial(self.allInDeal), 1.5)
        if True :
            Clock.schedule_once(partial(self.checkRoundover), 5)

    def allInDeal(self,*args):
        while self.round < 4:
            self.deal()
        self.round = 5

    def call(self):
        if self.playerTurn:
            self.updateCurrentStat(-5)
            self.currentChips = str(float(self.currentChips)-self.amount)
            if float(self.currentChips) <= 0:
                self.currentChips = str(0)
            self.currentBet = str(float(self.currentBet)+float(self.currentBet))
            if self.botallin:
                self.confirmedallIn()
            else:
                Clock.schedule_once(partial(self.checkRoundover),2)

    def botMove(self, previousMove, *args):

        # The AI Bot

        def com_check(self):
            if self.amount == None:
                self.updateCurrentStat(1)
                self.botPreviousMove = 1
                if self.playerPreviousMove != None:
                    Clock.schedule_once(partial(self.checkRoundover),2)

        def com_fold(self):
            self.updateCurrentStat(2)
            self.gameNo += 1
            if (self.gameNo == 5) or (float(self.botChips) <= 0) or (float(self.currentChips) <= 0):
                self.currentChips = str(float(self.currentChips) + float(self.pot))
                self.wallet += float(self.currentChips)
                endText = 'Computer folds. You win.'
                self.gameOver(endText)
            else:
                d = float(self.botChips) + float(self.pot)
                self.botChips = str(d)
                self.gameNo += 1
                Clock.schedule_once(partial(self.reset),1)

        def com_raise(self, amount):
            self.amount = amount
            if (self.round <= 4) and (float(self.botChips) > 0):
                self.botChips = str(float(self.botChips)-amount)
                self.currentBet = str(float(self.currentBet)+amount)
                self.amount = amount
                if amount == float(self.botChips):
                    self.updateCurrentStat(4)
                    self.botallin = True
                else:
                    self.updateCurrentStat(3)

        def com_call(self):
            self.updateCurrentStat(5)
            self.botChips = str(float(self.botChips)-self.amount)
            if float(self.botChips) <= 0:
                self.botChips = str(0)
            self.currentBet = str(float(self.currentBet)+float(self.currentBet))
            if self.playerallin:
                self.confirmedallIn()
            else:
                Clock.schedule_once(partial(self.checkRoundover),2)

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

        def handstrength(firstcard, secondcard):
            c1 = firstcard[1]
            c2 = secondcard[1]
            finalhs = 0
            # handstrengthArray array of [green sets, brown sets, blue sets]
            handstrengthArray = [
                [
                [[2,2],[3,3],[4,4]],
                [[5,5],[6,6],[7,7]],
                [[8,8],[9,9]],
                [[10,10],[11,11]],
                [[12,12]],
                [[13,13],[1,1]]
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
                [[2,7],[2,8],[2,9],[2,10],[3,8]],
                [[2,11],[2,12],[2,13],[3,9],[3,10],[3,11],[3,12],[4,9],[4,10],[4,11],[5,10]],
                [[3,13],[4,12],[4,13],[5,11],[5,12],[5,13],[6,11],[6,12],[6,13],[7,12]],
                [[6,1],[7,13],[7,1],[8,13]],
                [[8,1],[9,1]]
                    ],
            ]
            if c1 == c2:
                finalhs += 3
            else:
                if c1-c2 <= 4:
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

        def convertpfRawData(rawdata):

            finalarray = []
            for i in rawdata:
                card1 = convertCard(i[0])
                card2 = convertCard(i[1])
                currenthandstrength = handstrength(i[0], i[1])
                bigblind = i[2]
                totalinGameChips = i[3] + i[4] + i[5]
                potbefore = i[3]/totalinGameChips
                botschips = i[4]/totalinGameChips
                playerschips = i[5]/totalinGameChips
                movebefore = i[6]/6
                finalarray.append([card1, card2, currenthandstrength, bigblind, potbefore, botschips, playerschips, movebefore])
            return numpy.array(finalarray)

        def convertfRawData(rawdata):

            finalarray = []
            for i in rawdata:
                card1 = convertCard(i[0])
                card2 = convertCard(i[1])
                flop1 = convertCard(i[2])
                flop2 = convertCard(i[3])
                flop3 = convertCard(i[4])
                totalinGameChips = i[5] + i[6] + i[7]
                potbefore = i[5]/totalinGameChips
                botschips = i[6]/totalinGameChips
                playerschips = i[7]/totalinGameChips
                movebefore = i[8]/6
                finalarray.append([card1, card2, flop1, flop2, flop3, potbefore, botschips, playerschips, movebefore])
            return numpy.array(finalarray)

        def converttRawData(rawdata):

            finalarray = []
            for i in rawdata:
                card1 = convertCard(i[0])
                card2 = convertCard(i[1])
                flop1 = convertCard(i[2])
                flop2 = convertCard(i[3])
                flop3 = convertCard(i[4])
                turn = convertCard(i[5])
                totalinGameChips = i[6] + i[7] + i[8]
                potbefore = i[6]/totalinGameChips
                botschips = i[7]/totalinGameChips
                playerschips = i[8]/totalinGameChips
                movebefore = i[9]/6
                finalarray.append([card1, card2, flop1, flop2, flop3, turn, potbefore, botschips, playerschips, movebefore])
            return numpy.array(finalarray)

        def convertrRawData(rawdata):

            finalarray = []
            for i in rawdata:
                card1 = convertCard(i[0])
                card2 = convertCard(i[1])
                flop1 = convertCard(i[2])
                flop2 = convertCard(i[3])
                flop3 = convertCard(i[4])
                turn = convertCard(i[5])
                river = convertCard(i[6])
                totalinGameChips = i[7] + i[8] + i[9]
                potbefore = i[7]/totalinGameChips
                botschips = i[8]/totalinGameChips
                playerschips = i[9]/totalinGameChips
                movebefore = i[10]/6
                finalarray.append([card1, card2, flop1, flop2, flop3, turn, river, potbefore, botschips, playerschips, movebefore])
            return numpy.array(finalarray)

        def getDecision(currentinput, brainnumber):
            jsonfilepath = '/Users/daniel/Desktop/code/PokerGame/model' + str(brainnumber) + '.json'
            h5filepath = '/Users/daniel/Desktop/code/PokerGame/model' + str(brainnumber) + '.h5'
            # load json and create the river model
            json_file = open(jsonfilepath, 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            loaded_model = model_from_json(loaded_model_json)
            # load weights into new model
            loaded_model.load_weights(h5filepath)
            print("Loaded model from disk")
            # make a prediction
            output_new = loaded_model.predict(currentinput)
            # show the inputs and predicted outputs
            print('output: ', output_new)
            return output_new

        # ai brain
        move = self.playerPreviousMove
        if move == None:
            move = 0
        if self.round == 1:
            if self.smallBlind:
                botblind = 0
            else:
                botblind = 1
            currentinput = [[self.pHand[0], self.pHand[1], botblind, float(self.pot), float(self.currentChips), float(self.botChips), move]]
            formattedinput = convertpfRawData(currentinput)
        if self.round == 2:
            currentinput = [[self.pHand[0], self.pHand[1], self.commCards[0], self.commCards[1], self.commCards[2], float(self.pot), float(self.currentChips), float(self.botChips), move]]
            formattedinput = convertfRawData(currentinput)
        if self.round == 3:
            currentinput = [[self.pHand[0], self.pHand[1], self.commCards[0], self.commCards[1], self.commCards[2], self.commCards[3], float(self.pot), float(self.currentChips), float(self.botChips), move]]
            formattedinput = converttRawData(currentinput)
        if self.round == 4:
            currentinput = [[self.pHand[0], self.pHand[1], self.commCards[0], self.commCards[1], self.commCards[2], self.commCards[3], self.commCards[4], float(self.pot), float(self.currentChips), float(self.botChips), move]]
            formattedinput = convertrRawData(currentinput)
        decision = getDecision(formattedinput, self.round)
        decision = decision[0][0]
        decision = decision*6
        if self.playerPreviousMove == None:
            # can check/fold/raise/allin
            if (decision <= 4) and (decision > 3):
                raiseamount = (decision-3)*float(self.botChips)
                if raiseamount > 0.97*float(self.botChips):
                    raiseamount = self.botChips
                raiseamount = int(raiseamount)
                com_raise(self, raiseamount)
            else:
                check_difference = decision-1
                fold_difference = decision-2
                x = min([check_difference, fold_difference])
                if x == check_difference:
                    com_check(self)
                if x == fold_difference:
                    com_fold(self)
        else:
            check_difference = decision-1
            fold_difference = decision-2
            call_difference = decision-5
            if self.playerallin:
                if min([call_difference, fold_difference]) == fold_difference:
                    com_fold(self)
                if min([call_difference, fold_difference]) == call_difference:
                    com_call(self)
            else:
                if (decision <= 4) and (decision > 3):
                    raiseamount = (decision-3)*float(self.botChips)
                    if raiseamount > 0.97*float(self.botChips):
                        raiseamount = self.botChips
                    raiseamount = int(raiseamount)
                    com_raise(self, raiseamount)
                else:
                    if self.amount == None:
                        if min([check_difference, fold_difference]) == check_difference:
                            com_check(self)
                        if min([check_difference, fold_difference]) == fold_difference:
                            com_fold(self)
                    else:
                        if min([call_difference, fold_difference]) == fold_difference:
                            com_fold(self)
                        if min([call_difference, fold_difference]) == call_difference:
                            com_call(self)

    def updateCurrentStat(self, x):

        # Prompt handler

        if x == -5:
            self.currentMove = 'Player calls'
            self.playerTurn = False
        if x == -4:
            self.currentMove = 'Player moves all in'
            self.playerTurn = False
        if x == -3:
            self.currentMove = 'Player raises to ' + str(self.amount)
            self.playerTurn = False
        if x == -2:
            self.currentMove = 'Player folds.'
            self.playerTurn = False
        if x == -1:
            self.currentMove = 'Player checks'
            self.playerTurn = False
        if x == 0:
            self.currentMove = 'Player ' + self.username + ' its your turn'
        if x == 0.5:
            self.currentMove = 'Computer\'s turn'
            Clock.schedule_once(partial(self.botMove),2)
        if x == 1:
            self.currentMove = 'Computer checks'
            self.playerTurn = True
        if x == 2:
            self.currentMove = 'Computer folds'
            self.playerTurn = True
        if x == 3:
            self.currentMove = 'Computer raises to ' + str(self.amount)
            self.playerTurn = True
        if x == 4:
            self.currentMove = 'Computer moves all in. Player\'s move.'
            self.playerTurn = True
        if x == 5:
            self.currentMove = 'Computer calls'
            self.playerTurn = True

    def checkRoundover(self, *args):
        if self.round <= 4:
            self.playerallin = False
            self.dealerallin = False
            self.playerPreviousMove = None
            self.botPreviousMove = None
            self.amount = None
            self.playerTurn = not self.playerTurn
            self.deal()
            if self.playerTurn:
                self.updateCurrentStat(0)
            else:
                self.updateCurrentStat(0.5)
        if self.round > 4:
            self.ids['bcard1'].source = self.showImgs(self.bHand[0])
            self.ids['bcard2'].source = self.showImgs(self.bHand[1])
            Clock.schedule_once(partial(self.checkWin),2)

    def deal(self, *args):
        self.pot = str(float(self.pot)+float(self.currentBet))
        self.currentBet = '0'
        if self.round == 1:
            self.commCards.append(self.deck[self.deckNo])
            self.ids['flop1'].source = self.showImgs(self.deck[self.deckNo])
            self.deckNo += 1
            self.commCards.append(self.deck[self.deckNo])
            self.ids['flop2'].source = self.showImgs(self.deck[self.deckNo])
            self.deckNo += 1
            self.commCards.append(self.deck[self.deckNo])
            self.ids['flop3'].source = self.showImgs(self.deck[self.deckNo])
            self.deckNo += 1
        if self.round == 2:
            self.commCards.append(self.deck[self.deckNo])
            self.ids['turn'].source = self.showImgs(self.deck[self.deckNo])
            self.deckNo += 1
        if self.round == 3:
            self.commCards.append(self.deck[self.deckNo])
            self.ids['river'].source = self.showImgs(self.deck[self.deckNo])
        self.round += 1


    def checkWin(self,*args):

        pEval = self.pHand + self.commCards
        dEval = self.bHand + self.commCards
        print(pEval)
        print(dEval)
        pverdict = checkHand(pEval)
        print(pverdict)
        dverdict = checkHand(dEval)
        print(dverdict)

        win = False
        draw = False
        if pverdict[0] == dverdict[0]:
            if pverdict[1] == dverdict[1]:
                try:
                    if pverdict[3] == dverdict[3]:
                        try:
                            if pverdict[4] > dverdict[4]:
                                c = float(self.currentChips) + float(self.pot)
                                outcome = pverdict[2]
                                win = True
                            else:
                                d = float(self.botChips) + float(self.pot)
                                outcome = dverdict[2]
                        except IndexError:
                            c = float(self.currentChips) + float(self.pot)/2
                            d = float(self.botChips) + float(self.pot)/2
                            outcome = pverdict[2]
                            draw = True
                    else:
                        if pverdict[3] > dverdict[3]:
                            c = float(self.currentChips) + float(self.pot)
                            outcome = pverdict[2]
                            win = True
                        else:
                            d = float(self.botChips) + float(self.pot)
                            outcome = dverdict[2]
                except  IndexError:
                    c = float(self.currentChips) + float(self.pot)/2
                    d = float(self.botChips) + float(self.pot)/2
                    outcome = pverdict[2]
                    draw = True
            else:
                if pverdict[1] > dverdict[1]:
                    c = float(self.currentChips) + float(self.pot)
                    outcome = pverdict[2]
                    win = True
                else:
                    d = float(self.botChips) + float(self.pot)
                    outcome = dverdict[2]
        else:
            if pverdict[0] > dverdict[0]:
                c = float(self.currentChips) + float(self.pot)
                outcome = pverdict[2]
                win = True
            else:
                d = float(self.botChips) + float(self.pot)
                outcome = dverdict[2]
        if win:
            self.currentChips = str(c)
            endText = 'You win with ' + outcome
        else:
            if draw:
                self.currentChips = str(c)
                self.botChips = str(d)
                endText = 'Draw. Both have ' + outcome
            else:
                self.botChips = str(d)
                endText = 'Computer wins with ' + outcome
        self.gameNo = 5
        if (self.gameNo == 5) or (float(self.botChips) <= 0) or (float(self.currentChips) <= 0):
            self.wallet += float(self.currentChips)
            self.gameOver(endText)
        else:
            self.openWinPopup(endText)

    def gameOver(self, winner):
        GameOverPopup(winner).open()

    def openWinPopup(self,winner):
        self.roundOverText = winner
        self.ids['winPopup'].open()

    def restart(self):
        self.reset()

    def initReset(self):
        self.deck = None
        self.pot = str(0)
        self.currentBet = str(0)
        self.pHand = []
        self.bHand = []
        self.commCards = []
        self.deckNo = 4
        self.round = 1
        self.amount = None
        self.gameNo = 3
        self.smallBlind = True
        self.playerTurn = True
        self.playerallin = False
        self.botallin = False
        self.playerPreviousMove = None
        self.botPreviousMove = None
        self.totalinGameChips = float(self.botChips) + float(self.currentChips)
        self.ids['pCard1'].source = 'PNG/Blank.png'
        self.ids['pCard2'].source = 'PNG/Blank.png'
        self.ids['bcard1'].source = 'PNG/Blank.png'
        self.ids['bcard2'].source = 'PNG/Blank.png'
        self.ids['flop1'].source = 'PNG/Blank.png'
        self.ids['flop2'].source = 'PNG/Blank.png'
        self.ids['flop3'].source = 'PNG/Blank.png'
        self.ids['turn'].source = 'PNG/Blank.png'
        self.ids['river'].source = 'PNG/Blank.png'

    def reset(self, *args):

        self.deck = None
        self.pot = '0'
        self.pHand = []
        self.bHand = []
        self.commCards =[]
        self.round = 1
        self.ids['pCard1'].source = 'PNG/Blank.png'
        self.ids['pCard2'].source = 'PNG/Blank.png'
        self.ids['bcard1'].source = 'PNG/Blank.png'
        self.ids['bcard2'].source = 'PNG/Blank.png'
        self.ids['flop1'].source = 'PNG/Blank.png'
        self.ids['flop2'].source = 'PNG/Blank.png'
        self.ids['flop3'].source = 'PNG/Blank.png'
        self.ids['turn'].source = 'PNG/Blank.png'
        self.ids['river'].source = 'PNG/Blank.png'
        self.currentBet = '0'
        self.deckNo = 4
        self.playerallin = False
        self.dealerallin = False
        self.playerPreviousMove = None
        self.botPreviousMove = None
        self.amount = None
        self.ids['inGameBet'].max = self.currentChips
        self.initGame()

    def compare(self):
        if float(self.currentChips) == float(self.botChips):
            return 'Its a draw! \n\nBoth you and the computer finished with: ' + self.currentChips
        else:
            if float(self.currentChips) > float(self.botChips):
                return 'You win! \n\nYou finished with: ' + self.currentChips + '\n\nComputer finished with: ' + self.botChips
            else:
                return 'Computer wins! \n\nYou finished with: ' + self.currentChips + '\n\nComputer finished with: ' + self.botChips

class GameoverScreen(Screen):

    gameVerdict = StringProperty()
    endWallet = StringProperty()

    def initiate(self):
        win = self.manager.get_screen('play').compare()
        p, c, w, e = self.manager.get_screen('play').passonExit()
        self.endWallet = 'Your current wallet balance: ' + str(w)
        print(win)
        self.gameVerdict = win

# global identifier to manage screens
pokerScreenManager = ScreenManager()
pokerScreenManager.add_widget(MenuScreen(name='Menu'))
pokerScreenManager.add_widget(AccountScreen(name='Account'))
pokerScreenManager.add_widget(CreateNewAccountScreen(name='CreateNewAccount'))
pokerScreenManager.add_widget(PlayGameScreen(name='play'))
pokerScreenManager.add_widget(GameoverScreen(name='gameOver'))

# main app class
class pokerApp(App):

    def build(self):
        self.sm = pokerScreenManager
        return self.sm

    def on_stop(self):
        self.updateSQL()

    # update sql wallets
    def updateSQL(*args):
        # save current user progress
        exitFrom = pokerScreenManager.current
        if exitFrom == 'play' or exitFrom == 'gameOver':
            userUsername, userInGameChips, userWallet, ended = pokerScreenManager.get_screen('play').passonExit()
            if not ended:
                userWallet += float(userInGameChips)
            print(userWallet, userUsername)
            host = sqlite3.connect(sqlfilepath)
            cursor = host.cursor()
            cursor.execute('UPDATE Accounts SET balance="{}" WHERE username="{}"'.format(userWallet, userUsername))
            host.commit()
            host.close()

# initialise or verify there is a SQL file to store Accounts
def initSQL():
    try:
        f = open(sqlfilepath,'r')
        f.close()
    except FileNotFoundError:
        host = sqlite3.connect(sqlfilepath)
        cursor = host.cursor()
        initCommands =  '''
                        CREATE TABLE Accounts(id INTEGER PRIMARY KEY, name TEXT,
                        username TEXT, password TEXT, balance FLOAT)
                        '''
        cursor.execute(initCommands)
        host.commit()
        host.close()

if __name__ == '__main__':
    initSQL()
    pokerApp().run()
