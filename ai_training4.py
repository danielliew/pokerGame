import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json


# bot model4: river bot

'''
data syntax:

inputs:
    card1
    card2
    flop1
    flop2
    flop3
    turn
    river
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
        river = convertCard(i[6])
        totalinGameChips = i[7] + i[8] + i[9]
        potbefore = i[7]/totalinGameChips
        botschips = i[8]/totalinGameChips
        playerschips = i[9]/totalinGameChips
        movebefore = i[10]/6
        finalarray.append([card1, card2, flop1, flop2, flop3, turn, river, potbefore, botschips, playerschips, movebefore])
    return numpy.array(finalarray)

def convertOutputs(outputs):
    finalarray = []
    for i in outputs:
        finalarray.append(i/6)
    return numpy.array(finalarray)

raw_data_inputs = [
    [[' A of clubs', 1], [' 4 of clubs', 4], [' 3 of hearts', 3], [' Q of diamonds', 12], [' Q of spades', 12], [' 6 of hearts', 6], [' 8 of hearts', 8], 930000, 2735000, 2335000, 0],
    [[' A of clubs', 1], [' 4 of clubs', 4], [' 3 of hearts', 3], [' Q of diamonds', 12], [' Q of spades', 12], [' 6 of hearts', 6], [' 8 of hearts', 8], 930000, 2735000, 2335000, 3+(400000/2335000)],
    [[' K of spades', 13], [' 2 of spades', 2], [' 2 of hearts', 2], [' 8 of diamonds', 8], [' 3 of hearts', 3], [' 3 of spades', 3], [' 8 of hearts', 8], 910000, 4275000, 815000, 0],
    [[' K of spades', 13], [' 2 of spades', 2], [' 2 of hearts', 2], [' 8 of diamonds', 8], [' 3 of hearts', 3], [' 3 of spades', 3], [' 8 of hearts', 8], 910000, 4275000, 815000, 4],
    [[' 8 of clubs', 8], [' 6 of spades', 6], [' 7 of diamonds', 7], [' 2 of diamonds', 2], [' 8 of spades', 8], [' 3 of diamonds', 3], [' 6 of clubs', 6], 410000, 4615000, 975000, 0]
]

raw_data_outputs = [1,5,1,2,1]

river_input_data = convertRawData(raw_data_inputs)

river_output_data = convertOutputs(raw_data_outputs)

print(river_input_data)
print(river_output_data)

seed = numpy.random.randint(10)
numpy.random.seed(seed)

# r: abrv. of river
r_model = Sequential()
r_model.add(Dense(9, input_dim=11, kernel_initializer='normal', activation='relu'))
r_model.add(Dense(7, kernel_initializer='normal', activation='relu'))
r_model.add(Dense(1, kernel_initializer='normal', activation='sigmoid'))
r_model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

# Fit the model
r_model.fit(river_input_data, river_output_data, epochs=150, batch_size=2)
# evaluate the model
scores = r_model.evaluate(river_input_data, river_output_data)
print("%s: %.2f%%" % (r_model.metrics_names[1], scores[1]*100))

# serialize model to JSON
model_json = r_model.to_json()
with open("/Users/daniel/Desktop/code/PokerGame/model4.json", "w+") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
r_model.save_weights("/Users/daniel/Desktop/code/PokerGame/model4.h5")
print("Saved model to disk")

# load json and create model
json_file = open('/Users/daniel/Desktop/code/PokerGame/model4.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("/Users/daniel/Desktop/code/PokerGame/model4.h5")
print("Loaded model from disk")

# evaluate loaded model on test data
loaded_model.compile(loss='mean_squared_error', optimizer='rmsprop', metrics=['accuracy'])
score = loaded_model.evaluate(river_input_data, river_output_data, verbose=0)
print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))

# new instance where we do not know the answer
newinput = [
            [[' A of clubs', 1], [' 4 of clubs', 4], [' 3 of hearts', 3], [' Q of diamonds', 12], [' Q of spades', 12], [' 6 of hearts', 6], [' 8 of hearts', 8], 930000, 2735000, 2335000, 3+(40000/233500)]
]
input_new = convertRawData(newinput)
# make a prediction
output_new = loaded_model.predict(input_new)
# show the inputs and predicted outputs
print("X=%s, Predicted=%s" % (input_new[0], output_new[0]))
