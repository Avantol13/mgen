"""
Configuration
"""
import os

CFG_DIR = os.path.dirname(os.path.realpath(__file__))
# LILYPOND_INSTALLATION = 'lilypond'
# *nix users who didn't modify their path after getting lilypond, the default location is below
LILYPOND_INSTALLATION = '/home/$USER/bin/lilypond'

__version__ = 1.0
