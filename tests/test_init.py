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

for roll in [BOSKA_3,BOSKA_8,BOSKA_9]:
    print('---')
    print(pianoroll2descriptors(roll))
    print()
    print(pianoroll2descriptors(roll, drums=False))
    print('---')


def test_midifile2descriptors():
    v = midifile2descriptors("midi/boska/3.mid")
    assert v["noi"] == 5
    assert v["polyDensity"] == 20
    assert v["lowDensity"] == 4
    assert v["midDensity"] == 7
    assert v["hiDensity"] == 9
    assert v["lowness"] == 0.36363636363636365
    assert v["midness"] == 0.6363636363636364
    assert v["hiness"] == 0.8181818181818182
    assert v["stepDensity"] == 0.6875
    assert v["sync"] == -10
    assert v["lowSync"] == -7
    assert v["midSync"] == -4
    assert v["hiSync"] == -14
    assert v["syness"] == -0.9090909090909091
    assert v["lowSyness"] == -1.75
    assert v["midSyness"] == -0.5714285714285714
    assert v["hiSyness"] == -1.5555555555555556
    assert v["balance"] == 0.9623442216024459
    assert v["polyBalance"] == 0.8621714780149552
    assert v["evenness"] == 0.9841710008484362
    assert v["polyEvenness"] == 4.818647489725106
    assert v["polySync"] == 13

    v = midifile2descriptors("midi/boska/8.mid")
    assert v["noi"] == 5
    assert v["polyDensity"] == 12
    assert v["lowDensity"] == 2
    assert v["midDensity"] == 7
    assert v["hiDensity"] == 3
    assert v["lowness"] == 0.2222222222222222
    assert v["midness"] == 0.7777777777777778
    assert v["hiness"] == 0.3333333333333333
    assert v["stepDensity"] == 0.5625
    assert v["sync"] == -4
    assert v["lowSync"] == 3
    assert v["midSync"] == -11
    assert v["hiSync"] == -7
    assert v["syness"] == -0.4444444444444444
    assert v["lowSyness"] == 1.5
    assert v["midSyness"] == -1.5714285714285714
    assert v["hiSyness"] == -2.3333333333333335
    assert v["balance"] == 0.8779951001768869
    assert v["polyBalance"] == 0.9023419344890125
    assert v["evenness"] == 0.9462279747433523
    assert v["polyEvenness"] == 5.099656633584969
    assert v["polySync"] == 0

    v = midifile2descriptors("midi/boska/9.mid")
    assert v["noi"] == 6
    assert v["polyDensity"] == 17
    assert v["lowDensity"] == 4
    assert v["midDensity"] == 6
    assert v["hiDensity"] == 7
    assert v["lowness"] == 0.4444444444444444
    assert v["midness"] == 0.6666666666666666
    assert v["hiness"] == 0.7777777777777778
    assert v["stepDensity"] == 0.5625
    assert v["sync"] == -10
    assert v["lowSync"] == -6
    assert v["midSync"] == -3
    assert v["hiSync"] == -14
    assert v["syness"] == -1.1111111111111112
    assert v["lowSyness"] == -1.5
    assert v["midSyness"] == -0.5
    assert v["hiSyness"] == -2.0
    assert v["balance"] == 0.905804548330825
    assert v["polyBalance"] == 0.7646388055112554
    assert v["evenness"] == 0.9842351591376168
    assert v["polyEvenness"] == 4.930845709389592
    assert v["polySync"] == 3


def test_pianoroll2descriptors():
    v = pianoroll2descriptors(BOSKA_3)
    assert v["noi"] == 5
    assert v["polyDensity"] == 19
    assert v["lowDensity"] == 4
    assert v["midDensity"] == 5
    assert v["hiDensity"] == 10
    assert v["lowness"] == 0.36363636363636365
    assert v["midness"] == 0.45454545454545453
    assert v["hiness"] == 0.9090909090909091
    assert v["stepDensity"] == 0.6875
    assert v["sync"] == -7
    assert v["lowSync"] == -7
    assert v["midSync"] == -4
    assert v["hiSync"] == -10
    assert v["syness"] == -0.6363636363636364
    assert v["lowSyness"] == -1.75
    assert v["midSyness"] == -0.8
    assert v["hiSyness"] == -1.0
    assert v["balance"] == 0.8855199884772941
    assert v["polyBalance"] == 0.9618538544571633
    assert v["evenness"] == 0.9649989736702275
    assert v["polyEvenness"] == 5.2753683906977775
    assert v["polySync"] == 9

    v = pianoroll2descriptors(BOSKA_3, drums=False)
    assert v["noi"] == 5
    assert v["polyDensity"] == 11
    assert v["lowDensity"] is None
    assert v["midDensity"] is None
    assert v["hiDensity"] is None
    assert v["lowness"] is None
    assert v["midness"] is None
    assert v["hiness"] is None
    assert v["stepDensity"] == 0.6875
    assert v["sync"] == -7
    assert v["lowSync"] is None
    assert v["midSync"] is None
    assert v["hiSync"] is None
    assert v["syness"] == -0.6363636363636364
    assert v["lowSyness"] is None
    assert v["midSyness"] is None
    assert v["hiSyness"] is None
    assert v["balance"] == 0.8855199884772941
    assert v["polyBalance"] is None
    assert v["evenness"] == 0.9649989736702275
    assert v["polyEvenness"] is None
    assert v["polySync"] is None

    v = pianoroll2descriptors(BOSKA_8)
    assert v["noi"] == 4
    assert v["polyDensity"] == 25
    assert v["lowDensity"] == 6
    assert v["midDensity"] == 10
    assert v["hiDensity"] == 9
    assert v["lowness"] == 0.375
    assert v["midness"] == 0.625
    assert v["hiness"] == 0.5625
    assert v["stepDensity"] == 1.0
    assert v["sync"] == 0
    assert v["lowSync"] == 3
    assert v["midSync"] == -4
    assert v["hiSync"] == -5
    assert v["syness"] == 0.0
    assert v["lowSyness"] == 0.5
    assert v["midSyness"] == -0.4
    assert v["hiSyness"] == -0.5555555555555556
    assert v["balance"] == 0.9999999999999999
    assert v["polyBalance"] == 0.9961791398488665
    assert v["evenness"] == 1.0
    assert v["polyEvenness"] == 4.428794764473658
    assert v["polySync"] == 7

    v = pianoroll2descriptors(BOSKA_8, drums=False)
    assert v["noi"] == 4
    assert v["polyDensity"] == 16
    assert v["lowDensity"] is None
    assert v["midDensity"] is None
    assert v["hiDensity"] is None
    assert v["lowness"] is None
    assert v["midness"] is None
    assert v["hiness"] is None
    assert v["stepDensity"] == 1.0
    assert v["sync"] == 0
    assert v["lowSync"] is None
    assert v["midSync"] is None
    assert v["hiSync"] is None
    assert v["syness"] == 0.0
    assert v["lowSyness"] is None
    assert v["midSyness"] is None
    assert v["hiSyness"] is None
    assert v["balance"] == 0.9999999999999999
    assert v["polyBalance"] is None
    assert v["evenness"] == 1.0
    assert v["polyEvenness"] is None
    assert v["polySync"] is None

    v = pianoroll2descriptors(BOSKA_9)
    assert v["noi"] == 6
    assert v["polyDensity"] == 24
    assert v["lowDensity"] == 8
    assert v["midDensity"] == 7
    assert v["hiDensity"] == 9
    assert v["lowness"] == 0.5714285714285714
    assert v["midness"] == 0.5
    assert v["hiness"] == 0.6428571428571429
    assert v["stepDensity"] == 0.875
    assert v["sync"] == -3
    assert v["lowSync"] == 4
    assert v["midSync"] == 2
    assert v["hiSync"] == -12
    assert v["syness"] == -0.21428571428571427
    assert v["lowSyness"] == 0.5
    assert v["midSyness"] == 0.2857142857142857
    assert v["hiSyness"] == -1.3333333333333333
    assert v["balance"] == 0.8680172096412447
    assert v["polyBalance"] == 0.7964353630870814
    assert v["evenness"] == 0.9551143976077295
    assert v["polyEvenness"] == 4.9758868520193955
    assert v["polySync"] == 20

    v = pianoroll2descriptors(BOSKA_9, drums=False)
    assert v["noi"] == 6
    assert v["polyDensity"] == 14
    assert v["lowDensity"] is None
    assert v["midDensity"] is None
    assert v["hiDensity"] is None
    assert v["lowness"] is None
    assert v["midness"] is None
    assert v["hiness"] is None
    assert v["stepDensity"] == 0.875
    assert v["sync"] == -3
    assert v["lowSync"] is None
    assert v["midSync"] is None
    assert v["hiSync"] is None
    assert v["syness"] == -0.21428571428571427
    assert v["lowSyness"] is None
    assert v["midSyness"] is None
    assert v["hiSyness"] is None
    assert v["balance"] == 0.8680172096412447
    assert v["polyBalance"] is None
    assert v["evenness"] == 0.9551143976077295
    assert v["polyEvenness"] is None
    assert v["polySync"] is None


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
