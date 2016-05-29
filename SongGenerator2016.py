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


import mido
import time
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

    noteArray = zeros((1,1,1))
    
    for i, track in enumerate(mid.tracks[2:]):
    
        noteArray = vstack((noteArray, [[[0]]]))

    newNoteShape = noteArray.shape
    newNoteArray = zeros(newNoteShape)
    
    for i, track in enumerate(mid.tracks[1:]):
        #print 'Track {}: {}'.format(i, track.name)
        
        currentNotes = []
        
        if track.name not in exclusions: 
        
            for message in track:
            
                if message.type != "meta message":
                    
                    if message.type == "note_on": 
                                
                        currentNotes.append(float(message.note))
                    
                    elif message.type == "note_off": 
            
                        currentNotes.remove(float(message.note))
                        
                    if len(currentNotes) > 0:         
                        newNoteArray[i] = currentNotes
                        
                    noteArray = hstack((noteArray, newNoteArray))
                    
                    newNoteArray = zeros(newNoteShape)
                
    print noteArray

def playMidi(mid): 

    for message in mid.play():
        outport.send(message)

def Main(): 
    
    midiSetup()
    parseMidi(MidiFile('midi/Smbtheme.mid'))
    
Main()


'''
TESTING

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




