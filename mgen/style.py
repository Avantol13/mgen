"""
Style is a reflection of your attitude and your personality.
    - Shawn Ashmore
"""

# Other Modules
import json
import operator
import os

DEFAULT_CFG_FILE = (  os.path.dirname(os.path.abspath(__file__))
                    + "/../styles/default.json")
JAZZ_CFG_FILE = (  os.path.dirname(os.path.abspath(__file__))
                 + "/../styles/jazz.json")

REQUIRED_STYLE_CFG_VERSION = "1.0"

class StyleProbs(object):
    """
    A representation of a certain musical style. Holds the probabilities for
    scales, keys, note timings, modes, etc.
    """
    def __init__(self, probabilities_file):
        """
        Constructor

        :param probabilities_file: Cfg file to get probabilities from
        """
        self.probabilities = dict()
        self.parse_probabilities_file(probabilities_file)

    def parse_probabilities_file(self, file_name):
        """
        Parses the .cfg file to retrieve all the probabilities

        :param file_name: Cfg file to get probabilities from

        TODO: Add a check to make sure all probabilities in section add upto 1.0
        """
        # Attempt to import the cfg file, this could fail if format is wrong
        try:
            with open(file_name) as data_file:
                data = json.load(data_file)
        except Exception as exc:
            raise exc

        # Parse config data from file
        for section, section_items in data.items():
            # Sort it by probability (convert to list)
            sorted_section = sorted(section_items.items(),
                                    key=operator.itemgetter(1))
            self.probabilities[section] = sorted_section

        if "progressions" not in self.probabilities.keys():
            raise Exception("Missing \"progressions\" section in cfg file:"
                            "\n   " + file_name)

        if "keys" not in self.probabilities.keys():
            raise Exception("Missing \"keys\" section in cfg file:"
                            "\n   " + file_name)

        if "timings" not in self.probabilities.keys():
            raise Exception("Missing \"timings\" section in cfg file:"
                            "\n   " + file_name)

        if "modes" not in self.probabilities.keys():
            raise Exception("Missing \"modes\" section in cfg file:"
                            "\n   " + file_name)

        if "minor_scales" not in self.probabilities.keys():
            raise Exception("Missing \"minor_scales\" section in cfg file:"
                            "\n   " + file_name)

        if "major_scales" not in self.probabilities.keys():
            raise Exception("Missing \"major_scales\" section in cfg file:"
                            "\n   " + file_name)

        if (    ("__info__" not in data.keys())
             or ("__version__" not in data["__info__"].keys()) ):
            raise Exception("Missing \"__info__\" section in cfg file:"
                            "\n   " + file_name)

        if data["__info__"]["__version__"] != REQUIRED_STYLE_CFG_VERSION:
            raise Exception("Invalid style version: " +
                            "{} in cfg file:\n   {}\n".format(
                                data["__info__"]["__version__"], file_name
                             ) + "This version of mgen requires a style " +
                            "configuration with version: " +
                            "{}\n".format(REQUIRED_STYLE_CFG_VERSION))
