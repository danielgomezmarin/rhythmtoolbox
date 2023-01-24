from rhythm_descriptors import (
    event_to_8number,
    event_to_3number,
    density,
    syncopation16,
    syncopation16_awareness,
    evenness,
    balance,
    lowstream,
    midstream,
    histream,
    noi,
    loD,
    midD,
    hiD,
    stepD,
    lowness,
    midness,
    hiness,
    lowsync,
    midsync,
    hisync,
    losyness,
    midsyness,
    hisyness,
    polysync,
    polyevenness,
    polybalance,
    polyD,
    pattlist2descriptors,
)

PATT_1 = [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]
PATT_2 = [1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0]

BOSKA_3 = [
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

BOSKA_8 = [
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

BOSKA_9 = [
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


def test_event_to_8number():
    assert event_to_8number([36, 38, 46]) == [1, 2, 4]
    assert event_to_8number([37, 38, 39, 42, 46]) == [2, 3, 4, 5, 6]


def test_event_to_3number():
    assert event_to_3number([36, 38, 46]) == [1, 2, 3]
    assert event_to_3number([37, 38, 39, 42, 46]) == [2, 3]


def test_density():
    assert density(PATT_1) == 5
    assert density(PATT_2) == 10


def test_syncopation16():
    assert syncopation16(PATT_1) == -4
    assert syncopation16(PATT_2) == -10


def test_syncopation16_awareness():
    assert syncopation16_awareness(PATT_1) == -11
    assert syncopation16_awareness(PATT_2) == -39


def test_evenness():
    assert evenness(PATT_1) == 0.9816064222042191
    assert evenness(PATT_2) == 0.971165288619607


def test_balance():
    assert balance(PATT_1) == 0.9297693395285831
    assert balance(PATT_2) == 0.9609819355967744


def test_lowstream():
    assert lowstream(BOSKA_3) == [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0]
    assert lowstream(BOSKA_8) == [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0]
    assert lowstream(BOSKA_9) == [1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0]


def test_midstream():
    assert midstream(BOSKA_3) == [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]
    assert midstream(BOSKA_8) == [1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1]
    assert midstream(BOSKA_9) == [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1]


def test_histream():
    assert histream(BOSKA_3) == [1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0]
    assert histream(BOSKA_8) == [1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0]
    assert histream(BOSKA_9) == [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1]


def test_noi():
    assert noi(BOSKA_3) == 5
    assert noi(BOSKA_8) == 4
    assert noi(BOSKA_9) == 6


def test_loD():
    assert loD(BOSKA_3) == 4
    assert loD(BOSKA_8) == 6
    assert loD(BOSKA_9) == 8


def test_midD():
    assert midD(BOSKA_3) == 5
    assert midD(BOSKA_8) == 10
    assert midD(BOSKA_9) == 7


def test_hiD():
    assert hiD(BOSKA_3) == 10
    assert hiD(BOSKA_8) == 9
    assert hiD(BOSKA_9) == 9


def test_stepD():
    assert stepD(BOSKA_3) == 0.6875
    assert stepD(BOSKA_8) == 1.0
    assert stepD(BOSKA_9) == 0.875


def test_lowness():
    assert lowness(BOSKA_3) == 0.36363636363636365
    assert lowness(BOSKA_8) == 0.375
    assert lowness(BOSKA_9) == 0.5714285714285714


def test_midness():
    assert midness(BOSKA_3) == 0.45454545454545453
    assert midness(BOSKA_8) == 0.625
    assert midness(BOSKA_9) == 0.5


def test_hiness():
    assert hiness(BOSKA_3) == 0.9090909090909091
    assert hiness(BOSKA_8) == 0.5625
    assert hiness(BOSKA_9) == 0.6428571428571429


def test_lowsync():
    assert lowsync(BOSKA_3) == -7
    assert lowsync(BOSKA_8) == 3
    assert lowsync(BOSKA_9) == 4


def test_midsync():
    assert midsync(BOSKA_3) == -4
    assert midsync(BOSKA_8) == -4
    assert midsync(BOSKA_9) == 2


def test_hisync():
    assert hisync(BOSKA_3) == -10
    assert hisync(BOSKA_8) == -5
    assert hisync(BOSKA_9) == -12


def test_losyness():
    assert losyness(BOSKA_3) == -1.75
    assert losyness(BOSKA_8) == 0.5
    assert losyness(BOSKA_9) == 0.5


def test_midsyness():
    assert midsyness(BOSKA_3) == -0.8
    assert midsyness(BOSKA_8) == -0.4
    assert midsyness(BOSKA_9) == 0.2857142857142857


def test_hisyness():
    assert hisyness(BOSKA_3) == -1.0
    assert hisyness(BOSKA_8) == -0.5555555555555556
    assert hisyness(BOSKA_9) == -1.3333333333333333


def test_polysync():
    assert polysync(BOSKA_3) == 9
    assert polysync(BOSKA_8) == 7
    assert polysync(BOSKA_9) == 20


def test_polyevenness():
    assert polyevenness(BOSKA_3) == 5.2753683906977775
    assert polyevenness(BOSKA_8) == 4.428794764473658
    assert polyevenness(BOSKA_9) == 4.9758868520193955


def test_polybalance():
    assert polybalance(BOSKA_3) == 0.9618538544571633
    assert polybalance(BOSKA_8) == 0.9961791398488665
    assert polybalance(BOSKA_9) == 0.7964353630870814


def test_polyD():
    assert polyD(BOSKA_3) == 19
    assert polyD(BOSKA_8) == 25
    assert polyD(BOSKA_9) == 24


def test_pattlist2descriptors():
    assert pattlist2descriptors(BOSKA_3) == [
        5,
        4,
        5,
        10,
        0.6875,
        0.36363636363636365,
        0.45454545454545453,
        0.9090909090909091,
        -7,
        -4,
        -10,
        -1.75,
        -0.8,
        -1.0,
        9,
        5.2753683906977775,
        0.9618538544571633,
        19,
    ]
    assert pattlist2descriptors(BOSKA_8) == [
        4,
        6,
        10,
        9,
        1.0,
        0.375,
        0.625,
        0.5625,
        3,
        -4,
        -5,
        0.5,
        -0.4,
        -0.5555555555555556,
        7,
        4.428794764473658,
        0.9961791398488665,
        25,
    ]
    assert pattlist2descriptors(BOSKA_9) == [
        6,
        8,
        7,
        9,
        0.875,
        0.5714285714285714,
        0.5,
        0.6428571428571429,
        4,
        2,
        -12,
        0.5,
        0.2857142857142857,
        -1.3333333333333333,
        20,
        4.9758868520193955,
        0.7964353630870814,
        24,
    ]