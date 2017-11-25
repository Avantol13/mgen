"""
Created on Sep 14, 2016

@author: Alexander VanTol
"""
import pytest
from mgen import MusicGenerator
from mgen import StyleProbs
from mgen import JAZZ_CFG_FILE
from mgen import config
import os

def setup_module(choice):
    pass

def teardown_module(choice):
    pass

def test_mgen_obj_creation():
    music_generator = MusicGenerator()
    assert isinstance(music_generator, MusicGenerator)

def test_mgen_default_attributes():
    music_generator = MusicGenerator()
    assert isinstance(music_generator.style_probs, StyleProbs)
    assert isinstance(music_generator.composition_title, str)
    assert isinstance(music_generator.author_name, str)

def test_mgen_non_default_args():
    style_probs = StyleProbs(JAZZ_CFG_FILE)
    composition_title = "TEST1234!@#*&^%"
    author_name = "()*&@#$(&^jdnfjknopihfjned"

    music_generator = MusicGenerator(style_probs=style_probs,
                                     composition_title=composition_title,
                                     author_name=author_name)

    assert music_generator.style_probs == style_probs
    assert music_generator.composition_title == composition_title
    assert music_generator.author_name == author_name

def test_add_melody_track():
    """
    Test that adding a melody track actually adds it to the composition
    """
    num_bars = 3
    music_generator = MusicGenerator()

    music_generator.add_melody_track(num_bars)

    assert len(music_generator.composition.tracks) == 1
    assert len(music_generator.composition.tracks[0].bars) == num_bars

def test_add_melody_two_tracks():
    """
    Test that adding two melody tracks actually adds them to the composition
    with the right number of bars
    """
    num_bars_1 = 2
    num_bars_2 = 3
    music_generator = MusicGenerator()

    music_generator.add_melody_track(num_bars_1)
    music_generator.add_melody_track(num_bars_2)

    assert len(music_generator.composition.tracks) == 2
    assert len(music_generator.composition.tracks[0].bars) == num_bars_1
    assert len(music_generator.composition.tracks[1].bars) == num_bars_2

def test_add_melody_track_at_location():
    """
    Testing adding melody track at a specific bar
    """
    num_bars = 3
    location_to_add = 4
    music_generator = MusicGenerator()

    music_generator.add_melody_track(num_bars, location_to_add=location_to_add)

    assert len(music_generator.composition.tracks) == 1

    # Bars before insert location
    for bar in music_generator.composition.tracks[0].bars[0:location_to_add - 2]:
        for note in bar:
            # Location 2 in this list is the note value
            assert note[2] is None

    # Make sure the correct number of bars exist at the insert location
    assert len(music_generator.composition.tracks[0].bars[location_to_add - 1:]) == num_bars

def test_add_melody_track_repeat():
    """
    Test that times_to_repeat actually repeats the melody track
    """
    num_bars = 4
    times_to_repeat = 2
    music_generator = MusicGenerator()

    music_generator.add_melody_track(num_bars, times_to_repeat=times_to_repeat)

    assert len(music_generator.composition.tracks) == 1

    # Make sure the correct number of bars exist at the insert location
    assert len(music_generator.composition.tracks[0].bars) == num_bars + num_bars * times_to_repeat
    for x in range(0, num_bars):
        # Current bar is the same as the first repeated bar
        assert music_generator.composition.tracks[0].bars[x] == music_generator.composition.tracks[0].bars[x + num_bars]
        # Current bar is the same as the second repeated bar
        assert music_generator.composition.tracks[0].bars[x + num_bars] == music_generator.composition.tracks[0].bars[x + 2 * num_bars]

def test_add_chords_track():
    """
    Test that adding a chords track actually adds it to the composition
    """
    num_bars = 3
    music_generator = MusicGenerator()

    music_generator.add_chords_track(num_bars)

    assert len(music_generator.composition.tracks) == 1
    assert len(music_generator.composition.tracks[0].bars) == num_bars

def test_add_chords_two_tracks():
    """
    Test that adding two chords tracks actually adds them to the composition
    with the right number of bars
    """
    num_bars_1 = 3
    num_bars_2 = 4
    music_generator = MusicGenerator()

    music_generator.add_chords_track(num_bars_1)
    music_generator.add_chords_track(num_bars_2)

    assert len(music_generator.composition.tracks) == 2
    assert len(music_generator.composition.tracks[0].bars) == num_bars_1
    assert len(music_generator.composition.tracks[1].bars) == num_bars_2

def test_add_chords_track_at_location():
    """
    Testing adding chords track at a specific bar
    """
    num_bars = 3
    location_to_add = 4
    music_generator = MusicGenerator()

    music_generator.add_chords_track(num_bars, location_to_add=location_to_add)

    assert len(music_generator.composition.tracks) == 1

    # Bars before insert location
    for bar in music_generator.composition.tracks[0].bars[0:location_to_add - 2]:
        for note in bar:
            # Location 2 in this list is the note value
            assert note[2] is None

    # Make sure the correct number of bars exist at the insert location
    assert len(music_generator.composition.tracks[0].bars[location_to_add - 1:]) == num_bars

def test_add_chords_track_repeat():
    """
    Test that times_to_repeat actually repeats the chords track
    """
    num_bars = 4
    times_to_repeat = 2
    music_generator = MusicGenerator()

    music_generator.add_chords_track(num_bars, times_to_repeat=times_to_repeat)

    assert len(music_generator.composition.tracks) == 1

    # Make sure the correct number of bars exist at the insert location
    assert len(music_generator.composition.tracks[0].bars) == num_bars + num_bars * times_to_repeat
    for x in range(0, num_bars):
        # Current bar is the same as the first repeated bar
        assert music_generator.composition.tracks[0].bars[x] == music_generator.composition.tracks[0].bars[x + num_bars]
        # Current bar is the same as the second repeated bar
        assert music_generator.composition.tracks[0].bars[x + num_bars] == music_generator.composition.tracks[0].bars[x + 2 * num_bars]

def test_add_melody_track_and_chords_track():
    """
    Test that when attempting to add both a melody and chords track to the composition,
    they actually get added
    """
    melody_num_bars = 3
    chords_num_bars = 4
    music_generator = MusicGenerator()

    music_generator.add_melody_track(melody_num_bars)
    music_generator.add_chords_track(chords_num_bars)

    assert len(music_generator.composition.tracks) == 2
    assert len(music_generator.composition.tracks[0].bars) == melody_num_bars
    assert len(music_generator.composition.tracks[1].bars) == chords_num_bars

def test_remove_track_middle():
    """
    Test removing the middle track
    """
    melody_num_bars = 4
    chords_num_bars = 3
    music_generator = MusicGenerator()

    music_generator.add_melody_track(melody_num_bars)
    music_generator.add_chords_track(chords_num_bars)
    music_generator.add_melody_track(melody_num_bars)

    assert len(music_generator.composition.tracks) == 3

    music_generator.remove_track(1)

    assert len(music_generator.composition.tracks) == 2
    # Remaining tracks should be the two melody tracks, check how many bars
    assert len(music_generator.composition.tracks[0].bars) == melody_num_bars
    assert len(music_generator.composition.tracks[1].bars) == melody_num_bars

def test_remove_track_default():
    """
    Test that default for remove_track removes the last track
    """
    melody_num_bars = 4
    chords_num_bars = 3
    music_generator = MusicGenerator()

    music_generator.add_melody_track(melody_num_bars)
    music_generator.add_chords_track(melody_num_bars)
    music_generator.add_melody_track(chords_num_bars)

    assert len(music_generator.composition.tracks) == 3

    music_generator.remove_track()

    assert len(music_generator.composition.tracks) == 2
    # Remaining tracks should be the two melody tracks, check how many bars
    assert len(music_generator.composition.tracks[0].bars) == melody_num_bars
    assert len(music_generator.composition.tracks[1].bars) == melody_num_bars

def test_set_invalid_time_signature():
    """
    Test that exception is thrown with invalid time signature
    """
    music_generator = MusicGenerator()
    time_signature = "NOT A REAL TIME SIGNATURE"

    with pytest.raises(AttributeError):
        music_generator.set_time_signature(time_signature)

def test_set_valid_time_signature():
    """
    Test that setting a valid time signature works
    """
    music_generator = MusicGenerator()
    time_signature = (3, 4)

    music_generator.set_time_signature(time_signature)

    assert music_generator._time_signature == time_signature

def test_set_invalid_key():
    """
    Test that exception is thrown with invalid time key
    """
    music_generator = MusicGenerator()
    key = "NOT A REAL KEY"

    with pytest.raises(AttributeError):
        music_generator.set_key(key)

def test_set_valid_key():
    """
    Test that setting a valid key works
    """
    music_generator = MusicGenerator()
    key = "Ab"

    music_generator.set_key(key)
    assert music_generator._key == key

def test_export_pdf():
    filename = "test_export_pdf.pdf"
    music_generator = MusicGenerator()
    music_generator.add_melody_track(num_bars=4)
    music_generator.export_pdf(filename)
    assert os.path.isfile(filename)
    os.remove(filename)

def test_export_pdf_path():
    path = os.path.abspath(config._PATH_TO_SCRIPT +
                           "/../dev/unittests/tests/test_path/pdf")
    filename = os.path.abspath(path + "/test_export_pdf.pdf")
    music_generator = MusicGenerator()
    music_generator.add_melody_track(num_bars=4)
    music_generator.export_pdf(filename)
    assert os.path.isdir(path)
    assert os.path.isfile(filename)
    os.remove(filename)
    os.rmdir(path)

def test_export_midi():
    filename = "test_export_midi.mid"
    music_generator = MusicGenerator()
    music_generator.add_melody_track(num_bars=4)
    music_generator.export_midi(filename)
    assert os.path.isfile(filename)
    os.remove(filename)

def test_export_midi_path():
    path = os.path.abspath(config._PATH_TO_SCRIPT +
                           "/../dev/unittests/tests/test_path/midi")
    filename = os.path.abspath(path + "/test_export_midi.mid")
    music_generator = MusicGenerator()
    music_generator.add_melody_track(num_bars=4)
    music_generator.export_midi(filename)
    assert os.path.isdir(path)
    assert os.path.isfile(filename)
    os.remove(filename)
    os.rmdir(path)

def test_export_pickle():
    filename = "test_export_pkl.pkl"
    music_generator = MusicGenerator()
    music_generator.add_melody_track(num_bars=4)
    music_generator.export_pickle(filename)
    assert os.path.isfile(filename)
    os.remove(filename)

def test_export_pickle_path():
    path = os.path.abspath(config._PATH_TO_SCRIPT +
                           "/../dev/unittests/tests/test_path/pkl")
    filename = os.path.abspath(path + "/test_export_pkl.pkl")
    music_generator = MusicGenerator()
    music_generator.add_melody_track(num_bars=4)
    music_generator.export_pickle(filename)
    assert os.path.isdir(path)
    assert os.path.isfile(filename)
    os.remove(filename)
    os.rmdir(path)

def test_from_pickle():
    filename = os.path.abspath(config._PATH_TO_SCRIPT +
                               "/../dev/unittests/" + "test_export_pkl.pkl")
    music_generator = MusicGenerator()
    music_generator.add_melody_track(num_bars=4)
    music_generator.add_melody_track(num_bars=7)
    music_generator.export_pickle(filename)

    from_the_grave = MusicGenerator.from_pickle(filename)

    assert len(from_the_grave.composition.tracks) == 2
    assert len(from_the_grave.composition.tracks[0].bars) == 4
    assert len(from_the_grave.composition.tracks[1].bars) == 7

    os.remove(filename)

if __name__ == "__main__":
    pytest.main("-v")
