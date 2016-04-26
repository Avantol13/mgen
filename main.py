#!/usr/bin/python2
'''
Created on Jan 21, 2016

@author: Alex VanTol

TODO: Use http://www.sphinx-doc.org/en/stable/tutorial.html for documentation
'''

# Project Modules
from MusicGenerator import MusicGenerator

def main():
    my_generator = MusicGenerator()
    my_generator.add_melody_track(8)
    my_generator.add_chords_track(8, octave_adjust=-1)
    my_generator.export_pdf()
    my_generator.export_midi(bpm=90)
    print(my_generator)
    
if __name__ == '__main__':
    main()

    