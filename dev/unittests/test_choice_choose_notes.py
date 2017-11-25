"""
Created on May 26, 2016

@author: Alexander VanTol
"""
import pytest
from mgen import choice

_DEFAULT_SCALE = choice.scales.Chromatic("C")

def setup_module(choice):
    pass

def teardown_module(choice):
    pass

def test_choose_notes_0_notes():
    num_notes = 0
    notes_list = choice.choose_notes(num_notes, _DEFAULT_SCALE)

    assert len(notes_list) == num_notes

def test_choose_notes_1_note():
    num_notes = 1

    notes_list = choice.choose_notes(num_notes, _DEFAULT_SCALE)

    assert len(notes_list) == num_notes
    # Make sure note is valid or None (representing a rest)
    assert (notes_list[0] is None or
            notes_list[0] in _DEFAULT_SCALE.ascending() or
            notes_list[0] in _DEFAULT_SCALE.descending())

def test_choose_notes_2_notes():
    num_notes = 2

    notes_list = choice.choose_notes(num_notes, _DEFAULT_SCALE)

    assert len(notes_list) == num_notes
    for note in notes_list:
        # Make sure note is valid or None (representing a rest)
        assert (note is None or
                note in _DEFAULT_SCALE.ascending() or
                note in _DEFAULT_SCALE.descending())

def test_choose_notes_10_notes():
    num_notes = 10

    notes_list = choice.choose_notes(num_notes, _DEFAULT_SCALE)

    assert len(notes_list) == num_notes
    for note in notes_list:
        # Make sure note is valid or None (representing a rest)
        assert (note is None or
                note in _DEFAULT_SCALE.ascending() or
                note in _DEFAULT_SCALE.descending())

def test_choose_notes_major_scale():
    num_notes = 2
    scale = choice.scales.HarmonicMajor("G")

    notes_list = choice.choose_notes(num_notes, scale)

    assert len(notes_list) == num_notes
    for note in notes_list:
        # Make sure note is valid or None (representing a rest)
        assert (note is None or
                note in _DEFAULT_SCALE.ascending() or
                note in _DEFAULT_SCALE.descending())

def test_choose_notes_minor_scale():
    num_notes = 2
    scale = choice.scales.HarmonicMinor("G")

    notes_list = choice.choose_notes(num_notes, scale)

    assert len(notes_list) == num_notes
    for note in notes_list:
        # Make sure note is valid or None (representing a rest)
        assert (note is None or
                note in scale.ascending() or
                note in scale.descending())

def test_choose_notes_non_standard_scale():
    num_notes = 2
    scale = choice.scales.Dorian("G")

    notes_list = choice.choose_notes(num_notes, scale)

    assert len(notes_list) == num_notes
    for note in notes_list:
        # Make sure note is valid or None (representing a rest)
        assert (note is None or
                note in scale.ascending() or
                note in scale.descending())

def test_choose_notes_upper_bound():
    num_notes = 2
    rand_val = 1.0
    notes_list = choice.choose_notes(num_notes, _DEFAULT_SCALE, rand_val)

    assert len(notes_list) == num_notes
    for note in notes_list:
        # Make sure note is valid or None (representing a rest)
        assert (note is None or
                note in _DEFAULT_SCALE.ascending() or
                note in _DEFAULT_SCALE.descending())

def test_choose_notes_over_bound_choice():
    num_notes = 2
    rand_val = 5

    with pytest.raises(AttributeError):
        choice.choose_notes(num_notes, _DEFAULT_SCALE, rand_val)

def test_choose_notes_under_bound_choice():
    num_notes = 2
    rand_val = -5

    with pytest.raises(AttributeError):
        choice.choose_notes(num_notes, _DEFAULT_SCALE, rand_val)

def test_choose_notes_randomness():
    num_notes = 3
    # Populate 10 "random" choices
    notes_list = [choice.choose_notes(num_notes, _DEFAULT_SCALE) for _ in range(0, 10)]

    # Make sure they"re not ALL equal. Although this is possible... it"s
    # very unlikely. If you got here because of a failed test, I"m sorry.
    # Everything is most likely fine. Run them again.
    assert len(set(str(notes_list))) != 1

if __name__ == "__main__":
    pytest.main("-v")
