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

def midiSetup(): 

    inport = mido.open_input(u'MidiMock OUT')
    outport = mido.open_output()


'''
This function will take a midi file and parse it into a 3D numpy Array, with the rows
representing MIDI tracks, the columns representing beats, and each value being a 1D
Array containing all the notes played on that track on that particular beat. 

Note: I'm increasing the standard note values here by 1, so that I can initialize a
matrix full of zeros, where zero means that no note is being played (rather than the
lowest C note, which will instead be represented by a note value of "1")

input parameter must be a mido midi object, MidiFile([filename])

'''
def parseMidi(mid): 

    # Exclude certain tracks from being parsed, such as percussion
    exclusions = ["Percussion"]
    
    
    # Initialize the note Array 
    noteArray = zeros((1,1,1), dtype=int)
        
    # First build the note Array vertically (one row for each track, excluding the one
    # track we already accounted for in initializing the array
    # go through the messages and add up all the delta times of the messages, so we can 
    # figure out the maximum track length in clicks. This will let us us know how
    # far to build out the array horizontally
    

    maxTrackLength = 0
    for i, track in enumerate(mid.tracks[2:]):
        
        trackLength = 0
        for message in track:
            trackLength = trackLength + message.time
            
        if trackLength > maxTrackLength: 
            maxTrackLength = trackLength
        
        noteArray = vstack((noteArray, [[[0]]]))

    # Build the array horizontally, by adding empty vertical vectors for the length
    # of the longest track
        
    emptyVector = zeros(noteArray.shape, dtype=int)
    
    for x in range(maxTrackLength): 
        noteArray = hstack((noteArray, emptyVector))
        
    prettyPrintArray(noteArray)
        
    '''
    for i, track in enumerate(mid.tracks[1:]):
    
        raise ValueError(len(track))
        #print 'Track {}: {}'.format(i, track.name)
        
        currentNotes = []
        
        if track.name not in exclusions: 
        
            for message in track:
            
                if message.type != "meta message":
                    
                    if message.type == "note_on": 
                                
                        currentNotes.append(message.note)
                    
                    elif message.type == "note_off": 
            
                        currentNotes.remove(message.note)
                        
                    if len(currentNotes) > 0:         
                        newNoteVector[i] = currentNotes
                        
                    noteArray = hstack((noteArray, newNoteVector))
                    newNoteVector = zeros(newNoteShape, dtype=int)
    '''
    #raise ValueError(noteArray.shape[1])            
    return noteArray
    
# Note: this is designed for 3D arrays, like for noteArray constructed in parseMidi
def prettyPrintArray(inputArray): 

    # in order to pretty print, we have to find the length of the i,jth entry, 
    # in terms of how many entries are in the list, and how many digits those
    # entries are
    
    #file = open("output.txt", "w")
    
    # Store the length of each i, jth entry in a matrix identical in size to the input matrix
    # then when we pretty print, we can pick the longest length in each column to space out
    # the entries
    
    lengthArray = zeros(inputArray.shape, dtype=int)
    
    # First fill in the values for the length array
    for i in range(inputArray.shape[0]): 
        for j in range(inputArray.shape[1]): 
            
            length = 0 
            for entry in inputArray[i][j]: 
                
                # account for the length of the comma and space separating entries in the list
                # (only applies after the first entry, when there are additional entries)
                if length > 0 : 
                    length = length + 2
                
                length = length + len(str(entry))
                
            lengthArray[i][j] = length
    
    
    
    # Then actually print the values of the input array using that length information
    
    # But first lets print a timeline that let's visually index the entries
    
    
    for j in range(inputArray.shape[1]): 
            
        print("t = " + str(j), end="")    
            
        # find max length over all entries in this column in the lengthArray
        maxLength = 0
        for k in range(lengthArray.shape[0]): 
           if lengthArray[k][j] > maxLength: 
                maxLength = lengthArray[k][j]
            
        # then utilize length information for the spacing between the entries
        lengthEntry = 4 + len(str(j))
        numSpaces = maxLength - lengthEntry + 8
            
        for x in range(numSpaces): 
            print(" ", end="")
    
    print("\n")         
            
    for i in range(inputArray.shape[0]): 
        for j in range(inputArray.shape[1]): 
            
            # first print the entry    
            print(inputArray[i][j], end="")
            
            
            # find max length over all entries in this column in the lengthArray
            maxLength = 0
            for k in range(lengthArray.shape[0]): 
                if lengthArray[k][j] > maxLength: 
                    maxLength = lengthArray[k][j]
            
            # then utilize length information for the spacing between the entries
            numSpaces = maxLength - lengthArray[i][j] + 6
            
            for x in range(numSpaces): 
                print(" ", end="")
            
        
        print("\n")        
        
    

def playMidi(mid): 

    for message in mid.play():
        outport.send(message)

def Main(): 
    
    midiSetup()
    noteArray = parseMidi(MidiFile('midi/Smbtheme.mid'))
    
    #print(noteArray)
    
    #prettyPrintArray(noteArray)
    
    
Main()


'''
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


#outport.send(mido.Message('note_on', note=60, velocity=100))

time.sleep(5)
'''




