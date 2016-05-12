#!/usr/bin/python2
'''
Created on Jan 21, 2016

@author: Alex VanTol

TODO: Use http://www.sphinx-doc.org/en/stable/tutorial.html for documentation
'''

# Project Modules
from music_generator.create import MusicGenerator
from music_generator import style

def main():
    my_style = style.Style(style.DEFAULT)
    my_generator = MusicGenerator(my_style, composition_title='Programmatically Generated Music')

    my_generator.add_melody_track(style=my_style, location_to_add=0, num_bars=4)
    my_generator.add_melody_track(style=my_style, location_to_add=5, num_bars=4, times_to_repeat=2)

    my_generator.add_chords_track(num_bars=8, octave_adjust=-1)
    my_generator.add_chords_track(num_bars=8, location_to_add=9, octave_adjust=-1)

    my_generator.export_pdf()
    my_generator.export_midi(bpm=90)

    print(my_generator)

if __name__ == '__main__':
    main()
