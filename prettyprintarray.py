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