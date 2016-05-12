'''
Created on Apr 25, 2016

@author: Alex VanTol
'''

# Project Modules
from music_generator import convert
from music_generator import time
from music_generator import choice

# Mingus modules
import mingus.core.keys as keys
import mingus.containers.bar as bar
import mingus.core.progressions as progressions
import mingus.core.meter as meter
import mingus.containers.composition as mingus_composition
import mingus.containers.track as track
import mingus.extra.lilypond as LilyPond
from mingus.midi import midi_file_out

# Need scales import for eval() purposes, DON'T remove
import mingus.core.scales as scales

# Other Modules
from datetime import datetime
import os
import warnings
import traceback

class MusicGenerator(object):
    '''
    classdocs
    '''

    def __init__(self, style, composition_title='Untitled', author_name='By: Al Gogh Rhythm'):
        '''
        Constructor
        '''
        self.composition = mingus_composition.Composition()

        self.style = style
        self.composition.title = composition_title
        self.composition.author = author_name

        self.__time_signature = choice.choose_time_signature(self.style)
        self.__key = choice.choose_key(self.style.probabilities['keys'])

    def add_melody_track(self, num_bars, location_to_add=1, style=None, times_to_repeat=0, octave_adjust=0):
        '''
        Adds a mingus Track containing bars of randomly generated melodies to the composition.
        '''

        if style is None:
            style = self.style

        key = self.__key
        major_key_bool = key.istitle()

        melody_track = track.Track(style=style)

        # Determine scale based on key
        if major_key_bool:
            scale = choice.choose_scale(key, style.probabilities['major_scales'])
        else:
            # Only accepts all uppercase when determining scale from key
            key = key.upper()
            scale = choice.choose_scale(key, style.probabilities['minor_scales'])

        for index in range(0, num_bars):
            # Create time for melody
            melody_timing = self._create_melody_timing(style.probabilities['timings'])

            # Determine number notes in melody
            number_notes = time.get_notes_in_timing(melody_timing)

            # Choose notes for melody based on scale for given key
            chosen_notes = choice.choose_notes(number_notes, scale)

            # Combine melody time and notes into a mingus Bar object
            bar_to_add = convert.convert_notes_to_bar(self.__key, melody_timing, chosen_notes,
                                                      self.__time_signature)

            #print('TESTING STUFF...')
            #print(bar_to_add.determine_chords(shorthand=True))
            #print(bar_to_add.determine_progression(shorthand=True))

            # Add bar to track
            melody_track.add_bar(bar_to_add)

        # Repeat chords per argument
        melody_track.bars += melody_track.bars * times_to_repeat

        # Add empty bars to the front of the track to place melody at the location specified
        # Note: Start at Bar #1
        empty_bars_to_add = location_to_add - 1
        melody_track = time.prepend_empty_bars_to_track(melody_track, empty_bars_to_add)

        self.composition.add_track(melody_track)

    def add_chords_track(self, num_bars=None, location_to_add=0, style=None, melody_track=None, 
                         times_to_repeat=0, octave_adjust=0, force_mode_scale=False):
        '''
        Adds a track to the composition filled with chords
        TODO: Create chord length other than all whole notes
        '''

        if style is None:
            style = self.style

        # Create chord progression
        progression_probs = style.probabilities['progressions']

        if force_mode_scale:
            # Do something with mode?
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
                repeat_times_to_fill = num_bars / len(raw_chord_progression)

                # Repeat chords as necessary to fill up bars to number specified
                raw_chord_progression = self._repeat_chords_track(raw_chord_progression,
                                                                  repeat_times_to_fill)

            else:
                raise AttributeError('Cannot find a chord progression to meet the requirement' +
                                     ' for ' + str(num_bars) + ' bars.')

        # Number of bars was not specified, just pick a single chord progression
        else:
            raw_chord_progression = choice.choose_chord_progression(progression_probs)

        chord_progression_notes = progressions.to_chords(raw_chord_progression, self.__key)

        # Adjust octave
        chord_progression = convert.change_octave(chord_progression_notes, octave_adjust)

        # Convert it to a mingus track
        chord_track = convert.convert_chord_progression_to_track(self.__key, chord_progression,
                                                                 self.__time_signature)
        chord_track.style = style

        # Repeat chords per argument
        chord_track.bars += chord_track.bars * times_to_repeat

        # Add empty bars to the front of the track to place chords at the location specified
        # Note: Start at Bar #1
        empty_bars_to_add = location_to_add - 1
        chord_track = time.prepend_empty_bars_to_track(chord_track, empty_bars_to_add)

        self.composition.add_track(chord_track)

    def remove_track(self, index=None):
        '''
        Removes a track from the composition
        '''
        # If no index is specified, remove last track
        if index is None:
            index = len(self.composition.tracks) - 1

        if index >= len(self.composition.tracks):
            raise IndexError('Provided index for track in composition is out of bounds.')

        self.composition.tracks.pop(index)

    def set_time_signature(self, time_signature):
        '''
        Set the time signature for the composition.
        '''
        if meter.is_valid(time_signature):
            self.__time_signature = time_signature
        else:
            warnings.warn(time_signature + ' is not a valid time signature.', UserWarning)
            traceback.print_stack()

    def set_key(self, key):
        '''
        Set the key for the composition. Will randomly choose key by using the probabilities
        in configuration file if one is not provided.
        '''
        if keys.is_valid_key(key):
            self.__key = key
        else:
            warnings.warn(key + ' is not a valid key.', UserWarning)
            traceback.print_stack()

    def export_pdf(self, file_path=None):
        '''
        Outputs a pdf to a specified path
        '''
        if file_path is None:
            # Create filename based on key and time
            file_path = (str(os.getcwd()) + '\output\\' +
                         str(datetime.now()).replace(' ', '_').replace(':', '.'))

        # Output the pdf score
        ly_string = LilyPond.from_Composition(self.composition)
        if ly_string and self.composition.tracks:
            LilyPond.to_pdf(ly_string, file_path)
        else:
            warnings.warn('PDF not generated because the composition didn\'t have any tracks. :(',
                          UserWarning)
            traceback.print_stack()

    def export_midi(self, file_name=None, bpm=100, repeat=0, verbose=False):
        '''
        Outputs a pdf to a specified path
        '''
        if file_name is None:
            # Create filename based on key and time
            file_name = (str(os.getcwd()) + '\output\\' +
                         str(datetime.now()).replace(' ', '_').replace(':', '.'))

        # Output a midi file
        if self.composition is not None and self.composition.tracks:
            midi_file_out.write_Composition(file_name + '.mid', self.composition, bpm,
                                            repeat, verbose)
        else:
            warnings.warn('PDF not generated because the composition didn\'t have any tracks. :(',
                          UserWarning)
            traceback.print_stack()

    def __str__(self):
        '''
        Returns a string representation of the class.
        '''
        output = ''
        output += '----------------------------------------------------------------------------\n'
        output += '------------------------------ Music Generator -----------------------------\n'
        output += '----------------------------------------------------------------------------\n\n'
        output += 'Time Signature: ' + str(self.__time_signature) + '\n'
        output += '           Key: ' + str(self.__key) + '\n'
        output += '\n'

        if self.composition is not None:
            for index, track in enumerate(self.composition):
                # I guess I should start at 1... ugh.
                index += 1

                output += '================================== TRACK ' + str(index) + ' '
                output += '=' * (35 - len(str(index)))
                output += '\n'

                for index, bar in enumerate(track):
                    # I guess I should start at 1... again... ugh.
                    index += 1

                    output += '----------------------------------- Bar ' + str(index) + ' '
                    # Adjust line based on size of index (ex: two less '-' for 2-digit number)
                    output += '-' * (36 - len(str(index)))
                    output += '\n'
                    output += str(bar) + '\n'

        output += '-----------------------------------------------------------------------------\n'
        return output

    def _create_melody_timing(self, note_timing_dict):
        '''
        Returns a list of note lengths representing the time of a melody for a single bar.
        '''
        melody_bar = []

        # If valid time signature is supplied, use it to craft melody, otherwise use common time
        if not meter.is_valid(self.__time_signature):
            raise AttributeError('Time signature: ' + self.__time_signature +
                                 ' cannot be converted to a mingus meter. ' +
                                 'Use tuple (#, #) format. Ex: (4, 4)')
        else:
            remaining_time_in_bar = time.get_time_remaining(melody_bar, self.__time_signature)

            # Continue getting note progressions as long as they're room in the bar
            while (remaining_time_in_bar > 0.0):
                next_timing = choice.choose_next_timing(remaining_time_in_bar, note_timing_dict)

                melody_bar.append(next_timing)

                remaining_time_in_bar = time.get_time_remaining(melody_bar, self.__time_signature)

        return melody_bar

    @staticmethod
    def _repeat_chords_track(raw_chord_progression, times_to_repeat):
        '''
        Returns an extended raw chord list which is the original repeated a number of times
        '''
        # Repeat chords per argument
        extended_chord_progression = []
        for index in range(0, times_to_repeat):
            for item in raw_chord_progression:
                extended_chord_progression.append(item)
        return extended_chord_progression

    