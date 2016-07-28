''' See text file for concept. 

Pseudocode: 

1. Load and parse midi files, acquire note values for each beat in the song
2. Use these note values to create a series of vectors, each one representing the notes
played in each beat of the song. The values should be ordered in increasing order. 
3. Divide the values by 12 and obtain the remainders, this represents the chord 
4. Loop through all of the vectors for each song, adding values to the accumulation matrix 
(see text file for reference). 
5. Convert the accumulation matrix into a probability matrix by making all rows sum to 1. 
6. Create a function to generate a new song (series of chord vectors) using the 
probability/transformation matrix
7. Based on the chord vectors, generate note-value vectors like what we originally got
before dividing by 12. Depending on the user-specified number of channels (length of this vector),
instruments will pick out notes from the chord vector, with some multiple of 12 (bass instruments
will be more likely to pick lower multiples of 12). 
8. Combined with a randomly generated matrix for determining whether notes should be started
or stopped, generate a midi file with the note-value vectors, and play the song. 
9. Create a user interface for the user to manipulate starting seed chord, and percussive
pattern. 

'''

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

### import functions in separate files
from randomfunctions import *
from parsemidi import *
from createarray import *
from generatechordprogression import *
from generatepossiblenotes import *
from createmidi import *

'''
######################
TO DO

1. Figure out why new_song.mid is playing so fast. It may have something to do with track 4, since
everything else is basically the same it seems like, when you print_tracks(). length is different
for some reason

For now, I'm just going to manually adjust the tempo, can't figure this out

2. Make sure that repeated notes work correctly. The midi messages for the drum track of SMB theme
aren't matching up exactly when deconstructed into a matrix and reconstructed



NEXT

now that I can parse and create midi files, I just have to analyze them for patterns and develop
my probability matrices

######################
'''

'''
TO DO 07/26/2016

Add functionality for chorded instruments, which allows them to select more than one note at a time (I may
have to fix midi file creation, not sure if its set up to allow this)

Add chord progression under the pretty print array


'''


inport = mido.open_input(u'MidiMock OUT')
outport = mido.open_output()

def playMidi(mid): 

    for message in mid.play():
        outport.send(message)
        
def printMidiMessages(mid): 
    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        for message in track:
            print(message)

def Main(): 
    
    #midiSetup()
    #noteArray = parseMidi(MidiFile('midi/SmbTheme.mid'))
    noteArray = createArray()
    
    #printMidiMessages(MidiFile('midi/sm1castl.mid'))
    
    #prettyPrintArray(noteArray)
    createMidi(noteArray)
    
    mid = MidiFile('midi/new_song.mid')
    
    
    
    #print(MidiFile('midi/new_song.mid').length)
    #print(MidiFile('midi/new_song.mid').print_tracks())
    
    #printMidiMessages(MidiFile('midi/new_song.mid'))
    playMidi(mid)
    #playMidi(MidiFile('midi/Smbtheme.mid'))
    
    #print(noteArray)
    
    
    
    
Main()


'''

for i, track in enumerate(mid.tracks[1:]):
        
        trackLength = 0
        for message in track:
            trackLength = trackLength + message.time
        print(trackLength)

TESTING

mid = MidiFile('midi/ddstage.mid')
    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        for message in track:
            print(message)



mid = MidiFile('midi/Smbtheme.mid')

#mido.set_backend('mido.backends.rtmidi')
mido.set_backend('mido.backends.portmidi')
#portmidi = mido.Backend('mido.backends.portmidi')

#outport = mido.open_output('New Port')

#print mido.get_output_names()
print mido.get_input_names()

inport = mido.open_input(u'MidiMock OUT')

outport = mido.open_output()

print mido.get_output_names()


for message in mid.play():
    outport.send(message)
    
if j == 480 and i ==3: 
                    raise ValueError(currentNotes, prevNotes, timeSinceLastMessage)
                


#outport.send(mido.Message('note_on', note=60, velocity=100))

time.sleep(5)
'''




