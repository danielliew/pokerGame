import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json


# bot model3: turn bot

'''
data syntax:

inputs:
    card1
    card2
    flop1
    flop2
    flop3
    turn
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

def convertRawData(rawdata):

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

def convertOutputs(outputs):
    finalarray = []
    for i in outputs:
        finalarray.append(i/6)
    return numpy.array(finalarray)

raw_data_inputs = [
    [[' A of clubs', 1], [' 4 of clubs', 4], [' 3 of hearts', 3], [' Q of diamonds', 12], [' Q of spades', 12], [' 6 of hearts', 6], 480000, 2960000, 2560000, 0],
    [[' A of clubs', 1], [' 4 of clubs', 4], [' 3 of hearts', 3], [' Q of diamonds', 12], [' Q of spades', 12], [' 6 of hearts', 6], 480000, 2960000, 2560000, 3+(225000/2560000)],
    [[' K of spades', 13], [' 2 of spades', 2], [' 2 of hearts', 2], [' 8 of diamonds', 8], [' 3 of hearts', 3], [' 3 of spades', 3], 410000, 4525000, 1065000, 0],
    [[' K of spades', 13], [' 2 of spades', 2], [' 2 of hearts', 2], [' 8 of diamonds', 8], [' 3 of hearts', 3], [' 3 of spades', 3], 410000, 4525000, 1065000, 3+(250000/1065000)],
    [[' 8 of clubs', 8], [' 6 of spades', 6], [' 7 of diamonds', 7], [' 2 of diamonds', 2], [' 8 of spades', 8], [' 3 of diamonds', 3], 210000, 4715000, 1075000, 0],
    [[' 8 of clubs', 8], [' 6 of spades', 6], [' 7 of diamonds', 7], [' 2 of diamonds', 2], [' 8 of spades', 8], [' 3 of diamonds', 3], 210000, 4715000, 1075000, 3+(100000/1075000)],
    [[' 7 of spades', 7], [' 7 of hearts', 7], [' K of clubs', 13], [' 7 of diamonds', 7], [' 8 of diamonds', 8], [' 5 of spades', 5], 730000, 4430000, 840000, 0],
    [[' 7 of spades', 7], [' 7 of hearts', 7], [' K of clubs', 13], [' 7 of diamonds', 7], [' 8 of diamonds', 8], [' 5 of spades', 5], 730000, 4430000, 840000, 4]
]

raw_data_outputs = [1, 5, 1, 5, 1, 5, 3+(375000/4430000), 5]

turn_input_data = convertRawData(raw_data_inputs)

turn_output_data = convertOutputs(raw_data_outputs)

print(turn_input_data)
print(turn_output_data)

seed = numpy.random.randint(10)
numpy.random.seed(seed)

# t: abrv. of turn
t_model = Sequential()
t_model.add(Dense(8, input_dim=10, kernel_initializer='normal', activation='relu'))
t_model.add(Dense(6, kernel_initializer='normal', activation='relu'))
t_model.add(Dense(1, kernel_initializer='normal', activation='sigmoid'))
t_model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

# Fit the model
t_model.fit(turn_input_data, turn_output_data, epochs=150, batch_size=2)
# evaluate the model
scores = t_model.evaluate(turn_input_data, turn_output_data)
print("%s: %.2f%%" % (t_model.metrics_names[1], scores[1]*100))

# serialize model to JSON
model_json = t_model.to_json()
with open("/Users/daniel/Desktop/code/PokerGame/model3.json", "w+") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
t_model.save_weights("/Users/daniel/Desktop/code/PokerGame/model3.h5")
print("Saved model to disk")

# load json and create model
json_file = open('/Users/daniel/Desktop/code/PokerGame/model3.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("/Users/daniel/Desktop/code/PokerGame/model3.h5")
print("Loaded model from disk")

# evaluate loaded model on test data
loaded_model.compile(loss='mean_squared_error', optimizer='rmsprop', metrics=['accuracy'])
score = loaded_model.evaluate(turn_input_data, turn_output_data, verbose=0)
print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
