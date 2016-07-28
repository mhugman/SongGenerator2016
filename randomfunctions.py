'''
SongGenerator2016

File for random functions
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

'''
def nCk(n,k): 
    return int( reduce(mul, (Fraction(n-i, i+1) for i in range(k)), 1) )
'''

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
    
# goes through a list of integers and finds the value which is closest to a target value
def closestToTarget(list, target): 
    
    closest = ( list[0] , max(list) - min(list) )
    for x in list: 
        if abs(x - target) < closest[1] : 
            closest = ( x, abs(x - target))
    
    return closest[0]
    
        

