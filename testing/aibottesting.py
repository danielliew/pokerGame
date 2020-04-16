import numpy
from keras.models import model_from_json

def botMove(currentinput, round, botChips, playerPreviousMove):

    # The AI Bot

    def com_check():
        print('check')

    def com_fold():
        print('fold')

    def com_raise(amount, chips):
        if amount == chips:
            print('all in ', amount)
        else:
            print('raise ', amount)

    def com_call():
        print('call')

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
    currentinput = [currentinput]
    if round == 1:
        formattedinput = convertpfRawData(currentinput)
    if round == 2:
        formattedinput = convertfRawData(currentinput)
    if round == 3:
        formattedinput = converttRawData(currentinput)
    if round == 4:
        formattedinput = convertrRawData(currentinput)
    playerallin = False
    if playerPreviousMove == 4:
        playerallin = True
    amount = None
    if (playerPreviousMove > 3) and (playerPreviousMove <=4):
        amount = 1
    if playerPreviousMove == 0:
        playerPreviousMove = None
    decision = getDecision(formattedinput, round)
    decision = decision[0][0]
    decision = decision*6
    print('converted output: ', decision)
    if playerPreviousMove == None:
        # can check/fold/raise/allin
        if (decision <= 4) and (decision > 3):
            raiseamount = (decision-3)*float(botChips)
            if raiseamount > 0.97*float(botChips):
                raiseamount = botChips
            raiseamount = int(raiseamount)
            com_raise(raiseamount, botChips)
        else:
            check_difference = abs(decision-1)
            fold_difference = abs(decision-2)
            x = min([check_difference, fold_difference])
            if x == check_difference:
                com_check()
            if x == fold_difference:
                com_fold()
    else:
        check_difference = abs(decision-1)
        fold_difference = abs(decision-2)
        call_difference = abs(decision-5)
        if playerallin:
            if min([call_difference, fold_difference]) == fold_difference:
                com_fold()
            if min([call_difference, fold_difference]) == call_difference:
                com_call()
        else:
            if (decision <= 4) and (decision > 3):
                raiseamount = (decision-3)*float(botChips)
                if raiseamount > 0.97*float(botChips):
                    raiseamount = botChips
                raiseamount = int(raiseamount)
                com_raise(raiseamount, botChips)
            else:
                if amount == None:
                    if min([check_difference, fold_difference]) == check_difference:
                        com_check()
                    if min([check_difference, fold_difference]) == fold_difference:
                        com_fold()
                else:
                    if min([call_difference, fold_difference]) == fold_difference:
                        com_fold()
                    if min([call_difference, fold_difference]) == call_difference:
                        com_call()

preflop_raw_data_inputs = [
    [[' A of clubs', 1], [' 4 of clubs', 4], 1, 65000, 3160000, 2775000, 3+(70000/2775000)],
    [[' 8 of clubs', 8], [' 7 of hearts', 7], 0, 90000, 2300000, 3610000, 0],
    [[' 8 of clubs', 8], [' 7 of hearts', 7], 0, 90000, 2300000, 3610000, 3+(300000/3610000)],
    [[' K of spades', 13], [' 2 of spades', 2], 1, 90000, 4675000, 1235000, 3+(90000/1235000)],
    [[' 8 of clubs', 8], [' 6 of spades', 6], 1, 90000, 4767000, 1145000, 3+(20000/1145000)],
    [[' 9 of clubs', 9], [' 6 of diamonds', 6], 0, 90000, 4990000, 920000, 0],
    [[' 7 of spades', 7], [' 7 of hearts', 7], 1, 105000, 4730000, 1165000, 3+(125000/1165000)]
]

flop_raw_data_inputs = [
    [[' A of clubs', 1], [' 4 of clubs', 4], [' 3 of hearts', 3], [' Q of diamonds', 12], [' Q of spades', 12], 160000, 3120000, 2720000, 0],
    [[' A of clubs', 1], [' 4 of clubs', 4], [' 3 of hearts', 3], [' Q of diamonds', 12], [' Q of spades', 12], 160000, 3120000, 2720000, 3+(60000/2720000)],
    [[' 8 of clubs', 8], [' 7 of hearts', 7], [' 8 of spades', 8], [' 6 of spades', 6], [' 6 of hearts', 6], 630000, 2050000, 3320000, 3+(40000/3320000)],
    [[' K of spades', 13], [' 2 of spades', 2], [' 2 of hearts', 2], [' 8 of diamonds', 8], [' 3 of hearts', 3], 210000, 4625000, 1165000, 0],
    [[' K of spades', 13], [' 2 of spades', 2], [' 2 of hearts', 2], [' 8 of diamonds', 8], [' 3 of hearts', 3], 210000, 4625000, 1165000, 3+(100000/1165000)],
    [[' 8 of clubs', 8], [' 6 of spades', 6], [' 7 of diamonds', 7], [' 2 of diamonds', 2], [' 8 of spades', 8], 210000, 4920000, 870000, 0],
    [[' 9 of clubs', 9], [' 6 of diamonds', 6], [' 8 of spades', 8], [' J of diamonds', 11], [' Q of diamonds', 12], 210000, 4920000, 870000, 0],
    [[' 9 of clubs', 9], [' 6 of diamonds', 6], [' 8 of spades', 8], [' J of diamonds', 11], [' Q of diamonds', 12], 210000, 4920000, 870000, 4],
    [[' 7 of spades', 7], [' 7 of hearts', 7], [' K of clubs', 13], [' 7 of diamonds', 7], [' 8 of diamonds', 8], 730000, 4430000, 840000, 0]
]

turn_raw_data_inputs = [
    [[' A of clubs', 1], [' 4 of clubs', 4], [' 3 of hearts', 3], [' Q of diamonds', 12], [' Q of spades', 12], [' 6 of hearts', 6], 480000, 2960000, 2560000, 0],
    [[' A of clubs', 1], [' 4 of clubs', 4], [' 3 of hearts', 3], [' Q of diamonds', 12], [' Q of spades', 12], [' 6 of hearts', 6], 480000, 2960000, 2560000, 3+(225000/2560000)],
    [[' K of spades', 13], [' 2 of spades', 2], [' 2 of hearts', 2], [' 8 of diamonds', 8], [' 3 of hearts', 3], [' 3 of spades', 3], 410000, 4525000, 1065000, 0],
    [[' K of spades', 13], [' 2 of spades', 2], [' 2 of hearts', 2], [' 8 of diamonds', 8], [' 3 of hearts', 3], [' 3 of spades', 3], 410000, 4525000, 1065000, 3+(250000/1065000)],
    [[' 8 of clubs', 8], [' 6 of spades', 6], [' 7 of diamonds', 7], [' 2 of diamonds', 2], [' 8 of spades', 8], [' 3 of diamonds', 3], 210000, 4715000, 1075000, 0],
    [[' 8 of clubs', 8], [' 6 of spades', 6], [' 7 of diamonds', 7], [' 2 of diamonds', 2], [' 8 of spades', 8], [' 3 of diamonds', 3], 210000, 4715000, 1075000, 3+(100000/1075000)],
    [[' 7 of spades', 7], [' 7 of hearts', 7], [' K of clubs', 13], [' 7 of diamonds', 7], [' 8 of diamonds', 8], [' 5 of spades', 5], 730000, 4430000, 840000, 0],
    [[' 7 of spades', 7], [' 7 of hearts', 7], [' K of clubs', 13], [' 7 of diamonds', 7], [' 8 of diamonds', 8], [' 5 of spades', 5], 730000, 4430000, 840000, 4]
]

river_raw_data_inputs = [
    [[' A of clubs', 1], [' 4 of clubs', 4], [' 3 of hearts', 3], [' Q of diamonds', 12], [' Q of spades', 12], [' 6 of hearts', 6], [' 8 of hearts', 8], 930000, 2735000, 2335000, 0],
    [[' A of clubs', 1], [' 4 of clubs', 4], [' 3 of hearts', 3], [' Q of diamonds', 12], [' Q of spades', 12], [' 6 of hearts', 6], [' 8 of hearts', 8], 930000, 2735000, 2335000, 3+(400000/2335000)],
    [[' K of spades', 13], [' 2 of spades', 2], [' 2 of hearts', 2], [' 8 of diamonds', 8], [' 3 of hearts', 3], [' 3 of spades', 3], [' 8 of hearts', 8], 910000, 4275000, 815000, 0],
    [[' K of spades', 13], [' 2 of spades', 2], [' 2 of hearts', 2], [' 8 of diamonds', 8], [' 3 of hearts', 3], [' 3 of spades', 3], [' 8 of hearts', 8], 910000, 4275000, 815000, 4],
    [[' 8 of clubs', 8], [' 6 of spades', 6], [' 7 of diamonds', 7], [' 2 of diamonds', 2], [' 8 of spades', 8], [' 3 of diamonds', 3], [' 6 of clubs', 6], 410000, 4615000, 975000, 0]
]

# TESTing
# botMove(currentinput, round, botChips, playerPreviousMove)
'''
for pf in preflop_raw_data_inputs:
    print(pf)
    print('bot\'s move: ')
    botMove(pf, 1, pf[4], pf[6])
    print('\n')'''

for f in flop_raw_data_inputs:
    print(f)
    print('bot\'s move: ')
    botMove(f, 2, f[6], f[8])
    print('\n')
'''
for t in turn_raw_data_inputs:
    print(t)
    print('bot\'s move: ')
    botMove(t, 3, t[7], t[9])
    print('\n')

for r in river_raw_data_inputs:
    print(r)
    print('bot\'s move: ')
    botMove(r, 4, r[8], r[10])
    print('\n')
'''
