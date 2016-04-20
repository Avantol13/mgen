#!/usr/bin/python2
'''
Created on Jan 21, 2016

@author: Alex VanTol

TODO: Use http://www.sphinx-doc.org/en/stable/tutorial.html for documentation
'''

# Project Modules
from music_generator import create
from music_generator import choice
from music_generator import convert
from music_generator import config as config_module
from music_generator.config import config

# Mingus Modules
import mingus.extra.lilypond as LilyPond
from mingus.midi import midi_file_out

# Other Modules
from datetime import datetime
import argparse
import os
import sys

def update_config(args):
    if args.key:
        config['key'] = args.key
    else:
        config['key'] = choice.choose_key()
            
    if args.output_filepath:
        config['output_filename'] = args.output_filepath
    else:  
        # Create filename based on key and time
        config['output_filename'] = str(os.getcwd()) + '\output\key_' + config['key'] + '_' + str(datetime.now()).replace(' ', '_').replace(':', '.')

    if args.composition_name:
        config['composition_name'] = args.composition_name  
    else:
        # Default initializations
        config['composition_name'] = 'Programmatically Generated Music'
        
def main():
    # Parse arguments from command line interface
    parser = argparse.ArgumentParser()
    parser.add_argument('-prob', '--probability_file', help='Path to configuration file, ' + \
                        'if not provided, will search local path for probabilities.cfg')
    parser.add_argument('-o', '--output_filepath', help='Overrides default output file name ' + \
                        '(key and time) with name provided here')
    parser.add_argument('-c', '--composition_name', help='Name to associate with the ' + \
                        'generated composition.')
    parser.add_argument('-k', '--key', help='Forces the musical key. Use lower case for ' + \
                        'minor keys, b for flat, and # for sharp')
    parser.add_argument('-ac', '--adaptive_chord_track', help='Adds a track where the program ' + \
                        'adaptively decides what chords to place based on a melody. Specify ' + \
                        'integer value representing how many bars of melody to generate')
    parser.add_argument('-midi', '--generate_midi_file', help='Generates a MIDI file as well ' + \
                        'as a PDF', action='store_true')
    args = parser.parse_args()
    
    # If path is provided, use it, otherwise, use default
    if args.probability_file is None:
        config_module.configure_probabilities()
    else:
        config_module.configure_probabilities(args.probability_file)
    
    # Update configuration settings based on user input
    update_config(args)
    
    # Determine the time signature and scale
    time_signature = choice.choose_time_signature()
    scale = convert.convert_to_scale(config['key'])
    
    print('---------------------------------------------------------------------------')
    print('-------------------------- Music Generator Output -------------------------')
    print('---------------------------------------------------------------------------\n')
    print('Time Signature: ' + str(time_signature))
    print('           Key: ' + str(config['key']))
    print('         Scale: ' + str(scale))
    
    # This will hold all the mingus tracks that will be added to the composition
    tracks = []
    
    if args.adaptive_chord_track:
        try:
            num_bars = int(args.adaptive_chord_track)
        except Exception as exp:
            print('ERROR: ' + str(args.adaptive_chord_track) + ' is not a valid integer. ' + \
                  '-ac / --adaptive_chord_track requires an int to represent ' + \
                  'the number of bars of melody you\'d like to generate.')
            sys.exit()
            
        melody_track = create.create_melody_track(num_bars, config['key'], time_signature)
        tracks.append(melody_track)
        # TODO: Check create_melody_track in create for idea to use determine_chords or determine_progression 
        pass
    else:
        chord_progression_track = create.create_chords_track(config['key'], time_signature=time_signature)
        num_bars = len(chord_progression_track)
        melody_track = create.create_melody_track(num_bars, config['key'], time_signature)
        tracks.append(melody_track)
        tracks.append(chord_progression_track)

    print('---------------------------------------------------------------------------\n')
    print('Generating composition...')
    
    # Create composition
    composition = create.create_composition(config['composition_name'], tracks)
    
    if args.generate_midi_file:
        # Output a midi file
        midi_file_out.write_Composition(config['output_filename'] + '.mid', composition, bpm=100, repeat=1, verbose=False)
 
    # Output the pdf score
    LilyPond.to_pdf(LilyPond.from_Composition(composition), config['output_filename'])
    
if __name__ == '__main__':
    main()

    