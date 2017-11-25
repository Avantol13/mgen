"""
Created on May 26, 2016

@author: Alexander VanTol
"""
import pytest
from mgen import choice

default_test_keys = [("eb", "0.009"),
                     ("ab", "0.012"),
                     ("c#", "0.021"),
                     ("c", "0.024"),
                     ("Eb", "0.024"),
                     ("f#", "0.025"),
                     ("d", "0.026"),
                     ("g", "0.026"),
                     ("B", "0.026"),
                     ("F#", "0.027"),
                     ("f", "0.030"),
                     ("bb", "0.032"),
                     ("Bb", "0.035"),
                     ("e", "0.042"),
                     ("b", "0.042"),
                     ("Ab", "0.043"),
                     ("a", "0.048"),
                     ("F", "0.053"),
                     ("C#", "0.060"),
                     ("A", "0.067"),
                     ("D", "0.097"),
                     ("C", "0.113"),
                     ("G", "0.118")]

def setup_module(choice):
    pass

def teardown_module(choice):
    pass

def test_choose_key_lower_bound():
    rand_val = 0.0
    result = choice.choose_key(default_test_keys, rand_val)

    assert result == "eb"

def test_choose_key_upper_bound():
    rand_val = 1.0
    result = choice.choose_key(default_test_keys, rand_val)

    assert result == "G"

def test_choose_key_one_choice():
    keys = [("eb", "0"),
            ("ab", "0"),
            ("c#", "0"),
            ("c", "0"),
            ("Eb", "0"),
            ("f#", "0"),
            ("d", "0"),
            ("g", "0"),
            ("B", "0"),
            ("F#", "0"),
            ("f", "0"),
            ("bb", "1.0"),
            ("Bb", "0"),
            ("e", "0"),
            ("b", "0"),
            ("Ab", "0"),
            ("a", "0"),
            ("F", "0"),
            ("C#", "0"),
            ("A", "0"),
            ("D", "0"),
            ("C", "0"),
            ("G", "0")]

    result = choice.choose_key(keys)

    assert result == "bb"

def test_choose_key_over_bound_choice():
    with pytest.raises(AttributeError):
        choice.choose_key(default_test_keys, 5)

def test_choose_key_under_bound_choice():
    with pytest.raises(AttributeError):
        choice.choose_key(default_test_keys, -5)

def test_choose_key_randomness():
    # Populate 10 "random" choices
    keys_list = [choice.choose_key(default_test_keys) for _ in range(0, 10)]

    # Make sure they"re not ALL equal. Although this is possible... it"s
    # very unlikely. If you got here because of a failed test, I"m sorry.
    # Everything is most likely fine. Run them again.
    assert len(set(keys_list)) != 1

if __name__ == "__main__":
    pytest.main("-v")
