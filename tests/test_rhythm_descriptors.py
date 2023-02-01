from rhythmtoolbox import (
    get_stream,
    get_streams,
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
from rhythmtoolbox.midi_mapping import event_to_3number, event_to_8number

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


def test_get_stream():
    assert get_stream(BOSKA_3, "low").tolist() == [
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
    assert get_stream(BOSKA_8, "low").tolist() == [
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
    assert get_stream(BOSKA_9, "low").tolist() == [
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

    assert get_stream(BOSKA_3, "mid").tolist() == [
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
    assert get_stream(BOSKA_8, "mid").tolist() == [
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
    assert get_stream(BOSKA_9, "mid").tolist() == [
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

    assert get_stream(BOSKA_3, "hi").tolist() == [
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
    assert get_stream(BOSKA_8, "hi").tolist() == [
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
    assert get_stream(BOSKA_9, "hi").tolist() == [
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
    lowstream, midstream, histream = get_streams(BOSKA_3)
    assert density(lowstream) == 4
    assert density(midstream) == 5
    assert density(histream) == 10

    lowstream, midstream, histream = get_streams(BOSKA_8)
    assert density(lowstream) == 6
    assert density(midstream) == 10
    assert density(histream) == 9

    lowstream, midstream, histream = get_streams(BOSKA_9)
    assert density(lowstream) == 8
    assert density(midstream) == 7
    assert density(histream) == 9


def test_stepD():
    assert stepD(BOSKA_3) == 0.6875
    assert stepD(BOSKA_8) == 1.0
    assert stepD(BOSKA_9) == 0.875


def test_bandness():
    n_onset_steps = get_n_onset_steps(BOSKA_3)
    lowstream, midstream, histream = get_streams(BOSKA_3)
    assert bandness(lowstream, n_onset_steps) == 0.36363636363636365
    assert bandness(midstream, n_onset_steps) == 0.45454545454545453
    assert bandness(histream, n_onset_steps) == 0.9090909090909091

    n_onset_steps = get_n_onset_steps(BOSKA_8)
    lowstream, midstream, histream = get_streams(BOSKA_8)
    assert bandness(lowstream, n_onset_steps) == 0.375
    assert bandness(midstream, n_onset_steps) == 0.625
    assert bandness(histream, n_onset_steps) == 0.5625

    n_onset_steps = get_n_onset_steps(BOSKA_9)
    lowstream, midstream, histream = get_streams(BOSKA_9)
    assert bandness(lowstream, n_onset_steps) == 0.5714285714285714
    assert bandness(midstream, n_onset_steps) == 0.5
    assert bandness(histream, n_onset_steps) == 0.6428571428571429


def test_syncopation16():
    assert syncopation16(PATT_1) == -4
    assert syncopation16(PATT_2) == -10

    lowstream, midstream, histream = get_streams(BOSKA_3)
    assert syncopation16(lowstream) == -7
    assert syncopation16(midstream) == -4
    assert syncopation16(histream) == -10
    lowstream, midstream, histream = get_streams(BOSKA_8)
    assert syncopation16(lowstream) == 3
    assert syncopation16(midstream) == -4
    assert syncopation16(histream) == -5
    lowstream, midstream, histream = get_streams(BOSKA_9)
    assert syncopation16(lowstream) == 4
    assert syncopation16(midstream) == 2
    assert syncopation16(histream) == -12


def test_syness():
    lowstream, midstream, histream = get_streams(BOSKA_3)
    assert syness(lowstream) == -1.75
    assert syness(midstream) == -0.8
    assert syness(histream) == -1.0

    lowstream, midstream, histream = get_streams(BOSKA_8)
    assert syness(lowstream) == 0.5
    assert syness(midstream) == -0.4
    assert syness(histream) == -0.5555555555555556

    lowstream, midstream, histream = get_streams(BOSKA_9)
    assert syness(lowstream) == 0.5
    assert syness(midstream) == 0.2857142857142857
    assert syness(histream) == -1.3333333333333333


def test_polysync():
    lowstream, midstream, histream = get_streams(BOSKA_3)
    assert polysync(lowstream, midstream, histream) == 9

    lowstream, midstream, histream = get_streams(BOSKA_8)
    assert polysync(lowstream, midstream, histream) == 7

    lowstream, midstream, histream = get_streams(BOSKA_9)
    assert polysync(lowstream, midstream, histream) == 20


def test_polyevenness():
    lowstream, midstream, histream = get_streams(BOSKA_3)
    assert polyevenness(lowstream, midstream, histream) == 5.2753683906977775

    lowstream, midstream, histream = get_streams(BOSKA_8)
    assert polyevenness(lowstream, midstream, histream) == 4.428794764473658

    lowstream, midstream, histream = get_streams(BOSKA_9)
    assert polyevenness(lowstream, midstream, histream) == 4.9758868520193955


def test_polybalance():
    lowstream, midstream, histream = get_streams(BOSKA_3)
    assert polybalance(lowstream, midstream, histream) == 0.9618538544571633

    lowstream, midstream, histream = get_streams(BOSKA_8)
    assert polybalance(lowstream, midstream, histream) == 0.9961791398488665

    lowstream, midstream, histream = get_streams(BOSKA_9)
    assert polybalance(lowstream, midstream, histream) == 0.7964353630870814


def test_polyD():
    lowstream, midstream, histream = get_streams(BOSKA_3)
    assert polyD(lowstream, midstream, histream) == 19

    lowstream, midstream, histream = get_streams(BOSKA_8)
    assert polyD(lowstream, midstream, histream) == 25

    lowstream, midstream, histream = get_streams(BOSKA_9)
    assert polyD(lowstream, midstream, histream) == 24


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
