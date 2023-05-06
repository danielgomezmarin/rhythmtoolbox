from fixtures import BOSKA_3, BOSKA_8, BOSKA_9

from rhythmtoolbox.midi_mapping import (event_to_3number, event_to_8number,
                                        get_band)


def test_get_band():
    # fmt: off
    assert get_band(BOSKA_3, "low").tolist() == [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0]
    assert get_band(BOSKA_3, "mid").tolist() == [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1]
    assert get_band(BOSKA_3, "hi").tolist() == [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

    assert get_band(BOSKA_8, "low").tolist() == [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    assert get_band(BOSKA_8, "mid").tolist() == [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1]
    assert get_band(BOSKA_8, "hi").tolist() == [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0]

    assert get_band(BOSKA_9, "low").tolist() == [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]
    assert get_band(BOSKA_9, "mid").tolist() == [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0]
    assert get_band(BOSKA_9, "hi").tolist() == [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0]
    # fmt: on


def test_event_to_8number():
    assert event_to_8number([36, 38, 46]) == [1, 2, 4]
    assert event_to_8number([37, 38, 39, 42, 46]) == [2, 3, 4, 5, 6]


def test_event_to_3number():
    assert event_to_3number([36, 38, 46]) == [1, 2, 3]
    assert event_to_3number([37, 38, 39, 42, 46]) == [2, 3]
