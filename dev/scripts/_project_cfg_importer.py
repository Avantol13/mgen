"""
Project Configuration Importer

Handles the importing the project configuration from a separate location
and validates the version against the specified expected version.

NOTE: If you update this file or any others in scripts and require a
      NEW variable in project_cfg, then you need to UPDATE THE EXPECTED_CFG_VERSION

      That way, if someone tries to use the new scripts with an old cfg, they'll
      get a warning.
"""

import importlib
import os
import sys

PROJECT_CFG_DIR = os.path.realpath(os.path.dirname(__file__) + "/../../cfg/")
PROJECT_CFG_NAME = "project_cfg"
EXPECTED_CFG_VERSION = 1.0


def get_project_cfg():
    """
    Returns the project configuration module
    """
    sys.path.append(PROJECT_CFG_DIR)
    try:
        project_cfg_module = importlib.import_module(PROJECT_CFG_NAME)
    except:
        raise FileNotFoundError("\n\n================================= ERROR ========================================"
                                "\nUnable to import project configuration: " + PROJECT_CFG_DIR + "/" + PROJECT_CFG_NAME + ".py"
                                "\n================================================================================\n")

    _verify_correct_version(project_cfg_module)

    return project_cfg_module


def _verify_correct_version(project_cfg_module):
    is_correct_version = False
    if project_cfg_module.__CFG_VERSION__ == EXPECTED_CFG_VERSION:
        is_correct_version = True
    else:
        raise Exception("\n\n================================= ERROR ========================================"
                        "\nIncorrect project configuration version: " + str(project_cfg_module.__CFG_VERSION__) +
                        "\n       Development environment expected: " + str(EXPECTED_CFG_VERSION) +
                        "\n================================================================================\n")

    return is_correct_version
