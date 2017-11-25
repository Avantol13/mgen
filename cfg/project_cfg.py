import os

PROJECT_NAME = "mgen"

PYTHON_2_EXECUTABLE = "py -2"
PYTHON_3_EXECUTABLE = "py -3"
DEFAULT_PYTHON_EXECUTABLE = PYTHON_2_EXECUTABLE

#             0 = The tool will just use the DEFAULT_PYTHON_EXECUTABLE for testing
# Anything else = Will run tests under PYTHON_2_EXECUTABLE and PYTHON_3_EXECUTABLE
IS_PYTHON_2_AND_3_COMPATIBLE = 0

# Make sure these paths are absolute
PROJECT_CFG_DIR = os.path.normpath(os.path.dirname(os.path.realpath(__file__)))
DEVELOPMENT_DIR = os.path.abspath(PROJECT_CFG_DIR + "/../dev")
SOURCE_CODE_DIR = os.path.abspath(PROJECT_CFG_DIR + "/../")
TEST_DIR        = os.path.abspath(DEVELOPMENT_DIR + "/unittests")
SCRIPTS_DIR     = os.path.abspath(DEVELOPMENT_DIR + "/scripts")

DEVEL_REQUIREMENTS_FILE = os.path.abspath(DEVELOPMENT_DIR + "/devel_requirements.txt")
REQUIREMENTS_FILE = os.path.abspath(DEVELOPMENT_DIR + "/../requirements.txt")

COVERAGE_OUTPUT_DIR = os.path.abspath(DEVELOPMENT_DIR + "/_coverage")

# Delimit with ,'s and don't put spaces
COVERAGE_IGNORE_FILES = "*mingus/*,*dev/*,*cfg/*,mgen_cli.py,setup.py,cfg_import.py,"

DOCUMENTATION_DIR = os.path.abspath(DEVELOPMENT_DIR + "/docs")

__CFG_VERSION__ = 1.0
