"""
The time is always right to do what is right.
    - Martin Luther King, Jr.
"""

# Mingus modules
import mingus.core.meter as meter
import mingus.containers.note as note
import mingus.containers.bar as bar
import mingus.core.value as value

def get_notes_length(list_of_note_values):
    """
    Return the total musical length of a list of note lengths

    :param list_of_note_values: List of note timings
    """
    total_time = 0.0

    for note in list_of_note_values:
        total_time += 1.0 / note

    return total_time

def get_notes_in_timing(timing):
    """
    Return how many notes are in the given list of note timings.

    :param timing: List of note timings
    """
    counter = 0
    for notes in timing:
        if notes:
            counter += len(notes)
    return counter

def get_time_remaining(melody_bar, time_signature=meter.common_time):
    """
    Return the remaining musical time in the given bar for the given time
    signature.

    :param melody_bar: The musical bar
    :param time_signature: Time signature for the bar
    """
    # Get information from time signature
    beats_in_measure = time_signature[0]
    what_gets_beat   = (1.0 / time_signature[1])

    # Beat it
    total_time = beats_in_measure * what_gets_beat

    time_in_measure = 0.0
    for notes in melody_bar:
        if notes:
            for note in notes:
                time_in_measure += (1.0 / note)

    return (total_time - time_in_measure)

def prepend_empty_bars_to_track(track, num_bars):
    """
    Return a track with empty bars at the beginning

    :param track: The musical track
    :param num_bars: Number of empty bars to preprend
    """
    empty_bar = bar.Bar()
    empty_bar.place_rest(value.whole)
    for _ in range(0, num_bars):
        track.bars.insert(0, empty_bar)
    return track
