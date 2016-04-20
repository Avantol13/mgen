# Project Modules
from music_generator import choice
from music_generator import convert
from music_generator import timing
from music_generator.config import config

# Mingus modules
import mingus.core.progressions as progressions
import mingus.core.meter as meter
import mingus.containers.composition as composition
import mingus.containers.track as track

def create_composition(title='Untitled', tracks=None):
    '''
    Creates a mingus Composition object from given tracks.
    '''
    music_composition = composition.Composition()
    music_composition.set_author(config['Author'], '')
    
    # If no tracks are supplied, create everything
    if tracks is None:
        #TODO Generate everything
        pass
    else:
        music_composition.set_title(title)
        
        # Add tracks to the composition
        for track in tracks:
            music_composition.add_track(track)
    
    return music_composition
       
def create_melody_track(num_bars, key, time_signature=meter.common_time): 
    '''
    Returns a mingus Track containing bars of randomly generated melodies.
    '''
    melody_track = track.Track()
            
    # Get scale based on key
    scale = convert.convert_to_scale(key)
    
    for index in range(0, num_bars):
        print('--------------------------------- Bar ' + str(index) + ' ----------------------------------')
    
        # Create timing for melody
        melody_timing = create_melody_timing(time_signature)
        print(' Melody Timing: ' + str(melody_timing))
        
        # Determine number notes in melody
        number_notes = timing.get_notes_in_timing(melody_timing)
        
        # Choose notes for melody based on scale for given key
        chosen_notes = choice.choose_notes(number_notes, scale)
        print('  Chosen Notes: ' + str(chosen_notes))
        
        # Combine melody timing and notes into a mingus Bar object
        bar_to_add = convert.convert_notes_to_bar(key, melody_timing, chosen_notes, time_signature)
        
        print('TESTING STUFF...')
        print(bar_to_add.determine_chords(shorthand=True))
        print(bar_to_add.determine_progression(shorthand=True))
        
        # Add bar to track
        melody_track.add_bar(bar_to_add)
    
    return melody_track

def create_chords_track(key, time_signature=meter.common_time):
    '''
    Return a mingus Track given a key and time signature. 
    TODO: Create chord length other than all whole notes
    '''
    # Create chord progression
    raw_chord_progression = choice.choose_chord_progression()
    print('   Progression: ' + str(raw_chord_progression))
    chord_progression_notes = progressions.to_chords(raw_chord_progression, key)
    
    # Decrease octave by 1
    chord_progression = convert.change_octave(chord_progression_notes, -1)
    
    return convert.convert_chord_progression_to_track(key, chord_progression, time_signature=time_signature)

def create_melody_timing(time_signature=meter.common_time):
    '''
    Returns a list of note lengths representing the timing of a melody for a single bar.
    '''
    melody_bar = []
    
    # If valid time signature is supplied, use it to craft melody, otherwise use common time
    if not meter.is_valid(time_signature):
        raise AttributeError('Time signature: ' + time_signature + ' cannot be converted to a mingus meter. ' +
                         'Use tuple (#, #) format. Ex: (4, 4)')
    else:
        remaining_time_in_bar = timing.get_time_remaining(melody_bar, time_signature)
        
        # Continue getting note progressions as long as they're room in the bar
        while (remaining_time_in_bar > 0.0):
            next_timing = timing.get_next_timing(remaining_time_in_bar)
                        
            melody_bar.append(next_timing)
            
            remaining_time_in_bar = timing.get_time_remaining(melody_bar, time_signature)
    
    return melody_bar
