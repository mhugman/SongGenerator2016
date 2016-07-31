# SongGenerator2016

# Given a vector (list) of y values, and song length, will plot the target note function and the closest notes
# selected, highlighting the possible notes given the current chord in the chord progression

import matplotlib.pyplot as plt

def plotNotes(song_length, num_tracks, trackTargetNotes, trackClosestNotes): 
    
    trackColors = {
        0: ["b-", "c-"],
        1: ["y-", "g-"], 
        2: ["r-", "m-"],  
    }
    
    for track in range(num_tracks):
    
        #raise ValueError(len(range(song_length)), len(targetNotes), len(closestNotes))
        plt.plot(range(song_length), trackTargetNotes[track], trackColors[track][0])
        plt.plot(range(song_length), trackClosestNotes[track], trackColors[track][1])
    
    
    plt.show()

    