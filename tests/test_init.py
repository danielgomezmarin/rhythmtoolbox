import numpy as np
from .fixtures import (
    BOSKA_3,
    BOSKA_3_DESCRIPTORS,
    BOSKA_3_PATTLIST,
    BOSKA_8,
    BOSKA_8_DESCRIPTORS,
    BOSKA_8_PATTLIST,
    BOSKA_9,
    BOSKA_9_DESCRIPTORS,
    BOSKA_9_PATTLIST,
    FOUR_KICKS_DESCRIPTORS,
    UNBALANCED_1_DESCRIPTORS,
)

from rhythmtoolbox import (
    midifile2descriptors,
    pattlist2descriptors,
    pianoroll2descriptors,
)


def test_midifile2descriptors():
    file_descriptors = {
        "midi/boska/3.mid": BOSKA_3_DESCRIPTORS,
        "midi/two_bar/four_kicks.mid": FOUR_KICKS_DESCRIPTORS,
        "midi/two_bar/unbalanced_1.mid": UNBALANCED_1_DESCRIPTORS,
    }
    for f in file_descriptors:
        v = midifile2descriptors(f)
        assert set(v) == set(file_descriptors[f])
        for k in v:
            assert np.isclose(v[k], file_descriptors[f][k])

    v = midifile2descriptors("midi/boska/8.mid")
    assert np.isclose(v["noi"], 5)
    assert np.isclose(v["polyDensity"], 12)
    assert np.isclose(v["lowDensity"], 2)
    assert np.isclose(v["midDensity"], 7)
    assert np.isclose(v["hiDensity"], 3)
    assert np.isclose(v["lowness"], 0.2222222222222222)
    assert np.isclose(v["midness"], 0.7777777777777778)
    assert np.isclose(v["hiness"], 0.3333333333333333)
    assert np.isclose(v["stepDensity"], 0.5625)
    assert np.isclose(v["sync"], -4)
    assert np.isclose(v["lowSync"], 3)
    assert np.isclose(v["midSync"], -11)
    assert np.isclose(v["hiSync"], -7)
    assert np.isclose(v["syness"], -0.4444444444444444)
    assert np.isclose(v["lowSyness"], 1.5)
    assert np.isclose(v["midSyness"], -1.5714285714285714)
    assert np.isclose(v["hiSyness"], -2.3333333333333335)
    assert np.isclose(v["balance"], 0.8779951001768869)
    assert np.isclose(v["polyBalance"], 0.9023419344890125)
    assert np.isclose(v["evenness"], 0.9462279747433523)
    assert np.isclose(v["polyEvenness"], 5.099656633584969)
    assert np.isclose(v["polySync"], 0)

    v = midifile2descriptors("midi/boska/9.mid")
    assert np.isclose(v["noi"], 6)
    assert np.isclose(v["polyDensity"], 17)
    assert np.isclose(v["lowDensity"], 4)
    assert np.isclose(v["midDensity"], 6)
    assert np.isclose(v["hiDensity"], 7)
    assert np.isclose(v["lowness"], 0.4444444444444444)
    assert np.isclose(v["midness"], 0.6666666666666666)
    assert np.isclose(v["hiness"], 0.7777777777777778)
    assert np.isclose(v["stepDensity"], 0.5625)
    assert np.isclose(v["sync"], -10)
    assert np.isclose(v["lowSync"], -6)
    assert np.isclose(v["midSync"], -3)
    assert np.isclose(v["hiSync"], -14)
    assert np.isclose(v["syness"], -1.1111111111111112)
    assert np.isclose(v["lowSyness"], -1.5)
    assert np.isclose(v["midSyness"], -0.5)
    assert np.isclose(v["hiSyness"], -2.0)
    assert np.isclose(v["balance"], 0.905804548330825)
    assert np.isclose(v["polyBalance"], 0.7646388055112554)
    assert np.isclose(v["evenness"], 0.9842351591376168)
    assert np.isclose(v["polyEvenness"], 4.930845709389592)
    assert np.isclose(v["polySync"], 3)


def test_pianoroll2descriptors():
    v = pianoroll2descriptors(BOSKA_3)
    assert set(v) == set(BOSKA_3_DESCRIPTORS)
    for k in v:
        assert np.isclose(v[k], BOSKA_3_DESCRIPTORS[k])

    v = pianoroll2descriptors(BOSKA_3, drums=False)
    assert set(v) == set(BOSKA_3_DESCRIPTORS)
    assert np.isclose(v["noi"], 5)
    assert np.isclose(v["polyDensity"], 11)
    assert v["lowDensity"] is None
    assert v["midDensity"] is None
    assert v["hiDensity"] is None
    assert v["lowness"] is None
    assert v["midness"] is None
    assert v["hiness"] is None
    assert np.isclose(v["stepDensity"], 0.6875)
    assert np.isclose(v["sync"], -10)
    assert v["lowSync"] is None
    assert v["midSync"] is None
    assert v["hiSync"] is None
    assert np.isclose(v["syness"], -0.9090909090909091)
    assert v["lowSyness"] is None
    assert v["midSyness"] is None
    assert v["hiSyness"] is None
    assert np.isclose(v["balance"], 0.9623442216024459)
    assert v["polyBalance"] is None
    assert np.isclose(v["evenness"], 0.9841710008484362)
    assert v["polyEvenness"] is None
    assert v["polySync"] is None

    v = pianoroll2descriptors(BOSKA_8)
    assert set(v) == set(BOSKA_8_DESCRIPTORS)
    for k in v:
        assert np.isclose(v[k], BOSKA_8_DESCRIPTORS[k])

    v = pianoroll2descriptors(BOSKA_8, drums=False)
    assert set(v) == set(BOSKA_8_DESCRIPTORS)
    assert np.isclose(v["noi"], 5)
    assert np.isclose(v["polyDensity"], 10)
    assert v["lowDensity"] is None
    assert v["midDensity"] is None
    assert v["hiDensity"] is None
    assert v["lowness"] is None
    assert v["midness"] is None
    assert v["hiness"] is None
    assert np.isclose(v["stepDensity"], 0.625)
    assert np.isclose(v["sync"], -2)
    assert v["lowSync"] is None
    assert v["midSync"] is None
    assert v["hiSync"] is None
    assert np.isclose(v["syness"], -0.2)
    assert v["lowSyness"] is None
    assert v["midSyness"] is None
    assert v["hiSyness"] is None
    assert np.isclose(v["balance"], 0.8186690031367755)
    assert v["polyBalance"] is None
    assert np.isclose(v["evenness"], 0.8820076387881416)
    assert v["polyEvenness"] is None
    assert v["polySync"] is None

    v = pianoroll2descriptors(BOSKA_9)
    assert set(v) == set(BOSKA_9_DESCRIPTORS)
    for k in v:
        assert np.isclose(v[k], BOSKA_9_DESCRIPTORS[k])

    v = pianoroll2descriptors(BOSKA_9, drums=False)
    assert set(v) == set(BOSKA_9_DESCRIPTORS)
    assert np.isclose(v["noi"], 6)
    assert np.isclose(v["polyDensity"], 9)
    assert v["lowDensity"] is None
    assert v["midDensity"] is None
    assert v["hiDensity"] is None
    assert v["lowness"] is None
    assert v["midness"] is None
    assert v["hiness"] is None
    assert np.isclose(v["stepDensity"], 0.5625)
    assert np.isclose(v["sync"], -10)
    assert v["lowSync"] is None
    assert v["midSync"] is None
    assert v["hiSync"] is None
    assert np.isclose(v["syness"], -1.1111111111111112)
    assert v["lowSyness"] is None
    assert v["midSyness"] is None
    assert v["hiSyness"] is None
    assert np.isclose(v["balance"], 0.905804548330825)
    assert v["polyBalance"] is None
    assert np.isclose(v["evenness"], 0.9842351591376168)
    assert v["polyEvenness"] is None
    assert v["polySync"] is None


def test_pattlist2descriptors():
    v = pattlist2descriptors(BOSKA_3_PATTLIST)
    assert set(v) == set(BOSKA_3_DESCRIPTORS)
    for k in v:
        assert np.isclose(v[k], BOSKA_3_DESCRIPTORS[k])

    v = pattlist2descriptors(BOSKA_8_PATTLIST)
    assert set(v) == set(BOSKA_8_DESCRIPTORS)
    for k in v:
        assert np.isclose(v[k], BOSKA_8_DESCRIPTORS[k])

    v = pattlist2descriptors(BOSKA_9_PATTLIST)
    assert set(v) == set(BOSKA_9_DESCRIPTORS)
    for k in v:
        assert np.isclose(v[k], BOSKA_9_DESCRIPTORS[k])
