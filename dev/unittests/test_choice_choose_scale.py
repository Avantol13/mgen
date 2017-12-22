"""
Created on Sep 14, 2016

@author: Alexander VanTol
"""
import pytest
from mgen import choice
from mingus.core import scales

_DEFAULT_TEST_SCALES = [("Ionian", 0.17),
                        ("Dorian", 0.17),
                        ("Phrygian", 0.17),
                        ("Lydian", 0.17),
                        ("Mixolydian", 0.16),
                        ("Aeolian", 0.16)
                        ]

def setup_module(choice):
    pass

def teardown_module(choice):
    pass

def test_choose_scale_major_key():
    key = "A"
    result = choice.choose_scale(key, _DEFAULT_TEST_SCALES)

    assert isinstance(result, scales._Scale)

def test_choose_scale_minor_key():
    key = "Em"
    result = choice.choose_scale(key, _DEFAULT_TEST_SCALES)

    assert isinstance(result, scales._Scale)

def test_choose_scale_single_prob():
    key = "A"
    scale_prob_list = [("scales.Ionian", 0.00),
                       ("scales.Dorian", 0.00),
                       ("scales.Phrygian", 0.00),
                       ("scales.Lydian", 1.00),
                       ("scales.Mixolydian", 0.00),
                       ("scales.Aeolian", 0.00)
                       ]
    result = choice.choose_scale(key, scale_prob_list)

    assert isinstance(result, scales._Scale)

def test_choose_scale_single_prob_only_item():
    key = "A"
    scale_prob_list = [("scales.Lydian", 1.00)]
    result = choice.choose_scale(key, scale_prob_list)

    assert isinstance(result, scales._Scale)

def test_choose_scale_over_bound_choice():
    key = "A"
    with pytest.raises(AttributeError):
        choice.choose_scale(key, _DEFAULT_TEST_SCALES, 5)

def test_choose_scale_under_bound_choice():
    key = "A"
    with pytest.raises(AttributeError):
        choice.choose_scale(key, _DEFAULT_TEST_SCALES, -5)

def test_choose_scale_randomness():
    key = "A"
    # Populate 10 "random" choices
    scales_list = [choice.choose_scale(key, _DEFAULT_TEST_SCALES) for _ in range(0, 10)]

    # Make sure they're not ALL equal. Although this is possible... it's
    # very unlikely. If you got here because of a failed test, I'm sorry.
    # Everything is most likely fine. Run them again. They're not deterministic.... :'(
    assert len(set(str(scales_list))) != 1

if __name__ == "__main__":
    pytest.main("-v")
