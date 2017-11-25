'''
Style is a reflection of your attitude and your personality.
    - Shawn Ashmore
'''

# Other Modules
import config
import json
import operator
import pprint

DEFAULT_CFG_FILE = config._PATH_TO_SCRIPT + '/../styles/default.json'
JAZZ_CFG_FILE    = config._PATH_TO_SCRIPT + '/../styles/jazz.json'

class StyleProbs(object):
    '''
    A representation of a certain musical style. Holds the probabilities for
    scales, keys, note timings, modes, etc.
    '''
    def __init__(self, probabilities_file):
        '''
        Constructor

        :param probabilities_file: Cfg file to get probabilities from
        '''
        self.probabilities = dict()
        self.parse_probabilities_file(probabilities_file)

    def parse_probabilities_file(self, file_name):
        '''
        Parses the .cfg file to retrieve all the probabilities

        :param file_name: Cfg file to get probabilities from

        TODO: Add a check to make sure all probabilities in a section add up to 1.0
        '''
        # Attempt to import the cfg file, this could fail if format is wrong
        try:
            with open(file_name) as data_file:
                data = json.load(data_file)
        except Exception as exc:
            raise exc

        # Parse config data from file
        for section, section_items in data.items():
            # Sort it by probability (convert to list)
            sorted_section = sorted(section_items.items(), key=operator.itemgetter(1))
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
