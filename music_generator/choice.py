# Project Modules
from config import config

# Mingus Modules
import mingus.core.meter as meter
import mingus.core.value as value

# Other Modules
import random

def choose_time_signature():
    '''
    Returns a time signature.
    TODO: Make this random (create probaility in config file for time sigs)
    '''
    return meter.common_time

def choose_key(): 
    '''
    Returns a random key by using the probabilities in config.
    '''
    choice = random.uniform(0, 1) 
    
    for key, value in config['keys']:
        # Subtract the probability from the choice
        choice = choice - float(value[0])
        
        # When it reaches zero, we've hit our choice
        if choice <= 0:
            return key
        
def choose_chord_progression():
    '''
    Return a random chord progression based on probabilities in config.
    '''
    choice = random.uniform(0, 1)  
    
    for key, value in config['progressions']:
        # Subtract the probability from the choice
        choice = choice - float(value[0])
        
        # When it reaches zero, we've hit our choice
        if choice <= 0:
            # Create a list of the chords
            return key.split(' ')

def choose_notes(number_notes, scale):
    '''
    Returns a list of notes chosen randomly from a given scale.
    '''
    notes_in_scale = len(scale)
    notes = []
    
    while (len(notes) < number_notes):
        # values less than 0 will result in a rest
        choice = random.randint(-3, notes_in_scale-1) 
        if choice >= -1:
            notes.append(scale[choice])
        else:
            # Place a rest
            notes.append(None)
            
    return notes
