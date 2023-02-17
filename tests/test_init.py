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
    v = midifile2descriptors("assets/midi/boska/3.mid")
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

    v = midifile2descriptors("assets/midi/boska/8.mid")
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

    v = midifile2descriptors("assets/midi/boska/9.mid")
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
