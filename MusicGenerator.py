'''
Created on Apr 25, 2016

@author: Alex VanTol
'''

# Project Modules
from music_generator import convert
from music_generator import timing

# Mingus modules
import mingus.core.progressions as progressions
import mingus.core.meter as meter
import mingus.containers.composition as composition
import mingus.containers.track as track
import mingus.extra.lilypond as LilyPond
import mingus.core.value as value
from mingus.midi import midi_file_out

# Other Modules
import ConfigParser
import random
from datetime import datetime
import os

class MusicGenerator(object):
    '''
    classdocs
    '''

    def __init__(self, config_file='probabilities.cfg', composition_title='Untitled',
                 author_name='By: Al Gogh Rhymth'):
        '''
        Constructor
        '''
        
        self.probabilities = dict()
        
        # Attempt to import the cfg file, this could fail if format is wrong
        try:
            self.import_probabilities(config_file)
        except Exception as exc:
            # Raise up
            raise exc
        
        self.__composition = composition.Composition()
        self.set_time_signature()
        self.set_key()
    
    def add_melody_track(self, num_bars): 
        '''
        Adds a mingus Track containing bars of randomly generated melodies to the composition.
        '''
        melody_track = track.Track()
                
        # Get scale based on key
        scale = convert.convert_to_scale(self.__key)
        
        for index in range(0, num_bars):
            print('--------------------------------- Bar ' + str(index) + ' ----------------------------------')
        
            # Create timing for melody
            melody_timing = self._create_melody_timing()
            print(' Melody Timing: ' + str(melody_timing))
            
            # Determine number notes in melody
            number_notes = timing.get_notes_in_timing(melody_timing)
            
            # Choose notes for melody based on scale for given key
            chosen_notes = self.choose_notes(number_notes, scale)
            print('  Chosen Notes: ' + str(chosen_notes))
            
            # Combine melody timing and notes into a mingus Bar object
            bar_to_add = convert.convert_notes_to_bar(self.__key, melody_timing, chosen_notes, self.__time_signature)
            
            #print('TESTING STUFF...')
            #print(bar_to_add.determine_chords(shorthand=True))
            #print(bar_to_add.determine_progression(shorthand=True))
            
            # Add bar to track
            melody_track.add_bar(bar_to_add)
        
        self.__composition.add_track(melody_track)
    
    def add_chords_track(self, num_bars=None, octave_adjust=0):
        '''
        Adds a track to the composition filled with chords
        TODO: Create chord length other than all whole notes
        '''
        # Create chord progression
        progression_probs = self.probabilities['progressions']
        
        if num_bars:
            # Make sure there is a possible chord progression of the length they specify
            found_possible_match = False
            matches = []
            times_to_repeat = 1
            
            # Find all the possible progressions to match given length
            for key, value in progression_probs:
                chords = key.split(' ')
                if num_bars%len(chords) == 0:
                    found_possible_match = True
                    matches.append((key, value))
            
            # TODO: Retain relative probabilties
            # For now, just make probabilities of possible matches all equal
            temp_matches = matches
            matches = []
            for key, value in temp_matches:
                matches.append((key, 1.0/(len(temp_matches))))
            
            if found_possible_match:
                raw_chord_progression = self.choose_chord_progression(matches)
                times_to_repeat = num_bars/len(raw_chord_progression)
            
                # Repeat chords as necessary to fill up bars to number specified
                extended_chord_progression = []
                for index in range(0, times_to_repeat):
                    for item in raw_chord_progression:
                        extended_chord_progression.append(item)
            
                raw_chord_progression = extended_chord_progression
            else:
                raise AttributeError('Cannot find a chord progression to meet the requirement' + \
                                     ' for ' + str(num_bars) + ' bars.' )
                
        # Number of bars was not specified, just pick a single chord progression 
        else:
            raw_chord_progression = self.choose_chord_progression(progression_probs)
                
        print('   Progression: ' + str(raw_chord_progression))
        chord_progression_notes = progressions.to_chords(raw_chord_progression, self.__key)
        
        # Adjust octave
        chord_progression = convert.change_octave(chord_progression_notes, octave_adjust)
        
        chord_track = convert.convert_chord_progression_to_track(self.__key, chord_progression, self.__time_signature)
        
        self.__composition.add_track(chord_track)
    
    def remove_track(self, index=None):
        '''
        Removes a track from the composition
        '''
        # If no index is specified, remove last track
        if not index:
            index = len(self.composition.tracks) -1
        
        if index >= len(self.composition.tracks):
            raise IndexError('Provided index for track in composition is out of bounds.')
        
        self.composition.tracks.pop(index)
    
    def reset(self):
        self.__composition = composition.Composition()
        self.__key = self.set_key()
        self.__time_signature = self.set_time_signature()
    
    def set_time_signature(self, time_signature=None):
        '''
        Set the time signature for the composition.
        TODO: Validate input
        '''
        if time_signature:
            self.__time_signature = time_signature
        else:
            self.__time_signature = self.choose_time_signature()

    def set_key(self, key=None): 
        '''
        Set the key for the composition. Will randomly choose key by using the probabilities 
        in configuration file if one is not provided.
        TODO: Validate input
        '''
        key_probs = self.probabilities['keys']
        
        if key:
            self.__key = key
        else:
            self.__key = self.choose_key(key_probs)
    
    def export_pdf(self, file_path=None):
        '''
        Outputs a pdf to a specified path
        '''
        if not file_path:
            # Create filename based on key and time
            file_path = str(os.getcwd()) + '\output\key_' + self.__key + '_' + str(datetime.now()).replace(' ', '_').replace(':', '.')

        # Output the pdf score
        LilyPond.to_pdf(LilyPond.from_Composition(self.__composition), file_path)
    
    def export_midi(self, file_name=None, bpm=100, repeat=0, verbose=False):
        '''
        Outputs a pdf to a specified path
        '''
        if not file_name:
            # Create filename based on key and time
            file_name = str(os.getcwd()) + '\output\key_' + self.__key + '_' + str(datetime.now()).replace(' ', '_').replace(':', '.')

        # Output a midi file
        midi_file_out.write_Composition(file_name + '.mid', self.__composition, bpm, repeat, verbose)

    def import_probabilities(self, file_name):
        '''
        Parses the .cfg file to retrieve all the probabilities
        TODO: Add a check to make sure all probabilities in a section add up to 1.0
        '''
        config_parser = ConfigParser.ConfigParser()
        
        # Option here forced case sensitivity during parsing
        config_parser.optionxform = str
        
        # Parse the file for probabilities
        config_parser.readfp(open(file_name))
        
        # Parse config data from file
        for section in config_parser.sections():
            section_to_add = []
            for item in config_parser.items(section):
                # Grab the key and create a list
                parsed_values = item[1]
                section_to_add.append((item[0], parsed_values))
                
            # Sort it by probability (convert to list)
            sorted_section = sorted(section_to_add, key=lambda section_to_add: section_to_add[1])
            self.probabilities[section] = sorted_section
        
        if 'progressions' not in self.probabilities.keys():
            raise Exception('Missing \'progressions\' section in cfg file.')
        
        if 'keys' not in self.probabilities.keys():
            raise Exception('Missing \'keys\' section in cfg file.')
            
        if 'timings' not in self.probabilities.keys():
            raise Exception('Missing \'timings\' section in cfg file.')
    
    def __str__(self):
        '''
        Returns a string representation of the class.
        TODO: Cleanup output of bars to make it more user friendly?
        '''
        output = ''
        output += '---------------------------------------------------------------------------\n'
        output += '----------------------------- Music Generator -----------------------------\n'
        output += '---------------------------------------------------------------------------\n\n'
        output += 'Time Signature: ' + str(self.__time_signature) + '\n'
        output += '           Key: ' + str(self.__key) + '\n'
        output += '         Scale: ' + str(convert.convert_to_scale(self.__key)) + '\n'
        
        # I guess I should start at 1... ugh.
        count = 1
        for track in self.__composition:
            output += 'Track ' + str(count) + '\n'
            count += 1
            for bar in track:
                output += str(bar) + '\n'
        
        output += '---------------------------------------------------------------------------\n\n'
        return output
    
    def _create_melody_timing(self):
        '''
        Returns a list of note lengths representing the timing of a melody for a single bar.
        '''
        melody_bar = []
        
        # If valid time signature is supplied, use it to craft melody, otherwise use common time
        if not meter.is_valid(self.__time_signature):
            raise AttributeError('Time signature: ' + self.__time_signature + ' cannot be converted to a mingus meter. ' +
                             'Use tuple (#, #) format. Ex: (4, 4)')
        else:
            remaining_time_in_bar = timing.get_time_remaining(melody_bar, self.__time_signature)
            
            # Continue getting note progressions as long as they're room in the bar
            while (remaining_time_in_bar > 0.0):
                note_timing_probs = self.probabilities['timings']
                next_timing = self.get_next_timing(remaining_time_in_bar, note_timing_probs)
                            
                melody_bar.append(next_timing)
                
                remaining_time_in_bar = timing.get_time_remaining(melody_bar, self.__time_signature)
        
        return melody_bar
    
    @staticmethod
    def choose_key(key_probs):
        '''
        Return a randomly chosen key by using the provided probability dictionary.
        '''
        choice = random.uniform(0, 1) 
        
        for key, value in key_probs:
            # Subtract the probability from the choice
            choice = choice - float(value)
            
            # When it reaches zero, we've hit our choice
            if choice <= 0:
                return key
    
    @staticmethod
    def choose_time_signature():
        '''
        Return a randomly chosen time signature by using the provided probability dictionary.
        TODO: Actually make this random (create probability in cfg file for time sigs)
        '''
        return meter.common_time
    
    @staticmethod
    def choose_chord_progression(progression_probs):
        '''
        Return a randomly chosen chord progression by using the provided probability dictionary.
        '''
        choice = random.uniform(0, 1)  
        
        for chords, prob in progression_probs:
            # Subtract the probability from the choice
            choice = choice - float(prob)
            
            # When it reaches zero, we've hit our choice
            if choice <= 0:
                # Create a list of the chords
                return chords.split(' ')
            
    @staticmethod
    def choose_notes(number_notes, scale):
        '''
        Returns a list of notes chosen randomly from a given scale.
        '''
        notes_in_scale = len(scale)
        notes = []
        
        while (len(notes) < number_notes):
            # values less than 0 will result in a rest
            choice = random.randint(-3, notes_in_scale-1) 
            if choice >= -1:
                notes.append(scale[choice])
            else:
                # Place a rest
                notes.append(None)
                
        return notes
    
    @staticmethod
    def get_next_timing(remaining_time_in_bar, note_timing_prob_dict):
        '''
        Returns a "timing" representing a series of notes that will fit in the remaining portion of the bar.
        '''
        if remaining_time_in_bar > 0.0:
            # The chosen timing progression
            the_chosen_one = None 
            
            # Whether or not we've found The Chosen One
            the_chosen_one_found = False
            
            # Random choice
            choice = random.uniform(0, 1)  
            
            # As long as we haven't found The Chosen One, keep trying.
            # Centuries may pass... but The Chosen One will be found (hopefully).
            while (not the_chosen_one_found and choice >= 0):
                choice = random.uniform(0, 1)  
                 
                # Sort by the probability 
                #config.timing_probabilities.sort(key=lambda timing_probabilities: timing_probabilities[0])
                
                for key, val in note_timing_prob_dict:
                    # Subtract the probability from the choice
                    choice = choice - float(val)
                    
                    # When it reaches zero, we've hit our choice
                    if choice <= 0:
                        progression = []
                        parsed_progression = key.split(' ')
                        for item in parsed_progression:
                            item = item.replace('\'', '')
                            progression.append(eval(item))
                        
                        # If there's room in the measure
                        time_for_choice = timing.get_notes_length(progression)
                        
                        if (remaining_time_in_bar >= time_for_choice):
                            the_chosen_one_found = True
                            the_chosen_one = progression
                            break
        else:
            '''
            TODO: handle this better
            '''
            return None
        
        return the_chosen_one
    