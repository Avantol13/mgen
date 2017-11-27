"""
Configuration Importer

Handles the importing the project configuration
from a separate location.
"""
import importlib
import os
import sys

global config
EXPECTED_CFG_VERSION = 1.1

def set_global_config(config_module_path):
    """
    Sets the global configuration variable to
    the module specified in the path

    :param config_module_path: A path
                               to a .py configuration file
    """
    config_module = _get_cfg_from_path(config_module_path)

    global config
    config = config_module


def _get_cfg_from_path(config_module_path):
    """
    Returns the project configuration module

    :param config_module_path: A path
                               to a .py configuration file
    """
    try:
        cfg_dir = os.path.dirname(config_module_path)
        cfg_file = os.path.basename(config_module_path)
    except:
        raise Exception(
            "\nCould not import configuration. "
            "config_module_path was not valid: " + config_module_path
        )

    sys.path.append(cfg_dir)

    try:
        project_cfg_module = importlib.import_module(cfg_file.replace(".py", ""))
    except:
        raise FileNotFoundError(
            "\nUnable to import project configuration: " + config_module_path
        )

    _verify_correct_version(project_cfg_module, config_module_path)

    return project_cfg_module


def _verify_correct_version(project_cfg_module, config_module_path):
    if project_cfg_module.__version__ != EXPECTED_CFG_VERSION:
        raise Exception("\nIncorrect project configuration version: " +
                        str(project_cfg_module.__VERSION__) +
                        "\n         Execution environment expected: " +
                        str(EXPECTED_CFG_VERSION) +
                        "\n\nConfiguration File: " +
                        str(config_module_path))

# Default config to the default location (can be reset with set_global_config)
set_global_config(os.path.dirname(os.path.abspath(__file__)) + "/../cfg/config.py")
