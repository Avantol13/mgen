"""
In a time of destruction, create something.
    - Maxine Hong Kingston
"""

# Project Modules
from mgen import convert
from mgen import time
from mgen import choice
from mgen import style
from mgen import cfg_import
from mgen.style import Style

# Mingus modules
import mingus.core.keys as keys
import mingus.core.progressions as progressions
import mingus.core.meter as meter
import mingus.containers.composition as mingus_composition
import mingus.containers.track as track
import mingus.extra.lilypond as LilyPond
from mingus.midi import midi_file_out

# Other Modules
from datetime import datetime
import os
import warnings
import traceback
import pickle
import copy


class MusicGenerator(object):
    """
    A magical deity capable of generating music based on a predefined style
    """

    def __init__(self, style_probs=None, composition_title='Untitled',
                 author_name='By: Al Gogh Rhythm'):
        """
        Constructor

        :param style_probs: A Style object to represent a certain musical style. Holds
                            the probabilities for scales, keys, note timings, modes, etc.
        :param composition_title: Title for the work, used for generated files
        :param author_name: Name of the author, used for generated files
        """
        self.composition = mingus_composition.Composition()

        # If Style not provided, use default
        if style_probs is None:
            self.style_probs = Style(style.DEFAULT_CFG_FILE)
        else:
            self.style_probs = style_probs

        self.composition_title = composition_title
        self.author_name = author_name

        self._time_signature = choice.choose_time_signature(self.style_probs)
        self._key = choice.choose_key(self.style_probs.probabilities['keys'])

    def create_melody_track(self, num_bars, style=None, octave_adjust=0):
        """
        Creates a mingus Track containing bars of randomly generated melodies to
        the composition.

        :param num_bars: The number of bars to add to the track
        :param style: The musical Style for the track, overrides the generator's
        :param octave_adjust: Adjustment of the octave of notes in the generated bars (+/- int)
        """

        if style is None:
            style = self.style_probs

        # Check if it's a major key
        major_key_bool = self._key.istitle()

        # Add a track with the given style
        melody_track = track.Track(style=style)

        # Determine scale based on key
        if major_key_bool:
            scale = choice.choose_scale(self._key, style.probabilities['major_scales'])
        else:
            # Only accepts all uppercase when determining scale from key
            key = self._key.upper()
            scale = choice.choose_scale(key, style.probabilities['minor_scales'])

        for _ in range(0, num_bars):
            # Create time for melody
            melody_timing = self._create_melody_timing(style.probabilities['timings'])

            # Determine number notes in melody
            number_notes = time.get_notes_in_timing(melody_timing)

            # Choose notes for melody based on scale for given key
            chosen_notes = choice.choose_notes(number_notes, scale)

            if octave_adjust != 0:
                # Adjust octave
                chosen_notes = convert.alter_octave(chosen_notes,
                                                    octave_adjust)

            # Combine melody time and notes into a mingus Bar object
            bar_to_add = convert.convert_notes_to_bar(self._key, melody_timing,
                                                      chosen_notes,
                                                      self._time_signature)

            # Add bar to track
            melody_track.add_bar(bar_to_add)

        return melody_track

    def create_chords_track(self, num_bars=None, style=None, melody_track=None,
                            octave_adjust=0, force_mode_scale=False):
        """
        Create a track to the composition filled with chords

        :param num_bars: The number of bars to add to the track
        :param style: The musical Style for the track
        :param melody_track: Melody track to base the chords track off of TODO: Unused
        :param octave_adjust: Adjustment of the octave of notes in the generated bars
        :param force_mode_scale: Force a certain mode for a scale TODO: Unused
        TODO: Create chord length other than all whole notes
        """

        if style is None:
            style = self.style_probs

        # Create chord progression
        progression_probs = style.probabilities['progressions']

        if force_mode_scale:
            # TODO: Do something with mode?
            pass
        else:
            pass

        if num_bars is not None:
            # Make sure there is a possible chord progression of the length they specify
            found_possible_match = False
            matches = []
            repeat_times_to_fill = 0

            # Find all the possible progressions to match given length
            for key, prob in progression_probs:
                chords = key.split(' ')
                if num_bars % len(chords) == 0:
                    found_possible_match = True
                    matches.append((key, prob))

            # TODO: Retain relative probabilities
            # For now, just make probabilities of possible matches all equal
            temp_matches = matches
            matches = []
            for key, prob in temp_matches:
                matches.append((key, 1.0 / (len(temp_matches))))

            if found_possible_match:
                raw_chord_progression = choice.choose_chord_progression(matches)
                repeat_times_to_fill = int(num_bars / len(raw_chord_progression))

                # Repeat chords as necessary to fill up bars to number specified
                raw_chord_progression = self._repeat_chords_track(raw_chord_progression,
                                                                  repeat_times_to_fill)

            else:
                raise AttributeError('Cannot find a chord progression to' +
                                     ' meet the requirement' + ' for ' +
                                     str(num_bars) + ' bars.')

        # Number of bars was not specified, just pick a single chord progression
        else:
            raw_chord_progression = choice.choose_chord_progression(progression_probs)

        chord_progression_notes = progressions.to_chords(raw_chord_progression,
                                                         self._key)

        # Adjust octave
        chord_progression = convert.alter_octave(chord_progression_notes,
                                                 octave_adjust)

        # Convert it to a mingus track
        chord_track = convert.convert_chord_progression_to_track(self._key, chord_progression,
                                                                 self._time_signature)
        chord_track.style_probs = style

        return chord_track

    def insert_track(self, track, location_to_add=1, times_to_repeat=0):
        new_track = copy.deepcopy(track)

        # Repeat chords per argument
        new_track.bars += new_track.bars * times_to_repeat

        # Add empty bars to the front of the new_track to place melody at the
        # location specified. Note: Start at Bar #1
        if location_to_add > 1:
            empty_bars_to_add = location_to_add - 1
            new_track = time.prepend_empty_bars_to_track(new_track,
                                                     empty_bars_to_add)

        self.composition.add_track(new_track)

    def remove_track(self, index=None):
        """
        Removes a track from the composition

        :param index: Index of track in composition track list to remove
        """
        # If no index is specified, remove last track
        if index is None:
            index = len(self.composition.tracks) - 1

        if index >= len(self.composition.tracks) or index < 0:
            raise IndexError('Cannot remove track at index ' + str(index) + ' because '
                             'that index is out of bounds.')

        self.composition.tracks.pop(index)

    def set_time_signature(self, time_signature):
        """
        Set the time signature for the composition.

        :param time_signature: The musical time signature to set for a composition. Format: (3,4) for 3/4, (4,4) for 4/4, etc.
        """
        if meter.is_valid(time_signature):
            self._time_signature = time_signature
        else:
            raise AttributeError(str(time_signature) + ' is not a valid time signature.',
                                 UserWarning)

    def set_key(self, key):
        """
        Set the key for the composition. Will randomly choose key by using the
        probabilities in configuration file if one is not provided

        :param key: Musical key to use
        """
        if keys.is_valid_key(key):
            self._key = key
        else:
            raise AttributeError(str(key) + ' is not a valid key.', UserWarning)

    def export_pdf(self, file_path):
        """
        Outputs a pdf to a specified path

        :param file_path: Path to the file to generate. Put / at end to use
                          default naming in directory specified. Otherwise
                          provide full path. DO NOT use relative pathing.
        """
        if file_path is None:
            warnings.warn('PDF not generated. Please specify valid path.',
                          UserWarning)
            traceback.print_stack()
            return

        # Lilypond doesn't like it if the file path already ends in .pdf
        if file_path.lower()[-4:] == '.pdf':
            file_path = file_path[:-4]

        file_path = MusicGenerator._create_file_path(file_path, '')

        # Output the pdf score
        ly_string = LilyPond.from_Composition(self.composition)
        if ly_string and self.composition.tracks:
            LilyPond.to_pdf(ly_string, file_path,
                            lilypond_installation=cfg_import.config.LILYPOND_INSTALLATION)
        else:
            warnings.warn('PDF not generated because the composition didn\'t ' +
                          'have any tracks. :(', UserWarning)
            traceback.print_stack()

        return file_path + '.pdf'

    def export_midi(self, file_path, bpm=100, repeat=0, verbose=False):
        """
        Outputs a midi to a specified path

        :param file_path: Path to the file to generate. Put / at end to use
                          default naming in directory specified. Otherwise
                          provide full path. DO NOT use relative pathing.
        """
        if file_path is None:
            warnings.warn('MIDI not generated. Please specify valid path.',
                          UserWarning)
            traceback.print_stack()
            return

        file_path = MusicGenerator._create_file_path(file_path, 'mid')

        # Output a midi file
        if self.composition is not None and self.composition.tracks:
            midi_file_out.write_Composition(file_path, self.composition,
                                            bpm, repeat, verbose)
        else:
            warnings.warn('MIDI not generated because the composition didn\'t' +
                          ' have any tracks. :(', UserWarning)
            traceback.print_stack()

        return file_path

    def export_pickle(self, file_path, protocol_to_use=pickle.HIGHEST_PROTOCOL):
        """
        Outputs a python pickled object to a specified path

        :param file_path: Path to the file to generate. Put / at end to use
                          default naming in directory specified. Otherwise
                          provide full path. DO NOT use relative pathing.
        """
        if file_path is None or file_path == '':
            warnings.warn('Pickle not generated. Please specify valid path.',
                          UserWarning)
            traceback.print_stack()
            return

        file_path = MusicGenerator._create_file_path(file_path, 'pkl')

        with open(file_path, 'wb') as file:
            pickle.dump(self, file, protocol=protocol_to_use)

        return file_path

    @staticmethod
    def _create_file_path(file_path, file_extension=None):
        """
        Returns a file path and creates folders if necessary. If a path is given,
        a filename is generated using current time and file_extension provided is
        appended.

        :param file_path: Path to filename with extension or path to directory
        :param file_extension: Extension for file if file_path is a dir. Ex: pdf
        """
        if file_path is None or file_path == '':
            return None

        file_path = file_path.strip()

        if file_path.endswith('/') or file_path.endswith('\\'):
            if file_extension is None:
                raise AttributeError('Provide file_extension if only providing path: ' + file_path)

            # Make folder if necessary
            if not os.path.exists(file_path):
                os.makedirs(file_path)

            # Create filename based on key and time
            file_path = (file_path + '/' +
                         str(datetime.now()).replace(' ', '_').replace(':', '.') +
                         '.' + file_extension)
        else:
            file_path = os.path.abspath(file_path)

            # Make folder if necessary
            dir_path = os.path.dirname(file_path)
            if not os.path.isdir(dir_path):
                os.makedirs(dir_path)

        return file_path

    def _create_melody_timing(self, note_timing_prob_list):
        """
        Returns a list of note lengths representing the time of a melody for a
        single bar.

        :param note_timing_prob_list: List of tuples with note timings and
                                      associated probabilities
        """
        melody_bar = []

        # If valid time signature is supplied, use it to craft melody, otherwise
        # use common time
        if not meter.is_valid(self._time_signature):
            raise AttributeError('Time signature: ' + self._time_signature +
                                 ' cannot be converted to a mingus meter. ' +
                                 'Use tuple (#, #) format. Ex: (4, 4)')
        else:
            remaining_time_in_bar = time.get_time_remaining(melody_bar,
                                                            self._time_signature)

            # Continue getting note progressions as long as there's room in bar
            while (remaining_time_in_bar > 0.0):
                next_timing = choice.choose_next_timing(remaining_time_in_bar,
                                                        note_timing_prob_list)

                melody_bar.append(next_timing)

                remaining_time_in_bar = time.get_time_remaining(melody_bar,
                                                                self._time_signature)

        return melody_bar

    def __str__(self):
        """
        Returns a string representation of the class.
        """
        output = ''
        output += 'Time Signature: ' + str(self._time_signature) + '\n'
        output += '           Key: ' + str(self._key) + '\n'
        output += '\n'

        if self.composition is not None:
            for index, track in enumerate(self.composition):
                # I guess I should start at 1... ugh.
                index += 1

                output += ('================================== TRACK ' +
                           str(index) + ' ')
                output += '=' * (38 - len(str(index)))
                output += '\n'

                for index, bar in enumerate(track):
                    # I guess I should start at 1... again... ugh.
                    index += 1

                    output += ('----------------------------------- Bar ' +
                               str(index) + ' ')
                    # Adjust line based on size of index (ex: two less '-' for
                    # 2-digit number)
                    output += '-' * (39 - len(str(index)))
                    output += '\n'
                    output += str(bar) + '\n'

        output += ('--------------------------------------------------------' +
                   '------------------------\n')
        return output

    @staticmethod
    def from_pickle(pickle_file_name):
        pkl_file = open(pickle_file_name, 'rb')
        music_generator = pickle.load(pkl_file)
        return music_generator

    @staticmethod
    def _repeat_chords_track(raw_chord_progression, times_to_repeat):
        """
        Returns an extended raw chord list which is the original repeated a
        number of times

        :param raw_chord_progression: List of notes representing chord progression
        :param times_to_repeat: How many times to repeat the chords
        """
        # Repeat chords per argument
        extended_chord_progression = []
        for _ in range(0, times_to_repeat):
            for item in raw_chord_progression:
                extended_chord_progression.append(item)
        return extended_chord_progression
