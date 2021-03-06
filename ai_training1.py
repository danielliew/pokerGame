import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json


# bot model1: preflop bot

'''
data syntax:

inputs:
    card1
    card2
    currenthandstrength
    computer big blind?
    potbefore
    computerchips
    playerchips
    movebefore

output:
    decision

'''

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

def convertRawData(rawdata):

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

def convertOutputs(outputs):
    finalarray = []
    for i in outputs:
        finalarray.append(i/6)
    return numpy.array(finalarray)

raw_data_inputs = [
    [[' A of clubs', 1], [' 4 of clubs', 4], 1, 65000, 3160000, 2775000, 3+(70000/2775000)],
    [[' 8 of clubs', 8], [' 7 of hearts', 7], 0, 90000, 2300000, 3610000, 0],
    [[' 8 of clubs', 8], [' 7 of hearts', 7], 0, 90000, 2300000, 3610000, 3+(300000/3610000)],
    [[' K of spades', 13], [' 2 of spades', 2], 1, 90000, 4675000, 1235000, 3+(90000/1235000)],
    [[' 8 of clubs', 8], [' 6 of spades', 6], 1, 90000, 4767000, 1145000, 3+(20000/1145000)],
    [[' 9 of clubs', 9], [' 6 of diamonds', 6], 0, 90000, 4990000, 920000, 0],
    [[' 7 of spades', 7], [' 7 of hearts', 7], 1, 105000, 4730000, 1165000, 3+(125000/1165000)]
]

raw_data_outputs = [5, 3+(90000/3610000), 5, 5, 1, 3+(90000/4990000), 3+(350000/4730000)]

preflop_input_data = convertRawData(raw_data_inputs)

preflop_output_data = convertOutputs(raw_data_outputs)

print(preflop_input_data)
print(preflop_output_data)


# pf: abrv. of preflop
pf_model = Sequential()
pf_model.add(Dense(6, input_dim=8, kernel_initializer='normal', activation='relu'))
pf_model.add(Dense(4, kernel_initializer='normal', activation='relu'))
pf_model.add(Dense(1, kernel_initializer='normal', activation='sigmoid'))
pf_model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

# Fit the model
pf_model.fit(preflop_input_data, preflop_output_data, epochs=150, batch_size=2)
# evaluate the model
scores = pf_model.evaluate(preflop_input_data, preflop_output_data)
print("%s: %.2f%%" % (pf_model.metrics_names[1], scores[1]*100))

# serialize model to JSON
model_json = pf_model.to_json()
with open("/Users/daniel/Desktop/code/PokerGame/model1.json", "w+") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
pf_model.save_weights("/Users/daniel/Desktop/code/PokerGame/model1.h5")
print("Saved model to disk")

# load json and create model
json_file = open('/Users/daniel/Desktop/code/PokerGame/model1.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("/Users/daniel/Desktop/code/PokerGame/model1.h5")
print("Loaded model from disk")

# new instance where we do not know the answer
newinput = [
            [[' A of clubs', 1], [' 4 of clubs', 4], 1, 65000, 3160000, 2775000, 3+(70000/2775000)]
]
input_new = convertRawData(newinput)
# make a prediction
output_new = loaded_model.predict(input_new)
# show the inputs and predicted outputs
print("X=%s, Predicted=%s" % (input_new[0], output_new[0]))
