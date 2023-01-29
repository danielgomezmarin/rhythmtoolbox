"""This module defines a mapping of the General MIDI Percussion Key Map (GMPKM) to three frequency levels"""

low_instruments = [35, 36, 41, 45, 47, 64]
mid_instruments = [37, 38, 39, 40, 43, 48, 50, 58, 61, 62, 65, 77]
hi_instruments = [
    22,
    26,
    42,
    44,
    46,
    49,
    51,
    52,
    53,
    54,
    55,
    56,
    57,
    59,
    60,
    62,
    69,
    70,
    71,
    72,
    76,
]

GM_dict = {
    # Key is midi note number
    # Values are a list of:
    # [0] name (as string)
    # [1] name category low mid or high (as string)
    # [2] substiture midi number for simplified MIDI
    # [3] name of instrument for 8 note conversion (as string)
    # [4] number of instrument for 8 note conversion
    # [5] substiture midi number for conversion to 8 note
    22: ["Closed Hi-Hat edge", "high", 42, "CH", 3, 42],
    26: ["Open Hi-Hat edge", "high", 46, "OH", 4, 46],
    35: ["Acoustic Bass Drum", "low", 36, "K", 1, 36],
    36: ["Bass Drum 1", "low", 36, "K", 1, 36],
    37: ["Side Stick", "mid", 37, "RS", 6, 37],
    38: ["Acoustic Snare", "mid", 38, "SN", 2, 38],
    39: ["Hand Clap", "mid", 39, "CP", 5, 39],
    40: ["Electric Snare", "mid", 38, "SN", 2, 38],
    41: ["Low Floor Tom", "low", 45, "LT", 7, 45],
    42: ["Closed Hi Hat", "high", 42, "CH", 3, 42],
    43: ["High Floor Tom", "mid", 45, "HT", 8, 45],
    44: ["Pedal Hi-Hat", "high", 46, "OH", 4, 46],
    45: ["Low Tom", "low", 45, "LT", 7, 45],
    46: ["Open Hi-Hat", "high", 46, "OH", 4, 46],
    47: ["Low-Mid Tom", "low", 47, "MT", 7, 45],
    48: ["Hi-Mid Tom", "mid", 47, "MT", 7, 45],
    49: ["Crash Cymbal 1", "high", 49, "CC", 4, 46],
    50: ["High Tom", "mid", 50, "HT", 8, 50],
    51: ["Ride Cymbal 1", "high", 51, "RC", -1, 42],
    52: ["Chinese Cymbal", "high", 52, "", -1, 46],
    53: ["Ride Bell", "high", 53, "", -1, 42],
    54: ["Tambourine", "high", 54, "", -1, 42],
    55: ["Splash Cymbal", "high", 55, "OH", 4, 46],
    56: ["Cowbell", "high", 56, "CB", -1, -1],
    57: ["Crash Cymbal 2", "high", 57, "CC", 4, 46],
    58: ["Vibraslap", "mid", 58, "VS", 6, 37],
    59: ["Ride Cymbal 2", "high", 59, "RC", 3, 42],
    60: ["Hi Bongo", "high", 60, "LB", 8],
    61: ["Low Bongo", "mid", 61, "HB", 7],
    62: ["Mute Hi Conga", "mid", 62, "MC", 8, 50],
    63: ["Open Hi Conga", "high", 63, "HC", 8, 50],
    64: ["Low Conga", "low", 64, "LC", 7, 45],
    65: ["High Timbale", "mid", 65, "", 8],
    66: ["Low Timbale", "low", 66, "", 7],
    67: ["High Agogo", "", 67, "", -1],
    68: ["Low Agogo", "", 68, "", -1],
    69: ["Cabasa", "high", 70, "MA", -1],
    70: ["Maracas", "high", 70, "MA", -1],
    71: ["Short Whistle", "high", 71, "", -1],
    72: ["Long Whistle", "high", 72, ",-1"],
    73: ["Short Guiro", "", 73, "", -1],
    74: ["Long Guiro", "", 74, "", -1],
    75: ["Claves", "high", 75, "", -1],
    76: ["Hi Wood Block", "high", 76, "", 8],
    77: ["Low Wood Block", "mid", 77, "", 7],
    78: ["Mute Cuica", "", 78, "", -1],
    79: ["Open Cuica", "", 79, "", -1],
    80: ["Mute Triangle", "", 80, "", -1],
    81: ["Open Triangle", "", 81, "", -1],
}


def event_to_8number(midi_notes):
    # input an event list and output a representation
    # in 8 instrumental streams:
    # kick, snare, rimshot, clap, closed hihat, open hihat, low tom, high tom
    output = []
    # make sure the event has notes
    if len(midi_notes) == 0:
        return [0]

    for x in midi_notes:
        # print("x", x)
        output.append(GM_dict[x][4])

    # otherwise it is a silence
    output = list(set(output))
    output.sort()

    return output


def event_to_3number(midi_notes):
    # input an event list and output a representation
    # in 3 instrumental streams:
    # low, mid, high
    output = []
    # make sure the event has notes
    if len(midi_notes) == 0:
        return [0]

    for x in midi_notes:
        category = GM_dict[x][1]
        if category == "low":
            category_number = 1
        elif category == "mid":
            category_number = 2
        else:
            category_number = 3
        output.append(category_number)

    # otherwise it is a silence
    output = list(set(output))
    output.sort()

    return output
