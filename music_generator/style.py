'''
Created on Apr 27, 2016

@author: Alex VanTol
'''

# Other Modules
import ConfigParser
import os

# Configuration
_PATH_TO_SCRIPT = os.path.dirname(os.path.abspath(__file__))
DEFAULT = _PATH_TO_SCRIPT + '/../styles/default.cfg'
JAZZ    = _PATH_TO_SCRIPT + '/../styles/jazz.cfg'

class Style(object):
    '''
    classdocs
    '''

    def __init__(self, probabilities_file):
        '''
        Constructor
        '''
        self.probabilities = dict()
        self.parse_probabilities_file(probabilities_file)

    def parse_probabilities_file(self, file_name):
        '''
        Parses the .cfg file to retrieve all the probabilities
        TODO: Add a check to make sure all probabilities in a section add up to 1.0
        '''
        config_parser = ConfigParser.ConfigParser()

        # Option here forced case sensitivity during parsing
        config_parser.optionxform = str

        # Attempt to import the cfg file, this could fail if format is wrong
        try:
            config_parser.readfp(open(file_name))
        except Exception as exc:
            raise exc

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

        if 'modes' not in self.probabilities.keys():
            raise Exception('Missing \'modes\' section in cfg file.')

        if 'minor_scales' not in self.probabilities.keys():
            raise Exception('Missing \'minor_scales\' section in cfg file.')

        if 'major_scales' not in self.probabilities.keys():
            raise Exception('Missing \'major_scales\' section in cfg file.')
