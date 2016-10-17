'''
Created on Sep 14, 2016

@author: Alexander VanTol
'''
import pytest
from mgen import convert
from mingus.containers.bar import Bar
from mingus.containers.note import Note
from mingus.containers.note_container import NoteContainer

_DEFAULT_TEST_SCALES = [('scales.Ionian', 0.17),
                        ('scales.Dorian', 0.17),
                        ('scales.Phrygian', 0.17),
                        ('scales.Lydian', 0.17),
                        ('scales.Mixolydian', 0.16),
                        ('scales.Aeolian', 0.16)
                        ]

def setup_module(choice):
    pass

def teardown_module(choice):
    pass

def test_convert_notes_to_bar_invalid_key():
    musical_key = '@!)$*#(^!@)^%(*&'
    melody_timing = []
    chosen_notes = []
    with pytest.raises(AttributeError):
        convert.convert_notes_to_bar(musical_key, melody_timing, chosen_notes)

def test_convert_notes_to_bar_valid_major_key():
    musical_key = 'A'
    melody_timing = []
    chosen_notes = []
    result = convert.convert_notes_to_bar(musical_key, melody_timing, chosen_notes)

    assert isinstance(result, Bar)

def test_convert_notes_to_bar_valid_minor_key():
    musical_key = 'eb'
    melody_timing = []
    chosen_notes = []
    result = convert.convert_notes_to_bar(musical_key, melody_timing, chosen_notes)

    assert isinstance(result, Bar)

# TODO: Test that it actually creates a bar with the right notes and right lengths

def test_chords_change_octave_up():
    # Set all octave to 4
    chords = [['E-4', 'G-4', 'B-4'], ['D-4', 'F#-4', 'A-4'], ['C-4', 'E-4', 'G-4']]
    result = convert.change_chords_octave(chords, 1)
    for chord in result:
        for note in chord:
            assert Note(note).octave == 5

def test_chords_change_octave_down():
    # Set all octave to 4
    chords = [['E-4', 'G-4', 'B-4'], ['D-4', 'F#-4', 'A-4'], ['C-4', 'E-4', 'G-4']]
    result = convert.change_chords_octave(chords, -2)
    for chord in result:
        for note in chord:
            assert Note(note).octave == 2

def test_chords_change_octave_0():
    # Set all octave to 4
    chords = [['E-4', 'G-4', 'B-4'], ['D-4', 'F#-4', 'A-4'], ['C-4', 'E-4', 'G-4']]
    result = convert.change_chords_octave(chords, 0)
    for chord in result:
        for note in chord:
            assert Note(note).octave == 4

def test_notes_change_octave_up():
    # Set all octave to 4
    notes = ['E-4', 'G-4', 'B-4']
    result = convert.change_notes_octave(notes, 1)
    for note in result:
        assert Note(note).octave == 5

def test_notes_change_octave_down():
    # Set all octave to 4
    notes = ['E-4', 'G-4', 'B-4']
    result = convert.change_notes_octave(notes, -2)
    for note in result:
        assert Note(note).octave == 2

def test_notes_change_octave_0():
    # Set all octave to 4
    notes = ['E-4', 'G-4', 'B-4']
    result = convert.change_notes_octave(notes, 0)
    for note in result:
        assert Note(note).octave == 4

if __name__ == '__main__':
    pytest.main('-v')
