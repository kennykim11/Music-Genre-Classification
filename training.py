
#https://machinelearningmastery.com/tutorial-first-neural-network-python-keras/

# === IMPORTS ===
from keras.models import Sequential
from keras.layers import Dense
import json
import time
import random

# === CONSTANTS ===
genres = ['Pop', 'Dance', 'Electronic', 'Ambient', 'Country', 'Folk', 'Cinematic', 'R&B', 'Soul', 'Hip Hop', 'Rap',
          'Classical', 'Holiday', 'Jazz', 'Blues', "Children's", 'Rock', 'Alternative', 'Punk', 'World', 'Reggae']
training_chances = 0.9

# === FUNCTIONS ===
def get_length_in_seconds(string):
    minu, seco = string.split(':')
    return (int(minu)*60) + int(seco)

def get_genre_answer(listed_genres):
    concl = []
    for genre in genres:
        concl += [1] if genre in listed_genres else [0]
    return concl

print(get_length_in_seconds('5:20'))

time.sleep(3)

# load the dataset
dataset = json.loads(open('trialdata.json', 'r').read())
# split into input (X) and output (y) variables
X_training = []
X_testing = []
Y_training = []
Y_testing = []
for song in dataset:
    if random.random() < training_chances:
        X_training += song['pitchMeanEnergies']+[song['tempo']]+[song['tuning']]+[get_length_in_seconds(song['length'])]
        Y_training += get_genre_answer(song['genres'])
    else:
        X_testing += song['pitchMeanEnergies']+[song['tempo']]+[song['tuning']]+[get_length_in_seconds(song['length'])]
        Y_testing += get_genre_answer(song['genres'])
print(len(X_training), len(X_testing))

# define the keras model
model = Sequential()
model.add(Dense(12, input_dim=8, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
# compile the keras model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# fit the keras model on the dataset
model.fit(X_training, Y_training, epochs=150, batch_size=10)
# evaluate the keras model
_, accuracy = model.evaluate(X_testing, Y_testing)
print('Accuracy: %.2f' % (accuracy*100))