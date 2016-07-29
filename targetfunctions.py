## SongGenerator2016

'''
This file collects target functions, which are used by the song/array construction function to know which notes to aim
for (but the possible notes are limited by the chords in the chord being played at that time). 

My aim here is to not just use one target function, but blend together several different ones, like a sine function, 
a random walk, and markov chain

'''

import math
import random


def generateSine(length, coefficient, shift, mean, sigma): 
     
    # generates a list of y values
    y = []
    
    for x in range(length): 
     
        # We want it to range from 0 to 1 so we multiply it by 0.5 and add 0.5
        # then we want to center it around the mean value with a variation of sigma
        value = sigma * 0.5 * math.sin(coefficient * x + shift) + 0.5 + mean
        
        #raise ValueError(coefficient, shift, mean, sigma)
        
        roundedValue = int(round(value))
        
        y.append(roundedValue)
    
    return y
    
def generateRandomWalk(length, amplitude): 
    
    # generates a list of y values
    y = []
    
    for x in range(length): 
    
        z = 0

        if x > 0 :
            
            randomvar = random.randint(0,100)
             
            if randomvar < 10: 
                z = 1
            elif randomvar >= 10 and randomvar < 20: 
                z = 2
            elif randomvar >= 20 and randomvar < 30: 
                z = 3
            elif randomvar >= 30 and randomvar < 40: 
                z = 4
            elif randomvar >= 40 and randomvar < 50: 
                z = 5
            elif randomvar >= 50 and randomvar < 60: 
                z = -5
            elif randomvar >= 60 and randomvar < 70: 
                z = -4
            elif randomvar >= 70 and randomvar < 80: 
                z = -3
            elif randomvar >= 80 and randomvar < 90: 
                z = -2
            elif randomvar >= 90: 
                z = -1
            
            # We want to reverse direction if we hit the boundary though
        
            if y[x - 1] + z >= amplitude: 
                z = -3
            if y[x - 1] + z <= 0: 
                z = + 3
            
            y.append(y[x - 1] + z)
            
        else: 
            # Select a random starting point
            y.append(random.choice(range(amplitude)))
            
    return y
            
def blendTargetFunctions(song_length, coefficient, shift, mean, sigma, bias): 
    rw_values = generateRandomWalk(song_length, 127)
    sine_values = generateSine(song_length, coefficient, shift, mean, sigma)
    
    
    # returns a list of values which represent the blended functions
    mean_values = []
    
    for x in range(song_length): 
        rw_value = rw_values[x]
        sin_value = sine_values[x]
        
        # take the average of the target values
        mean_value = int(round(float(bias * rw_value + ( 1 - bias) * sin_value) / float(2)))
        
        mean_values.append(mean_value)
    
        
    return mean_values
        
    