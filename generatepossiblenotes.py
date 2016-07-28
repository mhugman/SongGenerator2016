
### SongGenerator2016

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
    
def generatePossibleNotes(chord):
    '''
    Generates a set of possible notes from a given chord, using its structure
    '''
    
    
    
    root = chord["root"]
    additional_notes = chord["notes"]
    
    baseNotes = [root ]
    
    for n in additional_notes: 
        note = root + n
        baseNotes.append(note)
    
    # keep adding multiples of the base notes to all the possible notes up to the highest 127    
    multiple = 1
    
    possibleNotes = baseNotes[:]
    
    end = False
    y = 0
    while end == False: 
    
        noteMultiples = []
        for n in baseNotes: 
            noteMultiple = n + multiple * 12
            if noteMultiple <= 127: 
                noteMultiples.append(noteMultiple)
        # if no multiples were added to the list, all the values are over 127 and we should stop
        if len(noteMultiples) > 0: 
            for m in noteMultiples: 
                possibleNotes.append(m)
        else: 
            end = True
            
        #raise ValueError(root, additional_notes, baseNotes, possibleNotes)
        #print(root, additional_notes, baseNotes, possibleNotes)
        y = y + 1
        multiple = multiple + 1
        
    
    return possibleNotes
        
        