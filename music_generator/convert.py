# Mingus Modules
import mingus.containers.note as note
import mingus.core.meter as meter
import mingus.core.scales as scales
import mingus.core.value as value
import mingus.core.keys as keys
import mingus.containers.bar as bar
import mingus.containers.track as track

def convert_notes_to_bar(musical_key, melody_timing, chosen_notes, time_signature=meter.common_time):
    '''
    Returns a bar of music by combining a given key, note timing, notes, and time signature.
    '''
    mingus_bar = bar.Bar()
    if keys.is_valid_key(musical_key):
        mingus_bar.key = keys.Key(musical_key)
        mingus_bar.set_meter(time_signature)
        
        # Index in list of notes to choose
        chosen_note_index = 0
        
        # Go through timing, assign chosen note to each timing and add to bar
        for notes_timing in melody_timing:
            # TODO make whole notes_timing a rest??
            for note_timing in notes_timing:
                note = chosen_notes[chosen_note_index]
                
                # Move to next note
                chosen_note_index += 1
                
                mingus_bar.place_notes(note, note_timing)
    else:
        raise AttributeError('Key: ' + musical_key + ' cannot be converted to a mingus key.')
        
    return mingus_bar

def convert_to_scale(key): 
    '''
    Returns a scale of notes given a key.
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
        raise AttributeError('Key: ' + key + ' cannot be converted to a mingus scale. ' +
                             'Use # and b for sharp and flat.')
    
    return notes_in_scale

def convert_chord_progression_to_track(key, chord_progression, time_signature=meter.common_time, chord_timing=None):
    '''
    Return a mingus Track given a key, chord progression, chord timing, and time signature.
    '''
    # If chord_timing not provided, make each chord a whole bar
    if (chord_timing == None):
        chord_timing=[[value.whole]]*len(chord_progression)
    
    new_track = track.Track()
    
    chord_index = 0
    
    for timing in chord_timing:    
        new_bar = convert_notes_to_bar(key, [timing], [chord_progression[chord_index]], time_signature)
        chord_index += 1
        new_track.add_bar(new_bar)
    
    return new_track

def change_octave(note_timings, octave_change):
    '''
    Returns note timing with octave change based on value for octave_change (ex: -1, 2)
    '''
    new_note_timings = []
    
    # Go through all the different note timings/chords
    for note_timing in note_timings:
        note_timing_octave_change = []
        
        # For every note in the timing/chord, change octave
        for given_note in note_timing:
            new_note = note.Note(given_note)
            octave_change_temp = octave_change
            
            if octave_change > 0:
                while(octave_change_temp > 0):
                    new_note.octave_up()
                    octave_change_temp -= 1
            elif octave_change < 0:
                while(octave_change_temp < 0):
                    new_note.octave_down()
                    octave_change_temp += 1
            else:
                # Do nothing
                pass
            
            # Append the altered note
            note_timing_octave_change.append(new_note)
        new_note_timings.append(note_timing_octave_change)
    
    return new_note_timings
