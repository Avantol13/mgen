"""
Created on Sep 14, 2016

@author: Alexander VanTol
"""
import pytest
from mgen import choice

_DEFAULT_TEST_CHORD_PROGRESSIONS = [("IM7 I7 IVM7 ivm7 iiim VI7 iim V7", 0.10),
                                    ("IM7 iim7 V7 IVM7", 0.10),
                                    ("IM7 II7 iim7 IM7", 0.10),
                                    ("IM7 #Idim7 iim7 #IIdim7 iiim7 VI7", 0.10),
                                    ("IM7 iim7 V7", 0.10),
                                    ("IM7 vim7 iim7 V7 iiim7 VI7 iim7 V7", 0.10),
                                    ("iim7 V7 IM7", 0.40)
                                    ]

def setup_module(choice):
    pass

def teardown_module(choice):
    pass

def test_choose_chord_progression_single_prob():
    prob_list = [("IM7 I7 IVM7 ivm7 iiim VI7 iim V7", 0.00),
                 ("IM7 iim7 V7 IVM7", 0.00),
                 ("IM7 II7 iim7 IM7", 1.00),
                 ("IM7 #Idim7 iim7 #IIdim7 iiim7 VI7", 0.00),
                 ("IM7 iim7 V7", 0.00),
                 ("IM7 vim7 iim7 V7 iiim7 VI7 iim7 V7", 0.00),
                 ("iim7 V7 IM7", 0.00)
                 ]
    result = choice.choose_chord_progression(prob_list)

    assert result == "IM7 II7 iim7 IM7".split(" ")

def test_choose_chord_progression_single_prob_only_item():
    scale_prob_list = [("IM7 II7 iim7 IM7", 1.00)]
    result = choice.choose_chord_progression(scale_prob_list)

    assert result == scale_prob_list[0][0].split(" ")

def test_choose_chord_progression_over_bound_choice():
    with pytest.raises(AttributeError):
        choice.choose_chord_progression(_DEFAULT_TEST_CHORD_PROGRESSIONS, 5)

def test_choose_chord_progression_under_bound_choice():
    with pytest.raises(AttributeError):
        choice.choose_chord_progression(_DEFAULT_TEST_CHORD_PROGRESSIONS, -5)

""" TODO: Enable this test once we implement actual randomness
def test_choose_chord_progression_randomness():
    # Populate 10 "random" choices
    chord_progs_list = [choice.choose_chord_progression(_DEFAULT_TEST_CHORD_PROGRESSIONS) for _ in range(0, 10)]

    # Make sure they"re not ALL equal. Although this is possible... it"s
    # very unlikely. If you got here because of a failed test, I"m sorry.
    # Everything is most likely fine. Run them again.
    assert len(set(str(chord_progs_list))) != 1
"""

if __name__ == "__main__":
    pytest.main("-v")
