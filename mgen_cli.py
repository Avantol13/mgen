"""
Created on Jan 21, 2016

@author: Alexander VanTol
"""

# Project Modules
import mgen
import sys
import argparse
import traceback
import os


def main():
    my_generator = None

    # Parse arguments into script. Note that 1st argument is script name
    args = _get_parser(sys.argv[1:]).parse_args()

    # If we don't want output, ignore all print statements
    if args.silent:
        # Redirect print output to null device on operating system
        print_redirect = open(os.devnull, 'w')
        sys.stdout = print_redirect

    _setup_cfg(args.cfg_file_path)

    print_header()

    # Use provided Style or use default
    if args.style_file_path:
        try:
            my_style = mgen.Style(args.style_file_path)
        except IOError:
            print_error('Couldn\'t find ' + args.style_file_path)
    else:
        my_style = mgen.Style(mgen.DEFAULT_CFG_FILE)

    # Load MusicGenerator object is specified, otherwise create a new one
    if args.load_pickle:
        try:
            my_generator = mgen.MusicGenerator.from_pickle(args.load_pickle)
            # Force style if provided
            if args.style_file_path:
                my_generator.style = my_style
        except IOError:
            print_error('Couldn\'t find ' + args.load_pickle)
    else:
        my_generator = mgen.MusicGenerator(my_style, composition_title=args.composition_name)

    # Force musical key if provided
    if args.key:
        my_generator.set_key(args.key)

    if args.melody_track:
        if args.repeat_tracks:
            my_generator.insert_track(
                my_generator.create_melody_track(
                    style=my_style,
                    num_bars=args.melody_track
                ),
                location_to_add=args.start_bar,
                times_to_repeat=args.repeat_tracks
            )
        else:
            my_generator.insert_track(
                my_generator.create_melody_track(
                    style=my_style,
                    num_bars=args.melody_track
                ),
                location_to_add=args.start_bar
            )

    if args.chords_track:
        if args.repeat_tracks:
            my_generator.insert_track(
                my_generator.create_chords_track(
                    style=my_style,
                    num_bars=args.melody_track,
                    octave_adjust=-1
                ),
                location_to_add=args.start_bar,
                times_to_repeat=args.repeat_tracks
            )
        else:
            my_generator.insert_track(
                my_generator.create_chords_track(style=my_style,
                                                 location_to_add=args.start_bar,
                                                 num_bars=args.melody_track,
                                                 octave_adjust=-1)
            )

    # File exports
    if args.generate_pickle:
        export_location = my_generator.export_pickle(args.generate_pickle)
        print('Generated PKL file: ' + export_location)
    if args.generate_pdf:
        export_location = my_generator.export_pdf(args.generate_pdf)
        print('Generated PDF file: ' + export_location)
    if args.generate_midi:
        export_location = my_generator.export_midi(args.generate_midi, args.beats_per_minute)
        print('Generated MIDI file: ' + export_location)

    print('\n' + str(my_generator))
    print_footer()


def _get_parser(args):
    """
    Returns parsed and validated arguments that were passed into the script.

    :param args: The arguments passed into the script
    """
    # Parse arguments from command line
    # NOTE: nargs=? allows 0 or 1 argument. If unspecified, will use default
    parser = argparse.ArgumentParser(description='Music Generator: ' +
                                     'Generate randomized musical ' +
                                     'compositions based on probabilities.')
    parser.add_argument('-mt', '--melody_track', metavar='NUM_BARS_TO_GEN',
                        help='Adds a melody track to the composition.',
                        nargs='?', const=8, type=int, default=None)
    parser.add_argument('-ct', '--chords_track', metavar='NUM_BARS_TO_GEN',
                        help='Adds a chords track to the composition.',
                        nargs='?', const=8, type=int, default=None)
    parser.add_argument('-sb', '--start_bar', type=int,
                        help='Bar in the composition to add the tracks to. ' +
                        ' For example, --start_bar 9 will generate tracks ' +
                        'beginning at the 9th bar.',
                        nargs='?', default=0)
    parser.add_argument('-r', '--repeat_tracks', type=int,
                        help='Will repeat the specified tracks the amount ' +
                        'of times specified.',
                        nargs='?', const=1, default=None)

    parser.add_argument('-c', '--composition_name',
                        help='Name to associate with the generated composition.',
                        nargs='?', default='Untitled')
    parser.add_argument('-k', '--key',
                        help='Forces the musical key. Use lower case for ' +
                        'minor keys, b for flat, and # for sharp')

    parser.add_argument('-midi', '--generate_midi', metavar='MIDI_OUTPUT_PATH',
                        help='Generates the composition as a MIDI file',
                        nargs='?', const=os.path.dirname(os.path.abspath(__file__)) + '/output/', default=None)

    parser.add_argument('-pdf', '--generate_pdf', metavar='PDF_OUTPUT_PATH',
                        help='Generates the musical score as a PDF file',
                        nargs='?', const=os.path.dirname(os.path.abspath(__file__)) + '/output/', default=None)

    parser.add_argument('-pkl', '--generate_pickle', metavar='PKL_OUTPUT_PATH',
                        help='Generates the MusicGenerator object as a .pkl ' +
                        '(reimportable Python object) file',
                        nargs='?', const=os.path.dirname(os.path.abspath(__file__)) + '/output/', default=None)

    parser.add_argument('-st', '--style_file_path', metavar='STYLE_FILE_PATH',
                        help='Path to musical probabilities configuration file,' +
                        ' if not provided, will use default style.')

    parser.add_argument('-l', '--load_pickle', metavar='PKL_FILE_PATH',
                        help='Load a MusicGenerator previously saved as' +
                        ' a .pkl file.')

    parser.add_argument('-bpm', '--beats_per_minute',
                        help='Beats per minute for midi output.',
                        nargs='?', default=90, type=int)

    parser.add_argument('-s', '--silent', help='Silence printing information to command window',
                        action='store_true')

    parser.add_argument("-cfg", "--cfg_file_path",
                        type=str,
                        default=os.path.abspath("./cfg/config.py"),
                        help=("Absolute path to Python file "
                              "containing necessary configuration "
                              "values for the tool."))

    return parser


def _setup_cfg(cfg_file_path):
    mgen.cfg_import.set_global_config(cfg_file_path)


def print_header():
    """
    Print header of tool into command line.
    """
    print('\n--------------------------------------------------' +
          '------------------------------')
    print('   MUSIC GENERATOR')
    print('-------------------------------------------------------------------' +
          '-------------\n')

def print_footer():
    """
    Print footer of tool into command line.
    """
    print('\n--------------------------------------------------' +
          '------------------------------')
    print('   END')
    print('-------------------------------------------------------------------' +
          '-------------\n')

def print_error(error=None):
    """
    Print an error into command line with traceback.

    :param error: Optional string to print before traceback
    """
    print('!!!--------------------------------------' +
          '------------------------------------!!!\n')

    if error is not None:
        print(error + '\n')

    traceback.print_exc()

    print('\n!!!--------------------------------------------------------------' +
          '------------!!!\n')


if __name__ == '__main__':
    main()
