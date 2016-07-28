
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
from generatechordprogression import *
from generatepossiblenotes import *

def createArray(): 
    '''
    This function will create a note array from scratch, without input from a midi file like the parseMidi function
    '''
    
    #### TWEAKABLE PARAMETERS ####
    
    num_tracks = 3
    
    # trackShift determines how much to shift the sine function horizontally
    trackShift = {
    
        0: int(round(random.normalvariate(500,50))), 
        1: int(round(random.normalvariate(500,50))), 
        2: int(round(random.normalvariate(500,50)))
    }
    
    # trackMod determines how much to stretch the sine function horizontally
    trackMod = {
    
        0: round(random.normalvariate(0.01,0.002), 3), 
        1: round(random.normalvariate(0.01,0.002), 3), 
        2: round(random.normalvariate(0.01,0.002), 3)
    }
    
    
    song_length = int(round(random.normalvariate(7000,500)))
    if song_length < 100: 
        song_length = 100
    
    silenceProb = random.randint(0,50)  # Should be between 0 and 100 (percent)
    
    
    ##################
     
    notes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    # mode is which note is the tonal center
    modes = [ 1, 2, 3, 4, 5, 6, 7]
    
    key = random.choice(notes)
    mode = random.choice(modes)
    
    # Specify which tracks are bass, mid, and treble to control their likely range of notes
    trackVoices = {
        0 : "bass", 
        1 : "mid", 
        2 : "treble"
    
    }
    
    # Initialize the note Array 
    noteArray = zeros((1,1,1), dtype=(int,3))
    
    # Build array vertically
    for i in range(num_tracks): 
        noteArray = vstack((noteArray, [[[(0,0,0)]]]))
    
    # Build the array horizontally
    emptyVector = zeros((noteArray.shape[0],1,1), dtype=(int,3))
    
    for x in range(song_length): 
        noteArray = hstack((noteArray, emptyVector))
        
    chordProgression = generateChordProgression(key, mode)
    print(key, chordProgression)
    
    for track in range(num_tracks): 
    
        
    
        # i tracks where we are in the chord progression
        i = 0
        # j tracks how long we've been playing the chord
        j = 0
        # k tracks how long we've been playing a note
        k = 0
        
        # Initialize the first note we're gonna play before entering the loop
        currentChord = chordProgression[0]
        possibleNotes = generatePossibleNotes(currentChord)
        currentNotes = [(random.choice(possibleNotes) + 1,random.randint(0,127) ,1)]
        noteLength = 1 + random.randint(0, currentChord["length"] - 1)
        noteArray[track][0] = asarray(currentNotes)
        
        silence = False
        
        for t in range(1,song_length): 
    
            # previous notes are the same as (not yet updated) current notes, 
            # but the third value is 0 instead of 1 (denoting the fact that 
            # the note is sustained, rather than hit)
            prevNotes = []
            for x in currentNotes: 
                prevNotes.append((x[0], x[1], 0))
        
            
        
            # if we've played the chord for its full length, switch to the next chord
            if j > currentChord["length"]: 
                i = i + 1
                if i < len(chordProgression): 
                    currentChord = chordProgression[i]
                else: 
                    i = 0
                    currentChord = chordProgression[i]
                j = 0
        
            possibleNotes = generatePossibleNotes(currentChord)
            
            ### Modification 1: instead of picking notes randomly from possible notes, use
            ### a sine function and pick notes closest to that
            
            # Add a modifier to the targetnote mean based on the voice (bass, mid, treble) 
            # of the track
            
            if trackVoices[track] == "bass" : 
                modifier = 30 * 0.75
            elif trackVoices[track] == "mid" :
                modifier = 60 * 0.75
            elif trackVoices[track] == "treble" :
                modifier = 90 * 0.75
            
            targetNoteMean = (math.sin(trackMod[track] * t - trackShift[track] * track) + 1) * modifier
            targetNoteSigma = 5
            
            targetNote = random.normalvariate(targetNoteMean, targetNoteSigma)
            
            #print(targetNote)
            
            closestNote = closestToTarget(possibleNotes, targetNote)
            
            # Lets also make the velocity normally distributed around the center
            
            velocity = random.normalvariate(62, 10)
            
            # adjust for the hard bounds of 0 and 127
            
            if velocity > 127: 
                velocity = 127
            if velocity < 0: 
                velocity = 0
                
            # let's also play silence with some probability (it also has a length designated by "noteLength")
            
            if random.randint(1,100) < silenceProb: 
                silence = True
            else: 
                silence = False
        
            if k > noteLength and silence == False: 
                currentNotes = [(closestNote + 1,random.randint(0,127) ,1)]
                noteLength = int(round(random.normalvariate((currentChord["length"] - j)/2,currentChord["length"] * 0.2))) 
                
                # take into account the hard bounds of 1 and chordLength - j
                if noteLength < 1: 
                    noteLength = 1
                if noteLength > currentChord["length"] - j: 
                    noteLength = currentChord["length"] - j
                
                #noteLength = 1 + random.randint(0, currentChord["length"] - j)
                k = 0
            elif k > noteLength and silence == True: 
                currentNotes = [(0,random.randint(0,127) ,1)]
                noteLength = 1 + random.randint(0, currentChord["length"] - j)
                k = 0
            else: 
                currentNotes = prevNotes
            
            #raise ValueError(noteArray)
            try: 
                noteArray[track][t] = asarray(currentNotes)
            except: 
                raise ValueError(track, t, currentNotes)
            
            
        
            j = j + 1
            k = k + 1
            
            
    return noteArray