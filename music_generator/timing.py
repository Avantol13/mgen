# Project Modules
from config import config

# Mingus modules
import mingus.core.meter as meter
import mingus.containers.note as note
import mingus.core.value as value

# Other Modules
import random

def get_next_timing(remaining_time_in_bar):
    '''
    Returns a "timing" representing a series of notes that will fit in the remaining portion of the bar.
    '''
    if remaining_time_in_bar > 0.0:
        # The chosen timing progression
        the_chosen_one = None 
        
        # Whether or not we've found The Chosen One
        the_chosen_one_found = False
        
        # Random choice
        choice = random.uniform(0, 1)  
        
        # As long as we haven't found The Chosen One, keep trying.
        # Centuries may pass... but The Chosen One will be found (hopefully).
        while (not the_chosen_one_found and choice >= 0):
            choice = random.uniform(0, 1)  
             
            # Sort by the probability 
            #config.timing_probabilities.sort(key=lambda timing_probabilities: timing_probabilities[0])
            
            for key, val in config['timings']:
                # Subtract the probability from the choice
                choice = choice - float(val[0])
                
                # When it reaches zero, we've hit our choice
                if choice <= 0:
                    progression = []
                    parsed_progression = key.split(' ')
                    for item in parsed_progression:
                        item = item.replace('\'', '')
                        progression.append(eval(item))
                    
                    # If there's room in the measure
                    time_for_choice = get_notes_length(progression)
                    
                    if (remaining_time_in_bar >= time_for_choice):
                        the_chosen_one_found = True
                        the_chosen_one = progression
                        break
    else:
        '''
        TODO: handle this better
        '''
        return None
    
    return the_chosen_one

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
    Determine the remaining musical time in the given bar for the given time signature.
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