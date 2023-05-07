from .fixtures import (
    BOSKA_3,
    BOSKA_3_DESCRIPTORS,
    BOSKA_8,
    BOSKA_8_DESCRIPTORS,
    BOSKA_9,
    BOSKA_9_DESCRIPTORS,
    PATT_1,
    PATT_2,
)

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
    assert noi(BOSKA_3) == BOSKA_3_DESCRIPTORS["noi"]
    assert noi(BOSKA_8) == BOSKA_8_DESCRIPTORS["noi"]
    assert noi(BOSKA_9) == BOSKA_9_DESCRIPTORS["noi"]


def test_density():
    lowband, midband, hiband = get_bands(BOSKA_3)
    assert density(lowband) == BOSKA_3_DESCRIPTORS["lowDensity"]
    assert density(midband) == BOSKA_3_DESCRIPTORS["midDensity"]
    assert density(hiband) == BOSKA_3_DESCRIPTORS["hiDensity"]

    lowband, midband, hiband = get_bands(BOSKA_8)
    assert density(lowband) == BOSKA_8_DESCRIPTORS["lowDensity"]
    assert density(midband) == BOSKA_8_DESCRIPTORS["midDensity"]
    assert density(hiband) == BOSKA_8_DESCRIPTORS["hiDensity"]

    lowband, midband, hiband = get_bands(BOSKA_9)
    assert density(lowband) == BOSKA_9_DESCRIPTORS["lowDensity"]
    assert density(midband) == BOSKA_9_DESCRIPTORS["midDensity"]
    assert density(hiband) == BOSKA_9_DESCRIPTORS["hiDensity"]


def test_stepDensity():
    assert step_density(BOSKA_3) == BOSKA_3_DESCRIPTORS["stepDensity"]
    assert step_density(BOSKA_8) == BOSKA_8_DESCRIPTORS["stepDensity"]
    assert step_density(BOSKA_9) == BOSKA_9_DESCRIPTORS["stepDensity"]


def test_bandness():
    n_onset_steps = get_n_onset_steps(BOSKA_3)
    lowband, midband, hiband = get_bands(BOSKA_3)
    assert bandness(lowband, n_onset_steps) == BOSKA_3_DESCRIPTORS["lowness"]
    assert bandness(midband, n_onset_steps) == BOSKA_3_DESCRIPTORS["midness"]
    assert bandness(hiband, n_onset_steps) == BOSKA_3_DESCRIPTORS["hiness"]

    n_onset_steps = get_n_onset_steps(BOSKA_8)
    lowband, midband, hiband = get_bands(BOSKA_8)
    assert bandness(lowband, n_onset_steps) == BOSKA_8_DESCRIPTORS["lowness"]
    assert bandness(midband, n_onset_steps) == BOSKA_8_DESCRIPTORS["midness"]
    assert bandness(hiband, n_onset_steps) == BOSKA_8_DESCRIPTORS["hiness"]

    n_onset_steps = get_n_onset_steps(BOSKA_9)
    lowband, midband, hiband = get_bands(BOSKA_9)
    assert bandness(lowband, n_onset_steps) == BOSKA_9_DESCRIPTORS["lowness"]
    assert bandness(midband, n_onset_steps) == BOSKA_9_DESCRIPTORS["midness"]
    assert bandness(hiband, n_onset_steps) == BOSKA_9_DESCRIPTORS["hiness"]


def test_syncopation16():
    assert syncopation16(PATT_1) == -4
    assert syncopation16(PATT_2) == -10

    lowband, midband, hiband = get_bands(BOSKA_3)
    assert syncopation16(lowband) == BOSKA_3_DESCRIPTORS["lowSync"]
    assert syncopation16(midband) == BOSKA_3_DESCRIPTORS["midSync"]
    assert syncopation16(hiband) == BOSKA_3_DESCRIPTORS["hiSync"]
    lowband, midband, hiband = get_bands(BOSKA_8)
    assert syncopation16(lowband) == BOSKA_8_DESCRIPTORS["lowSync"]
    assert syncopation16(midband) == BOSKA_8_DESCRIPTORS["midSync"]
    assert syncopation16(hiband) == BOSKA_8_DESCRIPTORS["hiSync"]
    lowband, midband, hiband = get_bands(BOSKA_9)
    assert syncopation16(lowband) == BOSKA_9_DESCRIPTORS["lowSync"]
    assert syncopation16(midband) == BOSKA_9_DESCRIPTORS["midSync"]
    assert syncopation16(hiband) == BOSKA_9_DESCRIPTORS["hiSync"]


def test_syness():
    lowband, midband, hiband = get_bands(BOSKA_3)
    assert syness(lowband) == BOSKA_3_DESCRIPTORS["lowSyness"]
    assert syness(midband) == BOSKA_3_DESCRIPTORS["midSyness"]
    assert syness(hiband) == BOSKA_3_DESCRIPTORS["hiSyness"]

    lowband, midband, hiband = get_bands(BOSKA_8)
    assert syness(lowband) == BOSKA_8_DESCRIPTORS["lowSyness"]
    assert syness(midband) == BOSKA_8_DESCRIPTORS["midSyness"]
    assert syness(hiband) == BOSKA_8_DESCRIPTORS["hiSyness"]

    lowband, midband, hiband = get_bands(BOSKA_9)
    assert syness(lowband) == BOSKA_9_DESCRIPTORS["lowSyness"]
    assert syness(midband) == BOSKA_9_DESCRIPTORS["midSyness"]
    assert syness(hiband) == BOSKA_9_DESCRIPTORS["hiSyness"]


def test_polySync():
    lowband, midband, hiband = get_bands(BOSKA_3)
    assert poly_sync(lowband, midband, hiband) == BOSKA_3_DESCRIPTORS["polySync"]

    lowband, midband, hiband = get_bands(BOSKA_8)
    assert poly_sync(lowband, midband, hiband) == BOSKA_8_DESCRIPTORS["polySync"]

    lowband, midband, hiband = get_bands(BOSKA_9)
    assert poly_sync(lowband, midband, hiband) == BOSKA_9_DESCRIPTORS["polySync"]


def test_polyEvenness():
    lowband, midband, hiband = get_bands(BOSKA_3)
    assert (
        poly_evenness(lowband, midband, hiband) == BOSKA_3_DESCRIPTORS["polyEvenness"]
    )

    lowband, midband, hiband = get_bands(BOSKA_8)
    assert (
        poly_evenness(lowband, midband, hiband) == BOSKA_8_DESCRIPTORS["polyEvenness"]
    )

    lowband, midband, hiband = get_bands(BOSKA_9)
    assert (
        poly_evenness(lowband, midband, hiband) == BOSKA_9_DESCRIPTORS["polyEvenness"]
    )


def test_polyBalance():
    lowband, midband, hiband = get_bands(BOSKA_3)
    assert poly_balance(lowband, midband, hiband) == BOSKA_3_DESCRIPTORS["polyBalance"]

    lowband, midband, hiband = get_bands(BOSKA_8)
    assert poly_balance(lowband, midband, hiband) == BOSKA_8_DESCRIPTORS["polyBalance"]

    lowband, midband, hiband = get_bands(BOSKA_9)
    assert poly_balance(lowband, midband, hiband) == BOSKA_9_DESCRIPTORS["polyBalance"]


def test_polyDensity():
    lowband, midband, hiband = get_bands(BOSKA_3)
    assert poly_density(lowband, midband, hiband) == BOSKA_3_DESCRIPTORS["polyDensity"]

    lowband, midband, hiband = get_bands(BOSKA_8)
    assert poly_density(lowband, midband, hiband) == BOSKA_8_DESCRIPTORS["polyDensity"]

    lowband, midband, hiband = get_bands(BOSKA_9)
    assert poly_density(lowband, midband, hiband) == BOSKA_9_DESCRIPTORS["polyDensity"]
