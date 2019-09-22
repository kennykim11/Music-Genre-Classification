#!/usr/bin/env python
'''
CREATED:2013-02-11 18:37:30 by Brian McFee <brm2132@columbia.edu>
Track beat events in an audio file
Usage:   ./beat_tracker.py [-h] input_file.mp3    output_beats.csv
'''
from __future__ import print_function

import argparse
import sys
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import wget


def beat_track(input_file):
    # === LOADING ===
    print('Loading ', input_file)
    y, sr = librosa.load(input_file, sr=22050)
    y_harmonic, y_percussive = librosa.effects.hpss(y)

    # Use a default hop size of 512 samples @ 22KHz ~= 23ms
    hop_length = 512

    # This is the window length used by default in stft
    print('Tracking beats')
    tempo, beats = librosa.beat.beat_track(y=y_percussive, sr=sr, hop_length=hop_length)

    print('Estimated tempo: {:0.2f} beats per minute'.format(tempo))


    # === TEMPO ===
    # 'beats' will contain the frame numbers of beat events.
    beat_times = librosa.frames_to_time(beats, sr=sr, hop_length=hop_length)
    print(tempo)
    print(beats)
    print(beat_times)


    # === TUNING ===

    print('Estimating tuning ... ')
    # Just track the pitches associated with high magnitude
    tuning = librosa.estimate_tuning(y=y_harmonic, sr=sr)
    print(tuning)

    print('{:+0.2f} cents'.format(100 * tuning))


    # === NOTES ===
    chroma = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr, tuning=tuning)

    #My first code!
    pitchesMeanEnergy = []
    for pitch in chroma:
        pitchesMeanEnergy += [sum(pitch)/len(pitch)]
    print(pitchesMeanEnergy)

beat_track(librosa.util.example_audio_file())