'''
Created on May 11, 2016

@author: Alex VanTol
'''

# Project Modules
from music_generator import time

# Mingus modules
import mingus.core.meter as meter
import mingus.core.keys as keys

# Need scales and value import for eval() purposes, DON'T remove
import mingus.core.scales as scales
import mingus.core.value as value

# Other Modules
import random

def choose_scale(key, scale_prob_list):
    '''
    Return a randomly chosen key by using the provided probability dictionary.
    '''
    choice = random.uniform(0, 1)

    for scale, prob in scale_prob_list:
        # Subtract the probability from the choice
        choice = choice - float(prob)

        # When it reaches zero, we've hit our choice
        if choice <= 0:
            scale_instance = eval(scale)(key)
            return scale_instance

def choose_key(key_prob_list):
    '''
    Return a randomly chosen key by using the provided probability dictionary.
    '''
    choice = random.uniform(0, 1)

    for key, prob in key_prob_list:
        # Subtract the probability from the choice
        choice = choice - float(prob)

        # When it reaches zero, we've hit our choice
        if choice <= 0:
            if keys.is_valid_key(key):
                return key.replace(' ', '')
            else:
                raise AttributeError('Key: ' + key +
                                     ' cannot be converted to a mingus scale. ' +
                                     'Use # and b for sharp and flat.')

def choose_time_signature(time_signature_prob_list):
    '''
    Return a randomly chosen time signature by using the provided probability 
    dictionary. TODO: Actually make this random (create probability in cfg file 
    for time sigs)
    '''
    return meter.common_time

def choose_chord_progression(chord_progression_prob_list):
    '''
    Return a randomly chosen chord progression by using the provided probability
    dictionary.
    '''
    choice = random.uniform(0, 1)

    for chords, prob in chord_progression_prob_list:
        # Subtract the probability from the choice
        choice = choice - float(prob)

        # When it reaches zero, we've hit our choice
        if choice <= 0:
            # Create a list of the chords
            return chords.split(' ')

def choose_notes(number_notes, scale):
    '''
    Returns a list of notes chosen randomly from a given scale.

    TODO: Don't just use the ascending scale...
    '''
    notes_in_scale = len(scale.ascending())
    notes = []

    while (len(notes) < number_notes):
        # values less than 0 will result in a rest
        choice = random.randint(-3, notes_in_scale - 1)
        if choice >= -1:
            notes.append(scale.ascending()[choice])
        else:
            # Place a rest
            notes.append(None)

    return notes

def choose_next_timing(remaining_time_in_bar, note_timing_prob_list):
    '''
    Returns a "time" representing a series of notes that will fit in the
    remaining portion of the bar.
    '''
    if remaining_time_in_bar > 0.0:
        # The chosen time progression
        the_chosen_one = None

        # Whether or not we've found The Chosen One
        the_chosen_one_found = False

        # Random choice
        choice = random.uniform(0, 1)

        # As long as we haven't found The Chosen One, keep trying.
        # Centuries may pass... but The Chosen One will be found (hopefully).
        while (not the_chosen_one_found and choice >= 0):
            choice = random.uniform(0, 1)

            for timing, val in note_timing_prob_list:
                # Subtract the probability from the choice
                choice = choice - float(val)

                # When it reaches zero, we've hit our choice
                if choice <= 0:
                    note_timing = []
                    parsed_note_timings = timing.split(' ')
                    for item in parsed_note_timings:
                        item = item.replace('\'', '')
                        note_timing.append(eval(item))

                    # Length of time The Chosen One takes up in the bar
                    time_for_choice = time.get_notes_length(note_timing)

                    # We may have found The Chosen One
                    the_chosen_one = note_timing
                    if (remaining_time_in_bar >= time_for_choice):
                        the_chosen_one_found = True
                        break
    else:
        '''
        TODO: handle this better
        '''
        raise IndexError()

    if the_chosen_one is None:
        pass

    return the_chosen_one
