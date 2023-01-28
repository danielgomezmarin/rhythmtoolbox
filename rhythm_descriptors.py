# this script contains descriptors meant to be extracted
# form symbolic polyphonic drum patterns
#
# the descriptors are coded as separated functions
# that can be run independently
#
# most of them are reported in different papers
# related to polyphonic drum analysis and generation
# * [1] "Similarity and Style in Electronic Dance Music Drum Rhythms"section 3.4
# * [2] "Strictly Rhythm: Exploring the Effects of Identical Regions and Meter Induction in Rhythmic Similarity Perception"
# * [3] "PAD and SAD: Two Awareness-Weighted Rhythmic Similarity Distances"
# * [4] "Drum rhythm spaces: From polyphonic similarity to generative maps"
# * [5] "Real-Time Drum Accompaniment Using Transformer Architecture"
# * [6] "Computational Creation and Morphing of Multilevel Rhythms by Control of Evenness"
# * [7] "The perceptual relevance of balance, evenness, and entropy in musical rhythms"
# * [8] "Syncopation, Body-Movement and Pleasure in Groove Music"

import math

import numpy as np

###########################
# MIDI instrument mapping #
###########################
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
    # key is midi note number
    # values are:
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


##########################
# monophonic descriptors #
##########################


def density(patt):
    # count the onsets in a pattern
    return sum([x for x in patt if x == 1])


def syncopation16(patt):
    # input a monophonic pattern as a list of 0s and 1s (1s indicating an onset)
    # and obtain its syncopation value
    synclist = [0] * 16
    salience_lhl = [5, 1, 2, 1, 3, 1, 2, 1, 4, 1, 2, 1, 3, 1, 2, 1]
    for s, step in enumerate(patt):
        # look for an onset preceding a silence
        if patt[s] == 1 and patt[(s + 1) % len(patt)] == 0:
            # compute syncopation
            synclist[s] = salience_lhl[(s + 1) % len(patt)] - salience_lhl[s]

    return sum(synclist)


def syncopation16_awareness(patt):
    # input a monophonic pattern as a list of 0s and 1s (1s indicating an onset)
    # and obtain its awareness-weighted syncopation value
    # awareness is reported in [2]
    synclist = [0] * 16
    salience = [5, 1, 2, 1, 3, 1, 2, 1, 4, 1, 2, 1, 3, 1, 2, 1]
    awareness = [5, 1, 4, 2]
    for s, step in enumerate(patt):
        # look for an onset and a silence following
        if patt[s] == 1 and patt[(s + 1) % 16] == 0:
            # compute syncopation
            synclist[s] = salience[(s + 1) % 16] - salience[s]

    # apply awareness
    sync_and_awareness = [
        sum(synclist[0:4]) * awareness[0],
        sum(synclist[4:8]) * awareness[1],
        sum(synclist[8:12]) * awareness[2],
        sum(synclist[12:16]) * awareness[3],
    ]

    return sum(sync_and_awareness)


def evenness(patt):
    # how well distributed are the D onsets of a pattern
    # if they are compared to a perfect D sided polygon
    # input patterns are phase-corrected to start always at step 0
    # i.e. if we have 4 onsets in a 16 step pattern, what is the distance of onsets
    # o1, o2, o3, o4 to positions 0 4 8 and 12
    # here we will use a simple algorithm that does not involve DFT computation
    # evenness is well described in [6] but this implementation is much simpler
    d = density(patt)
    if d == 0:
        return 0

    iso_angle_16 = 2 * math.pi / 16
    first_onset_step = [i for i, x in enumerate(patt) if x == 1][0]
    first_onset_angle = first_onset_step * iso_angle_16
    iso_angle = 2 * math.pi / d
    iso_patt_radians = [x * iso_angle for x in range(d)]
    patt_radians = [i * iso_angle_16 for i, x in enumerate(patt) if x == 1]
    cosines = [
        abs(math.cos(x - patt_radians[i] + first_onset_angle))
        for i, x in enumerate(iso_patt_radians)
    ]
    return sum(cosines) / d


def balance(patt):
    # balance is described in [7] as:
    # "a quantification of the proximity of that rhythm's
    # “centre of mass” (the mean position of the points)
    # to the centre of the unit circle."
    d = density(patt)
    if d == 0:
        return 1

    center = np.array([0, 0])
    iso_angle_16 = 2 * math.pi / 16
    X = [math.cos(i * iso_angle_16) for i, x in enumerate(patt) if x == 1]
    Y = [math.sin(i * iso_angle_16) for i, x in enumerate(patt) if x == 1]
    matrix = np.array([X, Y])
    matrix_sum = matrix.sum(axis=1)
    magnitude = np.linalg.norm(matrix_sum - center) / d
    return 1 - magnitude


#########################
# polyphonic descriptors
#########################


def pattlist_to_pianoroll(pattlist):
    roll = np.zeros((len(pattlist), 128))
    for i in range(len(roll)):
        roll[i][pattlist[i]] = 1
    return roll


def get_stream(pattlist, range="low"):
    # monophonic onset pattern of instruments in the given frequency range: low, mid, or hi
    stream = []

    range_map = {
        "low": low_instruments,
        "mid": mid_instruments,
        "hi": hi_instruments,
    }

    if range not in range_map:
        raise ValueError(f"Invalid range `{range}`. Must be low, mid, or hi")

    roll = pattlist_to_pianoroll(pattlist)
    for event in roll:
        stream.append(1 if event[range_map[range]].sum() > 0 else 0)

    return stream


def noi(pattlist):
    # number of different instruments in a pattern
    return len(set([i for s in pattlist for i in s]))


def lowD(pattlist):
    # density in the low frequency range
    return sum(get_stream(pattlist, range="low"))


def midD(pattlist):
    # density in the mid frequency range
    return sum(get_stream(pattlist, range="mid"))


def hiD(pattlist):
    # density in the hi frequency range
    return sum(get_stream(pattlist, range="hi"))


def stepD(pattlist):
    # percentage of steps that have onsets
    return sum([1 for x in pattlist if x]) / len(pattlist)


def lowness(pattlist):
    # number of onsets in the low freq stream divided by the number of steps that have onsets
    n = sum([1 for x in pattlist if x])
    return lowD(pattlist) / n if n else 0


def midness(pattlist):
    # number of onsets in the mid freq stream divided by the number of steps that have onsets
    n = sum([1 for x in pattlist if x])
    return midD(pattlist) / n if n else 0


def hiness(pattlist):
    # number of onsets in the hi freq stream divided by the number of steps that have onsets
    n = sum([1 for x in pattlist if x])
    return hiD(pattlist) / n if n else 0


def lowsync(pattlist):
    # syncopation value of the low-frequency stream
    return syncopation16(get_stream(pattlist, range="low"))


def midsync(pattlist):
    # syncopation value of the mid-frequency stream
    return syncopation16(get_stream(pattlist, range="mid"))


def hisync(pattlist):
    # syncopation value of the high-frequency stream
    return syncopation16(get_stream(pattlist, range="hi"))


def lowsyness(pattlist):
    # stream syncopation divided by the number of onsets of the stream
    d = lowD(pattlist)
    return lowsync(pattlist) / d if d else 0


def midsyness(pattlist):
    # stream syncopation divided by the number of onsets of the stream
    d = midD(pattlist)
    return midsync(pattlist) / d if d else 0


def hisyness(pattlist):
    # stream syncopation divided by the number of onsets of the stream
    d = hiD(pattlist)
    return hisync(pattlist) / d if d else 0


def polysync(pattlist):
    # polyphonic syncopation as described in [8]
    # If N is a note that precedes a rest, R,
    # and R has a metric weight greater than or equal to N,
    # then the pair (N, R) is said to constitute a monophonic syncopation.
    # If N is a note on a certain instrument that precedes a note
    # on a different instrument (Ndi), and Ndi has a metric weight
    # greater than or equal to N, then the pair (N, Ndi) is said to
    # constitute a polyphonic syncopation.

    # metric profile as described by witek
    salience_w = [0, -3, -2, -3, -1, -3, -2, -3, -1, -3, -2, -3, -1, -3, -2, -3]
    syncopation_list = []

    # find pairs of N and Ndi notes events in the polyphonic pattlist
    for i in range(len(pattlist)):

        lowstream_ = get_stream(pattlist, range="low")
        midstream_ = get_stream(pattlist, range="mid")
        histream_ = get_stream(pattlist, range="hi")

        # describe the instruments present in current and nex steps
        event = [lowstream_[i], midstream_[i], histream_[i]]
        event_next = [
            lowstream_[(i + 1) % len(pattlist)],
            midstream_[(i + 1) % len(pattlist)],
            histream_[(i + 1) % len(pattlist)],
        ]
        local_syncopation = 0

        # syncopation: events are different, and next one has greater or equal metric weight
        if event != event_next and salience_w[(i + 1) % len(pattlist)] >= salience_w[i]:
            # only process if there is a syncopation
            # now analyze what type of syncopation is found to assign instrumental weight
            # instrumental weight depends on the relationship between the instruments in the pair:

            ##### three-stream syncopations:
            # low (event[0]) against mid and hi (event_next[1] and event_next[2] respectively)
            if event[0] == 1 and event_next[1] == 1 and event_next[2] == 1:
                instrumental_weight = 2
                local_syncopation = (
                    abs(salience_w[i] - salience_w[(i + 1) % len(pattlist)])
                    + instrumental_weight
                )

            # mid syncopated against low and high
            # mid (event[1]) against low and hi (event_next[0] and event_next[2] respectively)
            if event[1] == 1 and event_next[0] == 1 and event_next[2] == 1:
                instrumental_weight = 1
                local_syncopation = (
                    abs(salience_w[i] - salience_w[(i + 1) % len(pattlist)])
                    + instrumental_weight
                )

            ##### two stream syncopations:
            # low or mid vs high
            if (event[0] == 1 or event[1] == 1) and event_next == [0, 0, 1]:
                instrumental_weight = 5
                local_syncopation = (
                    abs(salience_w[i] - salience_w[(i + 1) % len(pattlist)])
                    + instrumental_weight
                )

            # low vs mid (ATTENTION: not on Witek's paper)
            if event == [1, 0, 0] and event_next == [0, 1, 0]:
                instrumental_weight = 2
                local_syncopation = (
                    abs(salience_w[i] - salience_w[(i + 1) % len(pattlist)])
                    + instrumental_weight
                )

            # mid vs low (ATTENTION: not on Witek's paper)
            if event == [0, 1, 0] and event_next == [1, 0, 0]:
                instrumental_weight = 2
                local_syncopation = (
                    abs(salience_w[i] - salience_w[(i + 1) % len(pattlist)])
                    + instrumental_weight
                )

            syncopation_list.append(local_syncopation)

    return sum(syncopation_list)


def polyevenness(pattlist):
    # compute the polyphonic evenness of a pattlist
    # adapted from [7]
    lowstream_ = get_stream(pattlist, range="low")
    midstream_ = get_stream(pattlist, range="mid")
    histream_ = get_stream(pattlist, range="hi")

    low_evenness = evenness(lowstream_)
    mid_evenness = evenness(midstream_)
    hi_evenness = evenness(histream_)

    polyevenness = low_evenness * 3 + mid_evenness * 2 + hi_evenness

    return polyevenness


def polybalance(pattlist):
    # compute the polyphonic balance of a pattlist
    # adapted from [7]
    lowstream_ = get_stream(pattlist, range="low")
    midstream_ = get_stream(pattlist, range="mid")
    histream_ = get_stream(pattlist, range="hi")

    d = density(lowstream_) * 3 + density(midstream_) * 2 + density(histream_)
    if d == 0:
        return 1

    center = np.array([0, 0])
    iso_angle_16 = 2 * math.pi / 16

    Xlow = [3 * math.cos(i * iso_angle_16) for i, x in enumerate(lowstream_) if x == 1]
    Ylow = [3 * math.sin(i * iso_angle_16) for i, x in enumerate(lowstream_) if x == 1]
    matrixlow = np.array([Xlow, Ylow])
    matrixlowsum = matrixlow.sum(axis=1)

    Xmid = [2 * math.cos(i * iso_angle_16) for i, x in enumerate(midstream_) if x == 1]
    Ymid = [2 * math.sin(i * iso_angle_16) for i, x in enumerate(midstream_) if x == 1]
    matrixmid = np.array([Xmid, Ymid])
    matrixmidsum = matrixmid.sum(axis=1)

    Xhi = [2 * math.cos(i * iso_angle_16) for i, x in enumerate(histream_) if x == 1]
    Yhi = [2 * math.sin(i * iso_angle_16) for i, x in enumerate(histream_) if x == 1]
    matrixhi = np.array([Xhi, Yhi])
    matrixhisum = matrixhi.sum(axis=1)

    matrixsum = matrixlowsum + matrixmidsum + matrixhisum

    magnitude = np.linalg.norm(matrixsum - center) / d

    return 1 - magnitude


def polyD(pattlist):
    # compute the total number of onsets
    return lowD(pattlist) + midD(pattlist) + hiD(pattlist)


def pattlist2descriptors(pattlist):
    """Compute all descriptors from a pattern list representation of a polyphonic drum pattern.

    A pattern list is a list of lists representing time steps, each containing the MIDI note numbers that occur at that
    step, e.g. [[36, 42], [], [37], []]. Velocity is not included.

    Some descriptors are valid only for 16-step patterns and will be None if the pattern is not divisible by 16.
    """

    descriptors = {
        "noi": noi,
        "lowD": lowD,
        "midD": midD,
        "hiD": hiD,
        "stepD": stepD,
        "lowness": lowness,
        "midness": midness,
        "hiness": hiness,
        "polyD": polyD,
    }

    sixteen_step_descriptors = {
        "lowsync": lowsync,
        "midsync": midsync,
        "hisync": hisync,
        "lowsyness": lowsyness,
        "midsyness": midsyness,
        "hisyness": hisyness,
        "polysync": polysync,
        "polyevenness": polyevenness,
        "polybalance": polybalance,
    }

    result = {}
    for key, func in descriptors.items():
        result[key] = func(pattlist)

    for key, func in sixteen_step_descriptors.items():
        result[key] = None
        if len(pattlist) % 16 == 0:
            # Compute the descriptors for each 16-step subpattern
            vals = []
            for i in range(len(pattlist) - 16 + 1):
                vals.append(func(pattlist[i : i + 16]))
            result[key] = np.mean(vals)

    return result
