
'''
This function will take a midi file and parse it into a 3D numpy Array, with the rows
representing MIDI tracks, the columns representing beats, and each value being a 1D
Array containing all the notes played on that track on that particular beat. 

Note: I'm increasing the standard note values here by 1, so that I can initialize a
matrix full of zeros, where zero means that no note is being played (rather than the
lowest C note, which will instead be represented by a note value of "1")

input parameter must be a mido midi object, MidiFile([filename])

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

from randomfunctions import *

def parseMidi(mid): 

    # Exclude certain tracks from being parsed, such as percussion
    exclusions = ["Percussion"]
    
    
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
                        try:  
                            noteArray[i][currentTime] = asarray(currentNotes)
                        except: 
                            raise ValueError(message, i, currentTime, currentNotes)
                        
    
    #raise ValueError(noteArray.shape[1])            
    return noteArray