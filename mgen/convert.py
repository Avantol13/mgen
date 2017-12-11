'''
To convert somebody go and take them by the hand and guide them.
    - Thomas Aquinas
'''

# Mingus Modules
import mingus.containers.note as note
import mingus.core.notes as mingus_notes
import mingus.core.meter as meter
import mingus.core.scales as scales
import mingus.core.value as value
import mingus.core.keys as keys
import mingus.containers.bar as bar
import mingus.containers.track as track

def convert_notes_to_bar(musical_key, melody_timing, chosen_notes,
                         time_signature=meter.common_time):
    '''
    Returns a bar of music by combining a given key, note timing, notes,
    and time signature.

    :param musical_key: The musical key to put the bar in
    :param melody_timing: Timing of the notes given
    :param chosen_notes: The notes to assign to the timing
    :param time_signature: The musical time signature for the bar
    '''
    mingus_bar = bar.Bar()

    if keys.is_valid_key(musical_key):
        mingus_bar.key = keys.Key(musical_key)
        mingus_bar.set_meter(time_signature)

        # Go through timing, assign chosen note to each timing and add to bar
        for notes_timing in melody_timing:

            # Index in list of notes to choose
            chosen_note_index = 0

            if notes_timing:
                for note_timing in notes_timing:
                    note = chosen_notes[chosen_note_index]

                    # Move to next note
                    chosen_note_index += 1

                    mingus_bar.place_notes(note, note_timing)
    else:
        raise AttributeError('Key: ' + musical_key + ' cannot be converted' +
                             ' to a mingus key.')

    return mingus_bar

def convert_to_scale(key, scale):
    '''
    Returns a scale of notes given a key.

    :param key: The musical key
    :param scale: Unused

    TODO: Different scales? Add configuration for different scales.
    '''
    notes_in_scale = []

    # Remove key information
    key = key.replace(' ', '')

    major_key_bool = key.istitle()

    try:
        if major_key_bool:
            notes_in_scale = scales.Ionian(key).ascending()
        else:
            key = key.upper()
            notes_in_scale = scales.NaturalMinor(key).ascending()
    except Exception:
        raise AttributeError('Key: ' + key + ' cannot be converted to a' +
                             ' mingus scale. Use # and b for sharp and flat.')

    return notes_in_scale

def convert_chord_progression_to_track(key, chord_progression,
                                       time_signature=meter.common_time,
                                       chord_timing=None):
    '''
    Return a mingus Track given a key, chord progression, chord timing,
    and time signature.

    :param musical_key: The musical key to put the bar in
    :param chord_progression: The progression of chords for the track
    :param time_signature: The musical time signature for the track
    :param chord_timing: Timing for the chords track
    '''
    # If chord_timing not provided, make each chord a whole bar
    if chord_timing is None:
        chord_timing = [[value.whole]] * len(chord_progression)

    new_track = track.Track()

    chord_index = 0

    for timing in chord_timing:
        new_bar = convert_notes_to_bar(key, [timing],
                                       [chord_progression[chord_index]],
                                       time_signature)
        chord_index += 1
        new_track.add_bar(new_bar)

    return new_track

def alter_octave(bar, octave_change):
    '''
    Returns note timing with octave change based on value for octave_change
    (ex: alter_octave(bar, -1))

    :param bar: List of bar/chords to change octave of
    :param octave_change: Integer to shift octave by. Positive is up, negative is down
    '''
    new_bar = []

    # Go through all the different note timings/chords
    for notes in bar:
        note_octave_change = []

        # If it's not a rest (None) and NOT a single note,
        # then continue into the list of notes
        if notes:
            if mingus_notes.is_valid_note(notes):
                new_note = _adjust_note_octave(notes, octave_change)

                # Append the altered note
                note_octave_change.append(new_note)
            else:
                for given_note in notes:
                    if given_note:
                        new_note = _adjust_note_octave(given_note, octave_change)
                    else:
                        new_note = None

                    # Append the altered note
                    note_octave_change.append(new_note)

        new_bar.append(note_octave_change)

    return new_bar

def _adjust_note_octave(given_note, octave_change):
    new_note = note.Note(given_note)
    octave_change_temp = octave_change

    if octave_change > 0:
        while (octave_change_temp > 0):
            new_note.octave_up()
            octave_change_temp -= 1
    elif octave_change < 0:
        while (octave_change_temp < 0):
            new_note.octave_down()
            octave_change_temp += 1
    else:
        # Do nothing
        pass

    return new_note