from fixtures import (
    BOSKA_3,
    BOSKA_3_PATTLIST,
    BOSKA_8,
    BOSKA_8_PATTLIST,
    BOSKA_9,
    BOSKA_9_PATTLIST,
)

from rhythmtoolbox import (
    pattlist2descriptors,
    pianoroll2descriptors,
    midifile2descriptors,
)


def test_midifile2descriptors():
    v = midifile2descriptors("midi/boska/3.mid")
    assert v["noi"] == 5
    assert v["lowDensity"] == 4
    assert v["midDensity"] == 5
    assert v["hiDensity"] == 10
    assert v["stepDensity"] == 0.6875
    assert v["lowness"] == 0.36363636363636365
    assert v["midness"] == 0.45454545454545453
    assert v["hiness"] == 0.9090909090909091
    assert v["lowSync"] == -7
    assert v["midSync"] == -4
    assert v["hiSync"] == -10
    assert v["lowSyness"] == -1.75
    assert v["midSyness"] == -0.8
    assert v["hiSyness"] == -1.0
    assert v["polySync"] == 9
    assert v["polyEvenness"] == 5.2753683906977775
    assert v["polyBalance"] == 0.9618538544571633
    assert v["polyDensity"] == 19

    v = midifile2descriptors("midi/boska/8.mid")
    assert v["noi"] == 4
    assert v["lowDensity"] == 6
    assert v["midDensity"] == 10
    assert v["hiDensity"] == 9
    assert v["stepDensity"] == 1.0
    assert v["lowness"] == 0.375
    assert v["midness"] == 0.625
    assert v["hiness"] == 0.5625
    assert v["lowSync"] == 3
    assert v["midSync"] == -4
    assert v["hiSync"] == -5
    assert v["lowSyness"] == 0.5
    assert v["midSyness"] == -0.4
    assert v["hiSyness"] == -0.5555555555555556
    assert v["polySync"] == 7
    assert v["polyEvenness"] == 4.428794764473658
    assert v["polyBalance"] == 0.9961791398488665
    assert v["polyDensity"] == 25

    v = midifile2descriptors("midi/boska/9.mid")
    assert v["noi"] == 6
    assert v["lowDensity"] == 8
    assert v["midDensity"] == 7
    assert v["hiDensity"] == 9
    assert v["stepDensity"] == 0.875
    assert v["lowness"] == 0.5714285714285714
    assert v["midness"] == 0.5
    assert v["hiness"] == 0.6428571428571429
    assert v["lowSync"] == 4
    assert v["midSync"] == 2
    assert v["hiSync"] == -12
    assert v["lowSyness"] == 0.5
    assert v["midSyness"] == 0.2857142857142857
    assert v["hiSyness"] == -1.3333333333333333
    assert v["polySync"] == 20
    assert v["polyEvenness"] == 4.9758868520193955
    assert v["polyBalance"] == 0.7964353630870814
    assert v["polyDensity"] == 24


def test_pianoroll2descriptors():
    v = pianoroll2descriptors(BOSKA_3)
    assert v["noi"] == 5
    assert v["lowDensity"] == 4
    assert v["midDensity"] == 5
    assert v["hiDensity"] == 10
    assert v["stepDensity"] == 0.6875
    assert v["lowness"] == 0.36363636363636365
    assert v["midness"] == 0.45454545454545453
    assert v["hiness"] == 0.9090909090909091
    assert v["lowSync"] == -7
    assert v["midSync"] == -4
    assert v["hiSync"] == -10
    assert v["lowSyness"] == -1.75
    assert v["midSyness"] == -0.8
    assert v["hiSyness"] == -1.0
    assert v["polySync"] == 9
    assert v["polyEvenness"] == 5.2753683906977775
    assert v["polyBalance"] == 0.9618538544571633
    assert v["polyDensity"] == 19
    assert v["syness"] == -0.6363636363636364
    assert v["balance"] == 0.8855199884772941
    assert v["evenness"] == 0.9649989736702275
    assert v["sync"] == -7

    v = pianoroll2descriptors(BOSKA_3, drums=False)
    assert v["noi"] == 5
    assert v["stepDensity"] == 0.6875
    assert v["polyDensity"] == 11
    assert v["sync"] == 0
    assert v["balance"] == 0.8855199884772941
    assert v["evenness"] == 0.9649989736702275
    assert v["syness"] == -0.6363636363636364
    assert v["lowDensity"] is None
    assert v["midDensity"] is None
    assert v["hiDensity"] is None
    assert v["lowness"] is None
    assert v["midness"] is None
    assert v["hiness"] is None
    assert v["lowSync"] is None
    assert v["midSync"] is None
    assert v["hiSync"] is None
    assert v["polySync"] is None
    assert v["lowSyness"] is None
    assert v["midSyness"] is None
    assert v["hiSyness"] is None
    assert v["polyBalance"] is None
    assert v["polyEvenness"] is None

    v = pianoroll2descriptors(BOSKA_8)
    assert v["noi"] == 4
    assert v["stepDensity"] == 1.0
    assert v["lowDensity"] == 6
    assert v["midDensity"] == 10
    assert v["hiDensity"] == 9
    assert v["polyDensity"] == 25
    assert v["lowness"] == 0.375
    assert v["midness"] == 0.625
    assert v["hiness"] == 0.5625
    assert v["sync"] == 0
    assert v["lowSync"] == 3
    assert v["midSync"] == -4
    assert v["hiSync"] == -5
    assert v["polySync"] == 7
    assert v["lowSyness"] == 0.5
    assert v["midSyness"] == -0.4
    assert v["hiSyness"] == -0.5555555555555556
    assert v["balance"] == 0.9999999999999999
    assert v["polyBalance"] == 0.9961791398488665
    assert v["evenness"] == 1.0
    assert v["polyEvenness"] == 4.428794764473658
    assert v["syness"] == 0.0

    v = pianoroll2descriptors(BOSKA_8, drums=False)
    assert v["noi"] == 4
    assert v["stepDensity"] == 1.0
    assert v["polyDensity"] == 16
    assert v["sync"] == 0
    assert v["balance"] == 0.9999999999999999
    assert v["evenness"] == 1.0
    assert v["syness"] == 0.0
    assert v["lowDensity"] is None
    assert v["midDensity"] is None
    assert v["hiDensity"] is None
    assert v["lowness"] is None
    assert v["midness"] is None
    assert v["hiness"] is None
    assert v["lowSync"] is None
    assert v["midSync"] is None
    assert v["hiSync"] is None
    assert v["polySync"] is None
    assert v["lowSyness"] is None
    assert v["midSyness"] is None
    assert v["hiSyness"] is None
    assert v["polyBalance"] is None
    assert v["polyEvenness"] is None

    v = pianoroll2descriptors(BOSKA_9)
    assert v["noi"] == 6
    assert v["stepDensity"] == 0.875
    assert v["lowDensity"] == 8
    assert v["midDensity"] == 7
    assert v["hiDensity"] == 9
    assert v["polyDensity"] == 24
    assert v["lowness"] == 0.5714285714285714
    assert v["midness"] == 0.5
    assert v["hiness"] == 0.6428571428571429
    assert v["sync"] == -3
    assert v["lowSync"] == 4
    assert v["midSync"] == 2
    assert v["hiSync"] == -12
    assert v["polySync"] == 20
    assert v["lowSyness"] == 0.5
    assert v["midSyness"] == 0.2857142857142857
    assert v["hiSyness"] == -1.3333333333333333
    assert v["balance"] == 0.8680172096412447
    assert v["polyBalance"] == 0.7964353630870814
    assert v["evenness"] == 0.9551143976077295
    assert v["polyEvenness"] == 4.9758868520193955
    assert v["syness"] == -0.21428571428571427

    v = pianoroll2descriptors(BOSKA_9, drums=False)
    assert v["noi"] == 6
    assert v["stepDensity"] == 0.875
    assert v["polyDensity"] == 14
    assert v["sync"] == 0
    assert v["balance"] == 0.8680172096412447
    assert v["evenness"] == 0.9551143976077295
    assert v["syness"] == -0.21428571428571427
    assert v["lowDensity"] is None
    assert v["midDensity"] is None
    assert v["hiDensity"] is None
    assert v["lowness"] is None
    assert v["midness"] is None
    assert v["hiness"] is None
    assert v["lowSync"] is None
    assert v["midSync"] is None
    assert v["hiSync"] is None
    assert v["polySync"] is None
    assert v["lowSyness"] is None
    assert v["midSyness"] is None
    assert v["hiSyness"] is None
    assert v["polyBalance"] is None
    assert v["polyEvenness"] is None


def test_pattlist2descriptors():
    v = pattlist2descriptors(BOSKA_3_PATTLIST)
    assert v["noi"] == 5
    assert v["lowDensity"] == 4
    assert v["midDensity"] == 5
    assert v["hiDensity"] == 10
    assert v["stepDensity"] == 0.6875
    assert v["lowness"] == 0.36363636363636365
    assert v["midness"] == 0.45454545454545453
    assert v["hiness"] == 0.9090909090909091
    assert v["lowSync"] == -7
    assert v["midSync"] == -4
    assert v["hiSync"] == -10
    assert v["lowSyness"] == -1.75
    assert v["midSyness"] == -0.8
    assert v["hiSyness"] == -1.0
    assert v["polySync"] == 9
    assert v["polyEvenness"] == 5.2753683906977775
    assert v["polyBalance"] == 0.9618538544571633
    assert v["polyDensity"] == 19

    v = pattlist2descriptors(BOSKA_8_PATTLIST)
    assert v["noi"] == 4
    assert v["lowDensity"] == 6
    assert v["midDensity"] == 10
    assert v["hiDensity"] == 9
    assert v["stepDensity"] == 1.0
    assert v["lowness"] == 0.375
    assert v["midness"] == 0.625
    assert v["hiness"] == 0.5625
    assert v["lowSync"] == 3
    assert v["midSync"] == -4
    assert v["hiSync"] == -5
    assert v["lowSyness"] == 0.5
    assert v["midSyness"] == -0.4
    assert v["hiSyness"] == -0.5555555555555556
    assert v["polySync"] == 7
    assert v["polyEvenness"] == 4.428794764473658
    assert v["polyBalance"] == 0.9961791398488665
    assert v["polyDensity"] == 25

    v = pattlist2descriptors(BOSKA_9_PATTLIST)
    assert v["noi"] == 6
    assert v["lowDensity"] == 8
    assert v["midDensity"] == 7
    assert v["hiDensity"] == 9
    assert v["stepDensity"] == 0.875
    assert v["lowness"] == 0.5714285714285714
    assert v["midness"] == 0.5
    assert v["hiness"] == 0.6428571428571429
    assert v["lowSync"] == 4
    assert v["midSync"] == 2
    assert v["hiSync"] == -12
    assert v["lowSyness"] == 0.5
    assert v["midSyness"] == 0.2857142857142857
    assert v["hiSyness"] == -1.3333333333333333
    assert v["polySync"] == 20
    assert v["polyEvenness"] == 4.9758868520193955
    assert v["polyBalance"] == 0.7964353630870814
    assert v["polyDensity"] == 24
