#!/usr/bin/python2
'''
Created on Jan 21, 2016

@author: Alex VanTol
'''

# Project Modules
from music_generator.create import MusicGenerator
from music_generator import style
import sys
import argparse
from colorama import Fore, Back, Style
import traceback

def main():
    my_generator = None

    # Parse arguments into script. Note that 1st argument is script name
    args = parse_args(sys.argv[1:])

    try:
        my_generator = MusicGenerator.from_pickle('data.pkl')
    except IOError:
        my_style = style.Style(style.DEFAULT)
        my_generator = MusicGenerator(my_style,
                                      composition_title='Programmatically ' +
                                                        'Generated Music')

        my_generator.add_melody_track(style=my_style, location_to_add=0,
                                      num_bars=4)
        my_generator.add_melody_track(style=my_style, location_to_add=5,
                                      num_bars=4, times_to_repeat=2)

        my_generator.add_chords_track(num_bars=8, octave_adjust=-1)
        my_generator.add_chords_track(num_bars=8, location_to_add=9,
                                      octave_adjust=-1)

    if args.generate_pickle:
        my_generator.export_pickle(args.generate_pickle)
    if args.generate_pdf:
        my_generator.export_pdf(args.generate_pdf)
    if args.generate_midi:
        my_generator.export_midi(args.generate_midi, args.beats_per_minute)

    print(my_generator)

def parse_args(args):
    """
    Returns parsed and validated arguments that were passed into the script.

    :param args: The arguments passed into the script
    """
    # Parse arguments from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-st', '--style_file_path',
                        help='Path to configuration file, if not provided, ' +
                             'will search style folder for default.cfg')
    parser.add_argument('-c', '--composition_name',
                        help='Name to associate with the generated composition.')
    parser.add_argument('-k', '--key',
                        help='Forces the musical key. Use lower case for ' +
                        'minor keys, b for flat, and # for sharp')
    parser.add_argument('-bpm', '--beats_per_minute',
                        help='Beats per minute for midi output.',
                        nargs='?', default=90)

    # nargs=? allows 0 or 1 argument. If unspecified, will use default location
    parser.add_argument('-midi', '--generate_midi',
                        help='Generates the composition as a MIDI file',
                        nargs='?', const='output\\', default=None)
    parser.add_argument('-pdf', '--generate_pdf',
                        help='Generates the musical score as a PDF file',
                        nargs='?', const='C:\\Temp\\example.pdf', default=None)
    parser.add_argument('-pkl', '--generate_pickle',
                        help='Generates the MusicGenerator object as a .pkl ' +
                        '(reimportable Python object) file',
                        nargs='?', const='output\\', default=None)

    parser.add_argument('-l', '--load_pickle',
                        help='Load a MusicGenerator previously saved as a .pkl')

    return parser.parse_args()

def print_header():
    """
    Print header of tool into command line.
    """
    print(Style.BRIGHT + '\n--------------------------------------------------' +
          '------------------------------')
    print('   MUSIC GENERATOR')
    print('-------------------------------------------------------------------' +
          '-------------\n' + Style.RESET_ALL)

def print_footer():
    """
    Print footer of tool into command line.
    """
    print(Style.BRIGHT + '\n--------------------------------------------------' +
          '------------------------------')
    print('   END')
    print('-------------------------------------------------------------------' +
          '-------------\n' + Style.RESET_ALL)

def print_error(error=None):
    """
    Print an error into command line with traceback.

    :param error: Optional string to print before traceback
    """
    print(Fore.RED + Style.BRIGHT + '!!!--------------------------------------' +
          '------------------------------------!!!\n')

    if error is not None:
        print(error + '\n')

    traceback.print_exc()

    print('\n!!!--------------------------------------------------------------' +
          '------------!!!' + Style.RESET_ALL + '\n')

if __name__ == '__main__':
    main()
