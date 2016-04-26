# Mingus modules
import mingus.core.meter as meter
import mingus.containers.note as note

def get_notes_length(list_of_note_values):
    '''
    Return the total musical length of a list of note lengths
    '''
    total_time = 0.0
    
    for note in list_of_note_values:
        total_time += 1.0/note
    
    return total_time    

def get_notes_in_timing(timing):
    '''
    Return how many notes are in the given list of note timings.
    '''
    counter = 0
    for notes in timing:
        counter += len(notes)
    return counter
    
def get_time_remaining(melody_bar, time_signature=meter.common_time):  
    '''
    Return the remaining musical time in the given bar for the given time signature.
    '''  
    # Get information from time signature
    beats_in_measure = time_signature[0]
    what_gets_beat   = (1.0/time_signature[1])
    
    total_time = beats_in_measure * what_gets_beat
    
    time_in_measure = 0.0
    for notes in melody_bar:
        for note in notes:
            time_in_measure += (1.0/note) 
            
    return (total_time - time_in_measure)