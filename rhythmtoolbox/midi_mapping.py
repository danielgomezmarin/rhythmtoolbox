"""A mapping of the General MIDI Percussion Key Map (GMPKM) to three frequency levels: low, mid, and high"""

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

GM_dict={
# key is midi note number
# values are:
# [0] name (as string)
# [1] name category low mid or high (as string)
# [2] substiture midi number for simplified MIDI (all instruments)
# [3] name of instrument for 8 note conversion (as string)
# [4] number of instrument for 8 note conversion 
# [5] substiture midi number for conversion to 8 note
# [6] substiture midi number for conversion to 16 note
# [7] substiture midi number for conversion to 3 note
# if we are going to remap just use GM_dict[msg.note][X]

    22:['Closed Hi-Hat edge', 'high', 42, 'CH', 3,42,42],
    26:['Open Hi-Hat edge', 'high', 46, 'OH', 4,46,46],
    35:['Acoustic Bass Drum','low',36, 'K', 1, 36,36],
    36:['Bass Drum 1','low',36, 'K', 1, 36,36],
    37:['Side Stick','mid',37, 'RS', 6, 37,37],
    38:['Acoustic Snare','mid',38, 'SN', 2, 38,38],
    39:['Hand Clap','mid',39, 'CP', 5, 39, 39],
    40:['Electric Snare','mid',38, 'SN', 2, 38,38],
    41:['Low Floor Tom','low',45, 'LT', 7, 45,45],
    42:['Closed Hi Hat','high',42, 'CH', 3, 42,42],
    43:['High Floor Tom','mid',45, 'HT', 8, 45,45],
    44:['Pedal Hi-Hat','high',46, 'OH', 4, 46, 46],
    45:['Low Tom','low',45, 'LT', 7, 45, 45],
    46:['Open Hi-Hat','high',46, 'OH', 4, 46, 46],
    47:['Low-Mid Tom','low',47, 'MT', 7, 45, 47],
    48:['Hi-Mid Tom','mid',47, 'MT', 7, 50, 50],
    49:['Crash Cymbal 1','high',49, 'CC', 4, 46, 42],
    50:['High Tom','mid',50, 'HT', 8, 50, 50],
    51:['Ride Cymbal 1','high',51, 'RC', -1, 42, 51],
    52:['Chinese Cymbal','high',52, '', -1, 46, 51],
    53:['Ride Bell','high',53, '', -1, 42, 51],
    54:['Tambourine','high',54, '', -1, 42, 69],
    55:['Splash Cymbal','high',55, 'OH', 4, 46, 42],
    56:['Cowbell','high',56, 'CB', -1, 37, 56],
    57:['Crash Cymbal 2','high',57,'CC', 4,46, 42],
    58:['Vibraslap',"mid",58,'VS', 6,37, 37],
    59:['Ride Cymbal 2','high',59, 'RC',3, 42, 51],
    60:['Hi Bongo','high',60, 'LB', 8, 45,63],
    61:['Low Bongo','mid',61, 'HB', 7, 45, 64],
    62:['Mute Hi Conga','mid',62, 'MC', 8, 50, 62],
    63:['Open Hi Conga','high',63, 'HC', 8, 50, 63],
    64:['Low Conga','low',64, 'LC', 7, 45,64, 64],
    65:['High Timbale','mid',65, '',8, 45,63],
    66:['Low Timbale','low',66, '',7, 45,64],
    67:['High Agogo','',67, '',-1, 37,56],
    68:['Low Agogo','',68,'',- 1 , 37,56],
    69:['Cabasa','high',69, 'MA',-1, 42,69],
    70:['Maracas','high',69, 'MA',-1, 42,69],
    71:['Short Whistle','high',71,'',-1,37, 56],
    72:['Long Whistle','high',72,'',-1,37, 56],
    73:['Short Guiro','high',73,'',-1, 42,42],
    74:['Long Guiro','high',74,'',-1,46,46],
    75:['Claves','high',75,'',-1, 37,75,75],
    76:['Hi Wood Block','high',76,'',8, 50,63],
    77:['Low Wood Block','mid',77,'',7,45, 64],
    78:['Mute Cuica','',78,'',-1, 50,62],
    79:['Open Cuica','',79,'',-1, 45,63],
    80:['Mute Triangle','',80,'',-1, 37,75],
    81:['Open Triangle','',81,'',-1, 37,75],
    }

def get_band(roll, band="low"):
    """Returns a monophonic onset pattern of instruments in the given frequency band.

    roll, np.array
        Piano roll

    band, str
        "low", "mid", or "hi"
    """
    range_map = {
        "low": low_instruments,
        "mid": mid_instruments,
        "hi": hi_instruments,
    }

    if band not in range_map:
        raise ValueError(f"Invalid band `{band}`. Must be low, mid, or hi")

    return (roll[:, range_map[band]].sum(axis=1) > 0).astype(int)


def get_bands(roll):
    """Parses the low, mid, and high frequency bands of a piano roll"""
    return (
        get_band(roll, band="low"),
        get_band(roll, band="mid"),
        get_band(roll, band="hi"),
    )


def event_to_8number(midi_notes):
    # input an event list and output a representation
    # in 8 instrumental band:
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
    # in 3 instrumental band:
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
