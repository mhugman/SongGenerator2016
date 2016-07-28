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

def createMidi(inputArray):

    '''
    This function will take a 3D numpy note Array (e.g. parsed from a midi file), and turn it into 
    a midi file which can be played back. 
    '''
    # Smb theme
    TEMPO = 571428 * 5
    # Smb underwater
    #TEMPO = 272727 * 5
    # Smb castle
    #TEMPO = 666666

    with MidiFile() as mid:
    
        # add an empty first track (for testing)
    
        mid.add_track(name= str(0))
        track = mid.tracks[0]
            
        track.append(MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=96, notated_32nd_notes_per_beat=8, time=0))
        track.append(MetaMessage('set_tempo', tempo=TEMPO, time=0))
    
        for i in range(inputArray.shape[0]): 
            
            mid.add_track(name= str(i + 1))
            track = mid.tracks[i + 1]
            
            track.append(Message('control_change', channel = i, control=0, value=0, time=0))
            track.append(Message('program_change', channel = i, program=26, time=0))
            track.append(MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=96, notated_32nd_notes_per_beat=8, time=0))
            track.append(MetaMessage('set_tempo', tempo=TEMPO, time=0))
            
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
