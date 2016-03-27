'''
Created on Jan 21, 2016

@author: Alex VanTol

TODO: Use http://www.sphinx-doc.org/en/stable/tutorial.html for documentation
'''

# Project Modules
from music_generator import create
from music_generator import choice
from music_generator import convert

# Mingus Modules
import mingus.extra.lilypond as LilyPond
from mingus.midi import midi_file_out

# Other Modules
from datetime import datetime
import os

def main():
    print('\n------------------------- Music Generator Output -------------------------')
    time_signature = choice.choose_time_signature()
    key = choice.choose_key()
    
    # Force a key
    # key = 'C'
    scale = convert.convert_to_scale(key)
    
    print('Time Signature: ' + str(time_signature))
    print('           Key: ' + str(key))
    print('         Scale: ' + str(scale))
    
    # Create tracks
    chord_progression_track = create.create_chords_track(key, time_signature=time_signature)
    num_bars = len(chord_progression_track.bars)
    melody_track = create.create_melody_track(num_bars, key, time_signature) 
    tracks = [melody_track, chord_progression_track]
    
    print('---------------------------------------------------------------------------\n')
    
    print('Generating composition as PDF and MIDI files...')
    
    # Create filename based on key and time
    filename = str(os.getcwd()) + '\output\key_' + str(key) + '_' + str(datetime.now()).replace(' ', '_').replace(':', '.')
    
    # Create composition
    composition = create.create_composition('Programmatically Generated Music', tracks)
    
    # Output the pdf score
    LilyPond.to_pdf(LilyPond.from_Composition(composition), filename)
    
    # Output a midi file
    midi_file_out.write_Composition(filename + '.mid', composition, bpm=100, repeat=1, verbose=False)
    
if __name__ == '__main__':
    main()
    

        
    