import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json


# bot model2: flop bot

'''
data syntax:

inputs:
    card1
    card2
    flop1
    flop2
    flop3
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
        totalinGameChips = i[5] + i[6] + i[7]
        potbefore = i[5]/totalinGameChips
        botschips = i[6]/totalinGameChips
        playerschips = i[7]/totalinGameChips
        movebefore = i[8]/6
        finalarray.append([card1, card2, flop1, flop2, flop3, potbefore, botschips, playerschips, movebefore])
    return numpy.array(finalarray)

def convertOutputs(outputs):
    finalarray = []
    for i in outputs:
        finalarray.append(i/6)
    return numpy.array(finalarray)

raw_data_inputs = [
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

raw_data_outputs = [4, 3+(160000/3120000), 4, 3.5, 5, 3+(50000/4765000), 3+(125000/4920000), 2, 3.5]

flop_input_data = convertRawData(raw_data_inputs)

flop_output_data = convertOutputs(raw_data_outputs)

print(flop_input_data)
print(flop_output_data)

seed = numpy.random.randint(10)
numpy.random.seed(seed)

# f: abrv. of flop
f_model = Sequential()
f_model.add(Dense(8, input_dim=9, kernel_initializer='normal', activation='relu'))
f_model.add(Dense(6, kernel_initializer='normal', activation='relu'))
f_model.add(Dense(1, kernel_initializer='normal', activation='tanh'))
f_model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

# Fit the model
f_model.fit(flop_input_data, flop_output_data, epochs=150, batch_size=2)
# evaluate the model
scores = f_model.evaluate(flop_input_data, flop_output_data)
print("%s: %.2f%%" % (f_model.metrics_names[1], scores[1]*100))

# serialize model to JSON
model_json = f_model.to_json()
with open("/Users/daniel/Desktop/code/PokerGame/model2.json", "w+") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
f_model.save_weights("/Users/daniel/Desktop/code/PokerGame/model2.h5")
print("Saved model to disk")

# load json and create model
json_file = open('/Users/daniel/Desktop/code/PokerGame/model2.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("/Users/daniel/Desktop/code/PokerGame/model2.h5")
print("Loaded model from disk")

# evaluate loaded model on test data
loaded_model.compile(loss='mean_squared_error', optimizer='rmsprop', metrics=['accuracy'])
score = loaded_model.evaluate(flop_input_data, flop_output_data, verbose=0)
print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
