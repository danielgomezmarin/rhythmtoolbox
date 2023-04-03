from fixtures import BOSKA_3, BOSKA_8, BOSKA_9, PATT_1, PATT_2

from rhythmtoolbox.descriptors import (
    balance,
    bandness,
    density,
    evenness,
    get_n_onset_steps,
    noi,
    poly_balance,
    poly_density,
    poly_evenness,
    poly_sync,
    step_density,
    syncopation16,
    syncopation16_awareness,
    syness,
)
from rhythmtoolbox.midi_mapping import get_bands


def test_syncopation16_awareness():
    assert syncopation16_awareness(PATT_1) == -11
    assert syncopation16_awareness(PATT_2) == -39


def test_evenness():
    assert evenness(PATT_1) == 0.9816064222042191
    assert evenness(PATT_2) == 0.971165288619607


def test_balance():
    assert balance(PATT_1) == 0.9297693395285831
    assert balance(PATT_2) == 0.9609819355967744


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


def test_stepDensity():
    assert step_density(BOSKA_3) == 0.6875
    assert step_density(BOSKA_8) == 1.0
    assert step_density(BOSKA_9) == 0.875


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


def test_polySync():
    lowband, midband, hiband = get_bands(BOSKA_3)
    assert poly_sync(lowband, midband, hiband) == 9

    lowband, midband, hiband = get_bands(BOSKA_8)
    assert poly_sync(lowband, midband, hiband) == 7

    lowband, midband, hiband = get_bands(BOSKA_9)
    assert poly_sync(lowband, midband, hiband) == 20


def test_polyEvenness():
    lowband, midband, hiband = get_bands(BOSKA_3)
    assert poly_evenness(lowband, midband, hiband) == 5.2753683906977775

    lowband, midband, hiband = get_bands(BOSKA_8)
    assert poly_evenness(lowband, midband, hiband) == 4.428794764473658

    lowband, midband, hiband = get_bands(BOSKA_9)
    assert poly_evenness(lowband, midband, hiband) == 4.9758868520193955


def test_polyBalance():
    lowband, midband, hiband = get_bands(BOSKA_3)
    assert poly_balance(lowband, midband, hiband) == 0.9618538544571633

    lowband, midband, hiband = get_bands(BOSKA_8)
    assert poly_balance(lowband, midband, hiband) == 0.9961791398488665

    lowband, midband, hiband = get_bands(BOSKA_9)
    assert poly_balance(lowband, midband, hiband) == 0.7964353630870814


def test_polyDensity():
    lowband, midband, hiband = get_bands(BOSKA_3)
    assert poly_density(lowband, midband, hiband) == 19

    lowband, midband, hiband = get_bands(BOSKA_8)
    assert poly_density(lowband, midband, hiband) == 25

    lowband, midband, hiband = get_bands(BOSKA_9)
    assert poly_density(lowband, midband, hiband) == 24
