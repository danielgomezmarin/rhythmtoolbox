from rhythmtoolbox import pattlist_to_pianoroll

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
