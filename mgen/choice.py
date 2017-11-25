'''
It is our choices... that show what we truly are, far more than our abilities.
    - J. K. Rowling
'''

# Project Modules
from mgen import time

# Mingus modules
import mingus.core.meter as meter
import mingus.core.keys as keys

import mingus.core.value as value
import mingus.core.scales as scales

# Other Modules
import random
import warnings

MINGUS_TIMING_LOOKUP = {
    "whole": value.whole,
    "half": value.half,
    "quarter": value.quarter,
    "eighth": value.eighth,
    "sixteenth": value.sixteenth,
    "thirty_second": value.sixteenth,
    "sixty_fourth": value.sixteenth,
    "hundred_twenty_eighth": value.sixteenth,
}

MINGUS_SCALES_LOOKUP = {
    "Ionian": (lambda key: scales.Ionian(key)),
    "Dorian": (lambda key: scales.Dorian(key)),
    "Phrygian": (lambda key: scales.Phrygian(key)),
    "Lydian": (lambda key: scales.Lydian(key)),
    "Mixolydian": (lambda key: scales.Mixolydian(key)),
    "Aeolian": (lambda key: scales.Aeolian(key)),
    "Locrian": (lambda key: scales.Locrian(key)),
    "Major": (lambda key: scales.Major(key)),
    "HarmonicMajor": (lambda key: scales.HarmonicMajor(key)),
    "NaturalMinor": (lambda key: scales.NaturalMinor(key)),
    "HarmonicMinor": (lambda key: scales.HarmonicMinor(key)),
    "MelodicMinor": (lambda key: scales.MelodicMinor(key)),
    "Bachian": (lambda key: scales.Bachian(key)),
    "MinorNeapolitan": (lambda key: scales.MinorNeapolitan(key)),
}


def choose_scale(key, scale_prob_list, choice=None):
    '''
    Return a randomly chosen scale by using the provided probability dictionary.

    :param key: The musical key to use for the scale
    :param scale_prob_list: List of tuples with scales and associated probabilities
    '''
    if choice is None:
        choice = random.uniform(0, 1)

    if choice > 1.0 or choice < 0.0:
        raise AttributeError('Choice ' + str(choice) +
                             ' should be between 0.0 and 1.0')

    for scale, prob in scale_prob_list:
        # Subtract the probability from the choice
        choice = choice - float(prob)
        scale_instance = MINGUS_SCALES_LOOKUP.get(scale,
                                                  (lambda key: scales.HarmonicMajor(key)))(key)

        # When it reaches zero, we've hit our choice
        if choice <= 0:
            break

    return scale_instance


def choose_key(key_prob_list, choice=None):
    '''
    Return a randomly chosen key by using the provided probability dictionary.

    :param key_prob_list: List of tuples with keys and associated probabilities
    :param choice: Leave as default for random choice.
                   float between 0.0 and 1.0 to determine which item in list to
                   choose. Closer to 1 will choose a higher probability item
    '''
    if choice is None:
        choice = random.uniform(0, 1)

    if choice > 1.0 or choice < 0.0:
        raise AttributeError('Choice ' + str(choice) +
                             ' should be between 0.0 and 1.0')

    for key, prob in key_prob_list:
        # Subtract the probability from the choice
        choice = choice - float(prob)
        key = key.replace(' ', '')

        # When it reaches zero, we've hit our choice
        if choice <= 0:
            break

    if keys.is_valid_key(key):
        return str(key)
    else:
        raise AttributeError('Key: ' + key +
                             ' cannot be converted to a mingus scale. ' +
                             'Use # and b for sharp and flat.')


def choose_time_signature(time_signature_prob_list, choice=None):
    '''
    Return a randomly chosen time signature by using the provided probability
    dictionary. TODO: Actually make this random (create probability in cfg file
    for time sigs)

    :param time_signature_prob_list: List of tuples with time_signatures
                                    and associated probabilities
    :param choice: Leave as default for random choice.
               float between 0.0 and 1.0 to determine which item in list to
               choose. Closer to 1 will choose a higher probability item
    '''
    if choice is None:
        choice = random.uniform(0, 1)

    if choice > 1.0 or choice < 0.0:
        raise AttributeError('Choice ' + str(choice) +
                             ' should be between 0.0 and 1.0')

    return meter.common_time


def choose_chord_progression(chord_progression_prob_list, choice=None):
    '''
    Return a list of chords randomly by using the provided probability
    dictionary.

    :param chord_progression_prob_list: List of tuples with chord progressions
                                        and associated probabilities
    :param choice: Leave as default for random choice.
                   float between 0.0 and 1.0 to determine which item in list to
                   choose. Closer to 1 will choose a higher probability item
    '''
    if choice is None:
        choice = random.uniform(0, 1)

    if choice > 1.0 or choice < 0.0:
        raise AttributeError('Choice ' + str(choice) +
                             ' should be between 0.0 and 1.0')

    for chords, prob in chord_progression_prob_list:
        # Subtract the probability from the choice
        choice = choice - float(prob)

        # Create a list of the chords
        chords_list = chords.split(' ')

        # When it reaches zero, we've hit our choice
        if choice <= 0:
            break

    return chords_list


def choose_notes(number_notes, scale, choice=None):
    '''
    Returns a list of notes chosen randomly from a given scale.

    :param number_notes: The number of notes to add to list
    :param scale: List of notes to choose from
    :param choice: Leave as default for random choice.
                   float between 0.0 and 1.0 to determine which item in list to
                   choose. Closer to 1 will choose a higher probability item

    TODO: Don't just use the ascending scale...
    '''
    if choice is None:
        choice = random.uniform(0, 1)

    if choice > 1.0 or choice < 0.0:
        raise AttributeError('Choice ' + str(choice) +
                             ' should be between 0.0 and 1.0')

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


def choose_next_timing(remaining_time_in_bar, note_timing_prob_list, choice=None):
    '''
    Returns a note timing representing a series of notes that will fit in the
    remaining portion of the bar.

    :param remaining_time_in_bar: The remaining time in the musical bar
    :param note_timing_prob_list: List of tuples with note timings and associated
                                  probabilities
    :param choice: Leave as default for random choice.
                   float between 0.0 and 1.0 to determine which item in list to
                   choose. Closer to 1 will choose a higher probability item
    '''
    if choice is None:
        choice = random.uniform(0, 1)

    if choice > 1.0 or choice < 0.0:
        raise AttributeError('Choice ' + str(choice) +
                             ' should be between 0.0 and 1.0')

    if remaining_time_in_bar > 0.0:
        # The chosen time progression
        the_chosen_one = None

        # Whether or not we've found The Chosen One
        the_chosen_one_found = False

        # Random choice
        choice = random.uniform(0, 1)

        # As long as we haven't found The Chosen One, keep trying.
        # Centuries may pass... but The Chosen One will be found, lest we all
        # parish in an infinite search.
        while (not the_chosen_one_found and choice >= 0.0):
            choice = random.uniform(0, 1)

            for timing, val in note_timing_prob_list:
                # Subtract the probability from the choice
                choice = choice - float(val)

                # When it reaches zero, we've hit a Prospective Chosen One
                if choice <= 0.0:
                    note_timing = []
                    parsed_note_timings = timing.split(' ')
                    for item in parsed_note_timings:
                        item = item.replace('\'', '')
                        note_timing.append(_get_mingus_timing(item))

                    # Length of time The Prospective Chosen One takes up in the bar
                    time_for_choice = time.get_notes_length(note_timing)

                    if (remaining_time_in_bar >= time_for_choice):
                        # We have found The Chosen One
                        the_chosen_one = note_timing
                        the_chosen_one_found = True
                        break

                    # We must restart our search
    else:
        raise AttributeError('Remaining time in bar specified as ' +
                             remaining_time_in_bar +
                             '. You can\'t have negative time left.')

    if the_chosen_one is None:
        # TODO: Scream and cry?
        warnings.warn('Unable to fill bar with a configured note_timing.')
        pass

    return the_chosen_one


def _get_mingus_timing(raw_timing):
    dotted_indicator = "_dotted"
    dotted = False

    if raw_timing[-len(dotted_indicator):] == dotted_indicator:
        dotted = True
        raw_timing = raw_timing[:-len(dotted_indicator)]

    # default to eight note
    timing = MINGUS_TIMING_LOOKUP.get(raw_timing, value.eighth)

    if dotted:
        timing = value.dots(timing)

    return timing
