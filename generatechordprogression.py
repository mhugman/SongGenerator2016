### Song Generator 2016

from __future__ import print_function

import mido
#import sys
import time
import numpy
from numpy import *
from mido import MidiFile
from mido.midifiles import MidiTrack
from mido import MetaMessage
from mido import Message
import math
#from operator import mul    # or mul=lambda x,y:x*y
#from fractions import Fraction
import random

from randomfunctions import *

def generateChordProgression(key, mode): 

    '''
    Generates a chord progression, with the data structure: 
    [ {"root" : r, "notes" : [...], "length" : l}, {...}, ... {...} ]
    
    where the root is one of the 12 possible tones, and the notes are all the additional notes
    stacked onto it. E.g. a standard major chord is 1,3,5, and if the root is 4, then the chord
    will have the notes 4, 4 + 3, 4 + 5 = 4, 7, 9
    
    '''
    
    # note 0 corresponds with a C
    notes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    noteSteps = [2, 2, 1, 2, 2, 2]
    
    # Generate the (base) notes in the key, this will be used for the roots of the chord progression
    notesInKey = [key]
    
    prevNote = key
    for n in noteSteps: 
        
        nextNote = prevNote + n
        notesInKey.append(nextNote)
        
        prevNote = nextNote
        
    for n in range(len(notesInKey)): 
        notesInKey[n] = notesInKey[n] % 12
        
    
    numChords = random.randint(2,5)
    
    
    chordProgression = []
    
    rootProgression = []
    for n in range(numChords): 
        root = random.choice(notesInKey)
        rootProgression.append(root)
    
    chordList = []
    
    for r in rootProgression: 
    
        chordSize = random.randint(3,5)
    
        chordNotes = random.sample(notes[1:], chordSize - 1)
        
        chordLength = int(round(random.normalvariate(60,20))) 
        
        if chordLength < 1: 
            chordLength = 1
        
        chord = {"root" : r, "notes" : chordNotes, "length" : chordLength}
        
        chordProgression.append(chord)
        
    return chordProgression