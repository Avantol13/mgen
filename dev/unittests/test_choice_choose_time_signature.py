"""
Created on Sep 14, 2016

@author: Alexander VanTol
"""
import pytest
from mgen import choice
from mingus.core import meter

# TODO: Once choose_time_signature() returns anything other than meter.common_time,
#       add some more tests
_DEFAULT_TEST_TIME_SIGS = []

def setup_module(choice):
    pass

def teardown_module(choice):
    pass

def test_choose_time_signature_over_bound_choice():
    with pytest.raises(AttributeError):
        choice.choose_time_signature(_DEFAULT_TEST_TIME_SIGS, 5)

def test_choose_time_signature_under_bound_choice():
    with pytest.raises(AttributeError):
        choice.choose_time_signature(_DEFAULT_TEST_TIME_SIGS, -5)

""" TODO: Enable this test once we implement actual randomness
def test_choose_time_signature_randomness():
    # Populate 10 "random" choices
    time_sigs_list = [choice.choose_time_signature(_DEFAULT_TEST_TIME_SIGS) for _ in range(0, 10)]

    # Make sure they"re not ALL equal. Although this is possible... it"s
    # very unlikely. If you got here because of a failed test, I"m sorry.
    # Everything is most likely fine. Run them again.
    assert len(set(time_sigs_list)) != 1
"""
if __name__ == "__main__":
    pytest.main("-v")
