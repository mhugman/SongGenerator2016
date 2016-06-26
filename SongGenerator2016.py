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

'''
######################
TO DO

Figure out why new_song.mid is playing so fast. It may have something to do with track 4, since
everything else is basically the same it seems like, when you print_tracks(). length is different
for some reason

NEXT

now that I can parse and create midi files, I just have to analyze them for patterns and develop
my probability matrices

######################
'''

inport = mido.open_input(u'MidiMock OUT')
outport = mido.open_output()

def unique(a):
    """ return the list with duplicate elements removed """
    return list(set(a))

def intersect(a, b):
    """ return the intersection of two lists """
    return list(set(a) & set(b))

def union(a, b):
    """ return the union of two lists """
    return list(set(a) | set(b))

def midiSetup(): 

    inport = mido.open_input(u'MidiMock OUT')
    outport = mido.open_output()

# returns the union of two 2d numpy arrays
def union2d(A,B): 
    union = []
    for a in A: 
        union.append(a)
    for b in B: 
        if b not in A: 
            union.append(b)
    return union
        


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
    exclusions = []
    
    
    # Initialize the note Array 
    noteArray = zeros((1,1,1), dtype=(int,3))
        
    # First build the note Array vertically (one row for each track, excluding the one
    # track we already accounted for in initializing the array
    # go through the messages and add up all the delta times of the messages, so we can 
    # figure out the maximum track length in clicks. This will let us us know how
    # far to build out the array horizontally
    
    maxTrackLength = 0
    for i, track in enumerate(mid.tracks[1:]):
        
        trackLength = 0
        for message in track:
            trackLength = trackLength + message.time
            
        if trackLength > maxTrackLength: 
            maxTrackLength = trackLength
        if i > 0: 
            noteArray = vstack((noteArray, [[[(0,0,0)]]]))
            
    #raise ValueError(noteArray)
            
    #prettyPrintArray(noteArray)
    
    # Build the array horizontally, by adding empty vertical vectors for the length
    # of the longest track
        
    emptyVector = zeros((noteArray.shape[0],1,1), dtype=(int,3))
    
    #raise ValueError(maxTrackLength)
    
    for x in range(maxTrackLength): 
        noteArray = hstack((noteArray, emptyVector))
    
    #print(noteArray.shape)   
    #prettyPrintArray(noteArray)
        
    
    for i, track in enumerate(mid.tracks[1:]):
    
        #print 'Track {}: {}'.format(i, track.name)
        
        currentNotes = []
        
        if track.name not in exclusions: 
            
            currentTime = 0
            for message in track:
                
                if message.type == "note_on" or message.type == "note_off":
                    prevTime = currentTime
                    currentTime = currentTime + message.time
                    
                    # previous notes are the same as (not yet updated) current notes, 
                    # but the third value is 0 instead of 1 (denoting the fact that 
                    # the note is sustained, rather than hit)
                    prevNotes = []
                    for x in currentNotes: 
                         prevNotes.append((x[0], x[1], 0))
                    
                    # Fill in all the values since the previous message, and up to 
                    # but not including the time of the current message, with the
                    # previous notes
                    if len(prevNotes) > 0:     
                        deltaTime = currentTime - prevTime
                        for j in range(0, deltaTime - 1):     
                            noteArray[i][currentTime - 1 - j] = prevNotes
                    
                    # update the current Notes being played with the information in the
                    # message
                    if message.type == "note_on": 
                                
                        currentNotes.append((message.note + 1, message.velocity,1))
                    
                    elif message.type == "note_off": 
                        for x in currentNotes: 
                            if x[0] == message.note + 1: 
                                 currentNotes.remove(x)
                        #currentNotes.remove((message.note + 1, message.velocity))   
                     
                    # fill in the value for this particular time with the current Notes
                    if len(currentNotes) > 0:     
                        noteArray[i][currentTime] = asarray(currentNotes)
                        
    
    #raise ValueError(noteArray.shape[1])            
    return noteArray

'''
This function will take a 3D numpy note Array (e.g. parsed from a midi file), and turn it into 
a midi file which can be played back. 
'''
def createMidi(inputArray):

    with MidiFile() as mid:
    
        # add an empty first track (for testing)
    
        mid.add_track(name= str(0))
        track = mid.tracks[0]
            
        track.append(MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=96, notated_32nd_notes_per_beat=8, time=0))
        track.append(MetaMessage('set_tempo', tempo=571428, time=0))
    
        for i in range(inputArray.shape[0]): 
            
            mid.add_track(name= str(i + 1))
            track = mid.tracks[i + 1]
            
            track.append(Message('control_change', channel = i, control=0, value=0, time=0))
            track.append(Message('program_change', channel = i, program=26, time=0))
            track.append(MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=96, notated_32nd_notes_per_beat=8, time=0))
            track.append(MetaMessage('set_tempo', tempo=571428, time=0))
            
            currentNotes = asarray([(0,0,0)])
            
            timeSinceLastMessage = 0
            for j in range(inputArray.shape[1]):
                
                # previous notes are the same as (not yet updated) current notes, 
                # but the third value is 0 instead of 1 (denoting the fact that 
                # the note is sustained, rather than hit)
                prevNotesList = []
                for x in currentNotes: 
                    prevNotesList.append((x[0], x[1], 0))
                prevNotes = asarray(prevNotesList)
                currentNotes = inputArray[i][j]
                currentNoteValues = [x[0] for x in currentNotes]
                prevNoteValues = [x[0] for x in prevNotes]
                
                
                # Generate a note_off message if the note is in prevNotes but not in currentNotes. 
                # Generate a note_on message if the third value of the note is 1 (this represents note on)          
                messageGenerated = False
                for n in union2d(prevNotes, currentNotes): 
                    # if the first note value is 0 don't play it, that represents silence
                    # send a note_on  message if the third note value is 1
                    if n[2] == 1 and n[0] != 0: 
                        
                        # remember that we added 1 to the value of the note to store it in the 
                        # array, so to play it back, subtract 1
                        noteValue = n[0] - 1
                        noteVelocity = n[1]
                        
                        track.append(Message('note_on', channel = i, note= noteValue, velocity=noteVelocity, time=timeSinceLastMessage))
                        messageGenerated = True
                    # send a note_off message if the note is no longer being played
                    elif n[0] not in currentNoteValues and n[0] != 0: 
                        
                        track.append(Message('note_off', channel = i, note= noteValue, velocity=noteVelocity, time=timeSinceLastMessage))
                        messageGenerated = True
                    # send a note_off message if the note we just turned on was the same as a note already
                    # being played (a repeat note)
                    elif n[2] == 1 and n[0] in prevNoteValues and n[0] != 0: 
                        track.append(Message('note_off', channel = i, note= noteValue, velocity=noteVelocity, time=timeSinceLastMessage))
                        messageGenerated = True
                # if a message was generated (either note_on or note_off), then reset the time
                # since last message to 0
                if messageGenerated == True: 
                    # the value here resets to 1 instead of 0, because its been at least one tick 
                    # since the last message
                    timeSinceLastMessage = 1
                else: 
                    # if there was no message, simply increment the time since the last message
                    timeSinceLastMessage = timeSinceLastMessage + 1

        mid.save('midi/new_song.mid')

    
# Note: this is designed for 3D arrays, like for noteArray constructed in parseMidi
def prettyPrintArray(inputArray): 

    # in order to pretty print, we have to find the length of the i,jth entry, 
    # in terms of how many entries are in the list, and how many digits those
    # entries are
    
    #file = open("output.txt", "w")
    
    # Store the length of each i, jth entry in a matrix identical in size to the input matrix
    # then when we pretty print, we can pick the longest length in each column to space out
    # the entries
    
    lengthArray = zeros((inputArray.shape[0], inputArray.shape[1]), dtype=int)
    
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
    
    #raise ValueError(lengthArray)
    
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
        
def printMidiMessages(mid): 
    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        for message in track:
            print(message)

def Main(): 
    
    #midiSetup()
    noteArray = parseMidi(MidiFile('midi/Smbtheme.mid'))
    
    #prettyPrintArray(noteArray)
    createMidi(noteArray)
    
    mid = MidiFile('midi/new_song.mid')
    
    
    
    #print(MidiFile('midi/new_song.mid').length)
    print(MidiFile('midi/new_song.mid').print_tracks())
    
    #printMidiMessages(MidiFile('midi/new_song.mid'))
    #playMidi(mid)
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




