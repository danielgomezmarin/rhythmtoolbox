from rhythmtoolbox import (
    pattlist2descriptors,
    pattlist_to_pianoroll,
    pianoroll2descriptors,
)
from rhythmtoolbox.descriptors import (
    balance,
    bandness,
    density,
    evenness,
    get_n_onset_steps,
    noi,
    polybalance,
    polyD,
    polyevenness,
    polysync,
    stepD,
    syncopation16,
    syncopation16_awareness,
    syness,
)
from rhythmtoolbox.midi_mapping import (
    get_band,
    get_bands,
    event_to_3number,
    event_to_8number,
)

# TODO: add test case for non-16-step pattern
PATT_1 = [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]
PATT_2 = [1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0]

BOSKA_3_PATTLIST = [
    [36, 38, 42],
    [],
    [],
    [38, 42],
    [46],
    [46],
    [36, 38, 42],
    [],
    [42],
    [38],
    [36, 42],
    [],
    [38, 46],
    [46],
    [42, 64],
    [],
]
BOSKA_3 = pattlist_to_pianoroll(BOSKA_3_PATTLIST)

BOSKA_8_PATTLIST = [
    [38, 39, 46],
    [38, 39, 46],
    [38, 39, 46],
    [36],
    [36],
    [36],
    [38, 39, 46],
    [38, 39, 46],
    [38, 39, 46],
    [36],
    [36],
    [36],
    [38, 39, 46],
    [38, 39, 46],
    [39, 46],
    [38],
]
BOSKA_8 = pattlist_to_pianoroll(BOSKA_8_PATTLIST)

BOSKA_9_PATTLIST = [
    [36, 42],
    [36],
    [42],
    [],
    [42],
    [],
    [36, 38, 46],
    [36, 46],
    [37, 42],
    [36, 38],
    [36],
    [37],
    [36, 38, 42],
    [36],
    [37, 38, 39, 42, 46],
    [38, 46],
]
BOSKA_9 = pattlist_to_pianoroll(BOSKA_9_PATTLIST)


def test_syncopation16_awareness():
    assert syncopation16_awareness(PATT_1) == -11
    assert syncopation16_awareness(PATT_2) == -39


def test_evenness():
    assert evenness(PATT_1) == 0.9816064222042191
    assert evenness(PATT_2) == 0.971165288619607


def test_balance():
    assert balance(PATT_1) == 0.9297693395285831
    assert balance(PATT_2) == 0.9609819355967744


def test_get_band():
    assert get_band(BOSKA_3, "low").tolist() == [
        1,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        1,
        0,
    ]
    assert get_band(BOSKA_8, "low").tolist() == [
        0,
        0,
        0,
        1,
        1,
        1,
        0,
        0,
        0,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
    ]
    assert get_band(BOSKA_9, "low").tolist() == [
        1,
        1,
        0,
        0,
        0,
        0,
        1,
        1,
        0,
        1,
        1,
        0,
        1,
        1,
        0,
        0,
    ]

    assert get_band(BOSKA_3, "mid").tolist() == [
        1,
        0,
        0,
        1,
        0,
        0,
        1,
        0,
        0,
        1,
        0,
        0,
        1,
        0,
        0,
        0,
    ]
    assert get_band(BOSKA_8, "mid").tolist() == [
        1,
        1,
        1,
        0,
        0,
        0,
        1,
        1,
        1,
        0,
        0,
        0,
        1,
        1,
        1,
        1,
    ]
    assert get_band(BOSKA_9, "mid").tolist() == [
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        1,
        1,
        0,
        1,
        1,
        0,
        1,
        1,
    ]

    assert get_band(BOSKA_3, "hi").tolist() == [
        1,
        0,
        0,
        1,
        1,
        1,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        1,
        1,
        0,
    ]
    assert get_band(BOSKA_8, "hi").tolist() == [
        1,
        1,
        1,
        0,
        0,
        0,
        1,
        1,
        1,
        0,
        0,
        0,
        1,
        1,
        1,
        0,
    ]
    assert get_band(BOSKA_9, "hi").tolist() == [
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        1,
        1,
        0,
        0,
        0,
        1,
        0,
        1,
        1,
    ]


def test_noi():
    assert noi(BOSKA_3) == 5
    assert noi(BOSKA_8) == 4
    assert noi(BOSKA_9) == 6


def test_density():
    lowband, midband, hiband = get_bands(BOSKA_3)
    assert density(lowband) == 4
    assert density(midband) == 5
    assert density(hiband) == 10

    lowband, midband, hiband = get_bands(BOSKA_8)
    assert density(lowband) == 6
    assert density(midband) == 10
    assert density(hiband) == 9

    lowband, midband, hiband = get_bands(BOSKA_9)
    assert density(lowband) == 8
    assert density(midband) == 7
    assert density(hiband) == 9


def test_stepD():
    assert stepD(BOSKA_3) == 0.6875
    assert stepD(BOSKA_8) == 1.0
    assert stepD(BOSKA_9) == 0.875


def test_bandness():
    n_onset_steps = get_n_onset_steps(BOSKA_3)
    lowband, midband, hiband = get_bands(BOSKA_3)
    assert bandness(lowband, n_onset_steps) == 0.36363636363636365
    assert bandness(midband, n_onset_steps) == 0.45454545454545453
    assert bandness(hiband, n_onset_steps) == 0.9090909090909091

    n_onset_steps = get_n_onset_steps(BOSKA_8)
    lowband, midband, hiband = get_bands(BOSKA_8)
    assert bandness(lowband, n_onset_steps) == 0.375
    assert bandness(midband, n_onset_steps) == 0.625
    assert bandness(hiband, n_onset_steps) == 0.5625

    n_onset_steps = get_n_onset_steps(BOSKA_9)
    lowband, midband, hiband = get_bands(BOSKA_9)
    assert bandness(lowband, n_onset_steps) == 0.5714285714285714
    assert bandness(midband, n_onset_steps) == 0.5
    assert bandness(hiband, n_onset_steps) == 0.6428571428571429


def test_syncopation16():
    assert syncopation16(PATT_1) == -4
    assert syncopation16(PATT_2) == -10

    lowband, midband, hiband = get_bands(BOSKA_3)
    assert syncopation16(lowband) == -7
    assert syncopation16(midband) == -4
    assert syncopation16(hiband) == -10
    lowband, midband, hiband = get_bands(BOSKA_8)
    assert syncopation16(lowband) == 3
    assert syncopation16(midband) == -4
    assert syncopation16(hiband) == -5
    lowband, midband, hiband = get_bands(BOSKA_9)
    assert syncopation16(lowband) == 4
    assert syncopation16(midband) == 2
    assert syncopation16(hiband) == -12


def test_syness():
    lowband, midband, hiband = get_bands(BOSKA_3)
    assert syness(lowband) == -1.75
    assert syness(midband) == -0.8
    assert syness(hiband) == -1.0

    lowband, midband, hiband = get_bands(BOSKA_8)
    assert syness(lowband) == 0.5
    assert syness(midband) == -0.4
    assert syness(hiband) == -0.5555555555555556

    lowband, midband, hiband = get_bands(BOSKA_9)
    assert syness(lowband) == 0.5
    assert syness(midband) == 0.2857142857142857
    assert syness(hiband) == -1.3333333333333333


def test_polysync():
    lowband, midband, hiband = get_bands(BOSKA_3)
    assert polysync(lowband, midband, hiband) == 9

    lowband, midband, hiband = get_bands(BOSKA_8)
    assert polysync(lowband, midband, hiband) == 7

    lowband, midband, hiband = get_bands(BOSKA_9)
    assert polysync(lowband, midband, hiband) == 20


def test_polyevenness():
    lowband, midband, hiband = get_bands(BOSKA_3)
    assert polyevenness(lowband, midband, hiband) == 5.2753683906977775

    lowband, midband, hiband = get_bands(BOSKA_8)
    assert polyevenness(lowband, midband, hiband) == 4.428794764473658

    lowband, midband, hiband = get_bands(BOSKA_9)
    assert polyevenness(lowband, midband, hiband) == 4.9758868520193955


def test_polybalance():
    lowband, midband, hiband = get_bands(BOSKA_3)
    assert polybalance(lowband, midband, hiband) == 0.9618538544571633

    lowband, midband, hiband = get_bands(BOSKA_8)
    assert polybalance(lowband, midband, hiband) == 0.9961791398488665

    lowband, midband, hiband = get_bands(BOSKA_9)
    assert polybalance(lowband, midband, hiband) == 0.7964353630870814


def test_polyD():
    lowband, midband, hiband = get_bands(BOSKA_3)
    assert polyD(lowband, midband, hiband) == 19

    lowband, midband, hiband = get_bands(BOSKA_8)
    assert polyD(lowband, midband, hiband) == 25

    lowband, midband, hiband = get_bands(BOSKA_9)
    assert polyD(lowband, midband, hiband) == 24


def test_pianoroll2descriptors():
    v = pianoroll2descriptors(BOSKA_3)
    assert v["noi"] == 5
    assert v["lowD"] == 4
    assert v["midD"] == 5
    assert v["hiD"] == 10
    assert v["stepD"] == 0.6875
    assert v["lowness"] == 0.36363636363636365
    assert v["midness"] == 0.45454545454545453
    assert v["hiness"] == 0.9090909090909091
    assert v["lowsync"] == -7
    assert v["midsync"] == -4
    assert v["hisync"] == -10
    assert v["lowsyness"] == -1.75
    assert v["midsyness"] == -0.8
    assert v["hisyness"] == -1.0
    assert v["polysync"] == 9
    assert v["polyevenness"] == 5.2753683906977775
    assert v["polybalance"] == 0.9618538544571633
    assert v["polyD"] == 19

    v = pianoroll2descriptors(BOSKA_8)
    assert v["noi"] == 4
    assert v["lowD"] == 6
    assert v["midD"] == 10
    assert v["hiD"] == 9
    assert v["stepD"] == 1.0
    assert v["lowness"] == 0.375
    assert v["midness"] == 0.625
    assert v["hiness"] == 0.5625
    assert v["lowsync"] == 3
    assert v["midsync"] == -4
    assert v["hisync"] == -5
    assert v["lowsyness"] == 0.5
    assert v["midsyness"] == -0.4
    assert v["hisyness"] == -0.5555555555555556
    assert v["polysync"] == 7
    assert v["polyevenness"] == 4.428794764473658
    assert v["polybalance"] == 0.9961791398488665
    assert v["polyD"] == 25

    v = pianoroll2descriptors(BOSKA_9)
    assert v["noi"] == 6
    assert v["lowD"] == 8
    assert v["midD"] == 7
    assert v["hiD"] == 9
    assert v["stepD"] == 0.875
    assert v["lowness"] == 0.5714285714285714
    assert v["midness"] == 0.5
    assert v["hiness"] == 0.6428571428571429
    assert v["lowsync"] == 4
    assert v["midsync"] == 2
    assert v["hisync"] == -12
    assert v["lowsyness"] == 0.5
    assert v["midsyness"] == 0.2857142857142857
    assert v["hisyness"] == -1.3333333333333333
    assert v["polysync"] == 20
    assert v["polyevenness"] == 4.9758868520193955
    assert v["polybalance"] == 0.7964353630870814
    assert v["polyD"] == 24


def test_pattlist2descriptors():
    v = pattlist2descriptors(BOSKA_3_PATTLIST)
    assert v["noi"] == 5
    assert v["lowD"] == 4
    assert v["midD"] == 5
    assert v["hiD"] == 10
    assert v["stepD"] == 0.6875
    assert v["lowness"] == 0.36363636363636365
    assert v["midness"] == 0.45454545454545453
    assert v["hiness"] == 0.9090909090909091
    assert v["lowsync"] == -7
    assert v["midsync"] == -4
    assert v["hisync"] == -10
    assert v["lowsyness"] == -1.75
    assert v["midsyness"] == -0.8
    assert v["hisyness"] == -1.0
    assert v["polysync"] == 9
    assert v["polyevenness"] == 5.2753683906977775
    assert v["polybalance"] == 0.9618538544571633
    assert v["polyD"] == 19

    v = pattlist2descriptors(BOSKA_8_PATTLIST)
    assert v["noi"] == 4
    assert v["lowD"] == 6
    assert v["midD"] == 10
    assert v["hiD"] == 9
    assert v["stepD"] == 1.0
    assert v["lowness"] == 0.375
    assert v["midness"] == 0.625
    assert v["hiness"] == 0.5625
    assert v["lowsync"] == 3
    assert v["midsync"] == -4
    assert v["hisync"] == -5
    assert v["lowsyness"] == 0.5
    assert v["midsyness"] == -0.4
    assert v["hisyness"] == -0.5555555555555556
    assert v["polysync"] == 7
    assert v["polyevenness"] == 4.428794764473658
    assert v["polybalance"] == 0.9961791398488665
    assert v["polyD"] == 25

    v = pattlist2descriptors(BOSKA_9_PATTLIST)
    assert v["noi"] == 6
    assert v["lowD"] == 8
    assert v["midD"] == 7
    assert v["hiD"] == 9
    assert v["stepD"] == 0.875
    assert v["lowness"] == 0.5714285714285714
    assert v["midness"] == 0.5
    assert v["hiness"] == 0.6428571428571429
    assert v["lowsync"] == 4
    assert v["midsync"] == 2
    assert v["hisync"] == -12
    assert v["lowsyness"] == 0.5
    assert v["midsyness"] == 0.2857142857142857
    assert v["hisyness"] == -1.3333333333333333
    assert v["polysync"] == 20
    assert v["polyevenness"] == 4.9758868520193955
    assert v["polybalance"] == 0.7964353630870814
    assert v["polyD"] == 24


def test_event_to_8number():
    assert event_to_8number([36, 38, 46]) == [1, 2, 4]
    assert event_to_8number([37, 38, 39, 42, 46]) == [2, 3, 4, 5, 6]


def test_event_to_3number():
    assert event_to_3number([36, 38, 46]) == [1, 2, 3]
    assert event_to_3number([37, 38, 39, 42, 46]) == [2, 3]
