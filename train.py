#!/usr/bin/env python

"""
For each song in songdata
    Download
    Analyze
    Delete
    Choose to use for training or testing
Train
Test
"""

# === IMPORTS ===
import collections
import json
import os
import threading
import time
import random
import librosa
import wget
from pydub import AudioSegment



# === CONSTANTS ===
sampleFileName = 'music/sample.mp3'
percentForTraining = 0.9
songs = []
genresSet = collections.defaultdict(int)


# === CLASSES ===
class Song:
    '''#Metadata
    title = ''
    length = ''
    artist = ''
    genres = []
    mood = ''
    download_link = ''
    #Role
    forTesting = True
    #Analysis
    pitchMeanEnergies = []
    tuning = 0
    tempo = 0'''

    def __init__(self, data):
        data[3] = data[3].split(' & ')
        if 'Country and Folk' in data[3] or 'Country Folk' in data[3]: data[3] = ['Country', 'Folk']
        for genre in data[3]:
            genresSet[genre] += 1
        if len(data) == 5:
            self.title = data[0]
            self.length = data[1]
            self.artist = data[2]
            self.genres = data[3]
            self.download_link = data[4]
        elif len(data) == 6:
            self.title = data[0]
            self.length = data[1]
            self.artist = data[2]
            self.genres = data[3]
            self.mood = data[4]
            self.download_link = data[5]
        self.analyze()
        self.assignRole()

    def __str__(self):
        return str(self.__dict__)

    def dict(self):
        return self.__dict__

    def calculate_tempo(self, y_percussive, sr):
        start = time.time()
        hop_length = 512 #Use a default hop size of 512 samples @ 22KHz ~= 23ms
        self.tempo = librosa.beat.beat_track(y=y_percussive, sr=sr, hop_length=hop_length)[0]  # beats = estimated tempo in bpm
        print('tempo',time.time()-start)

    def calculate_tuning_and_tones(self, y_harmonic, sr):
        start = time.time()
        self.tuning = librosa.estimate_tuning(y=y_harmonic, sr=sr).tolist()
        print('tuning',time.time()-start)
        start = time.time()
        chroma = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr, tuning=self.tuning)
        self.pitchMeanEnergies = []
        for pitch in chroma:
            self.pitchMeanEnergies += [sum(pitch)/len(pitch)]
        print('tones',time.time()-start)

    def analyze(self):
        print('Analyzing ' + self.title)
        start = time.time()
        wget.download(self.download_link, sampleFileName)
        print('Download:', time.time()-start)
        start = time.time()
        y, sr = librosa.load(AudioSegment.from_mp3(sampleFileName).export(sampleFileName + ".ogg", format="ogg"), sr=22050)
        print('Load:', time.time()-start)
        start = time.time()
        y_harmonic, y_percussive = librosa.effects.hpss(y)
        print('Split tracks:', time.time()-start)

        start = time.time()
        threads = [
            threading.Thread(target=self.calculate_tempo, args=(y_percussive, sr)),
            threading.Thread(target=self.calculate_tuning_and_tones, args=(y_harmonic, sr))
        ]
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]


        print('Analysis:', time.time()-start)

        file = open('songdata.json', 'a')
        file.write(json.dumps(self.__dict__, indent=4) + ',\n')
        file.close()
        os.remove(sampleFileName)

    def assignRole(self):
        self.forTesting = random.random() < percentForTraining


# === FUNCTIONS ===
def instantiateSongs():
    songDataBuffer = []
    for line in open('songdata.txt', 'r').readlines():
        if line == '\n':
            songs.append(Song(songDataBuffer))
            songDataBuffer = []
        else:
            songDataBuffer += [line.strip()]

def main():
    open('songdata.json', 'w+').close()
    instantiateSongs()

main()