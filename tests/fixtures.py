from rhythmtoolbox import pattlist_to_pianoroll

# TODO: add test case for non-16-step pattern
PATT_1 = [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]
PATT_2 = [1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0]

BOSKA_3_PATTLIST = [
    [36, 38, 42],
    [],
    [42],
    [38, 42],
    [46],
    [],
    [36, 38, 42],
    [],
    [42],
    [38],
    [36, 42],
    [],
    [38, 46],
    [],
    [38, 42, 64],
    [38],
]

BOSKA_3 = pattlist_to_pianoroll(BOSKA_3_PATTLIST)

BOSKA_3_DESCRIPTORS = {
    "noi": 5,
    "polyDensity": 20,
    "lowDensity": 4,
    "midDensity": 7,
    "hiDensity": 9,
    "lowness": 0.36363636363636365,
    "midness": 0.6363636363636364,
    "hiness": 0.8181818181818182,
    "stepDensity": 0.6875,
    "sync": -10,
    "lowSync": -7,
    "midSync": -4,
    "hiSync": -14,
    "syness": -0.9090909090909091,
    "lowSyness": -1.75,
    "midSyness": -0.5714285714285714,
    "hiSyness": -1.5555555555555556,
    "balance": 0.9623442216024459,
    "polyBalance": 0.8621714780149552,
    "evenness": 0.9841710008484362,
    "polyEvenness": 4.818647489725106,
    "polySync": 13,
}

BOSKA_8_PATTLIST = [
    [38, 39, 46],
    [],
    [37],
    [36],
    [],
    [],
    [38, 39, 46],
    [],
    [37],
    [36],
    [],
    [],
    [38, 39, 46],
    [38, 39, 46],
    [37],
    [38],
]

BOSKA_8 = pattlist_to_pianoroll(BOSKA_8_PATTLIST)

BOSKA_8_DESCRIPTORS = {
    "noi": 5,
    "polyDensity": 14,
    "lowDensity": 2,
    "midDensity": 8,
    "hiDensity": 4,
    "lowness": 0.2,
    "midness": 0.8,
    "hiness": 0.4,
    "stepDensity": 0.625,
    "sync": -2,
    "lowSync": 3,
    "midSync": -9,
    "hiSync": -4,
    "syness": -0.2,
    "lowSyness": 1.5,
    "midSyness": -1.125,
    "hiSyness": -1.0,
    "balance": 0.8186690031367755,
    "polyBalance": 0.7887402430901225,
    "evenness": 0.8820076387881416,
    "polyEvenness": 4.575377577313285,
    "polySync": 0,
}

BOSKA_9_PATTLIST = [
    [36, 42],
    [],
    [42],
    [],
    [42],
    [],
    [36, 38, 46],
    [],
    [37, 42],
    [36, 38],
    [],
    [37],
    [36, 38, 42],
    [],
    [37, 38, 39, 42, 46],
    [],
]

BOSKA_9 = pattlist_to_pianoroll(BOSKA_9_PATTLIST)

BOSKA_9_DESCRIPTORS = {
    "noi": 6,
    "polyDensity": 17,
    "lowDensity": 4,
    "midDensity": 6,
    "hiDensity": 7,
    "lowness": 0.4444444444444444,
    "midness": 0.6666666666666666,
    "hiness": 0.7777777777777778,
    "stepDensity": 0.5625,
    "sync": -10,
    "lowSync": -6,
    "midSync": -3,
    "hiSync": -14,
    "syness": -1.1111111111111112,
    "lowSyness": -1.5,
    "midSyness": -0.5,
    "hiSyness": -2.0,
    "balance": 0.905804548330825,
    "polyBalance": 0.7646388055112554,
    "evenness": 0.9842351591376168,
    "polyEvenness": 4.930845709389592,
    "polySync": 3,
}
