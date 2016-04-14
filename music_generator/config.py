
# Other Modules
import ConfigParser

# Global config dictionary to access data from parsed files
config = dict()
    
def configure_probabilities(file_name='probabilities.cfg'):
    '''
    Parses the .cfg file to retrieve all the probabilities and saves them in a global dictionary
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
            parsed_values = [item[1]]
            section_to_add.append((item[0], parsed_values))
            
        # Sort it by probability (convert to list)
        sorted_section = sorted(section_to_add, key=lambda section_to_add: section_to_add[1])
        config[section] = sorted_section
    
    if 'progressions' not in config.keys():
        raise Exception('Missing \'progressions\' section in cfg file.')
    
    if 'keys' not in config.keys():
        raise Exception('Missing \'keys\' section in cfg file.')
        
    if 'timings' not in config.keys():
        raise Exception('Missing \'timings\' section in cfg file.')
