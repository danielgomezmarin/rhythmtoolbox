"""
This module implements a variety of descriptors for polyphonic drum patterns from scientific research related to
drum analysis and generation.

References
- [1] "Similarity and Style in Electronic Dance Music Drum Rhythms"section 3.4
- [2] "Strictly Rhythm: Exploring the Effects of Identical Regions and Meter Induction in Rhythmic Similarity Perception"
- [3] "PAD and SAD: Two Awareness-Weighted Rhythmic Similarity Distances"
- [4] "Drum rhythm spaces: From polyphonic similarity to generative maps"
- [5] "Real-Time Drum Accompaniment Using Transformer Architecture"
- [6] "Computational Creation and Morphing of Multilevel Rhythms by Control of Evenness"
- [7] "The perceptual relevance of balance, evenness, and entropy in musical rhythms"
- [8] "Syncopation, Body-Movement and Pleasure in Groove Music"
"""

import math

import numpy as np

from .midi_mapping import hi_instruments, low_instruments, mid_instruments

# Monophonic descriptors


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


# Polyphonic descriptors


def get_stream(roll, band="low"):
    # monophonic onset pattern of instruments in the given frequency band: low, mid, or hi
    stream = []

    range_map = {
        "low": low_instruments,
        "mid": mid_instruments,
        "hi": hi_instruments,
    }

    if band not in range_map:
        raise ValueError(f"Invalid range `{band}`. Must be low, mid, or hi")

    for event in roll:
        stream.append(1 if event[range_map[band]].sum() > 0 else 0)

    return stream


def noi(roll):
    # number of different instruments in a pattern
    return len(list(filter(lambda x: x.sum() > 0, roll.T)))


def lowD(roll):
    # density in the low frequency range
    return sum(get_stream(roll, band="low"))


def midD(roll):
    # density in the mid frequency range
    return sum(get_stream(roll, band="mid"))


def hiD(roll):
    # density in the hi frequency range
    return sum(get_stream(roll, band="hi"))


def stepD(roll):
    # percentage of steps that have onsets
    return sum([1 for x in roll if x.sum() > 0]) / len(roll)


def lowness(roll):
    # number of onsets in the low freq stream divided by the number of steps that have onsets
    n = sum([1 for x in roll if x.sum() > 0])
    return lowD(roll) / n if n else 0


def midness(roll):
    # number of onsets in the mid freq stream divided by the number of steps that have onsets
    n = sum([1 for x in roll if x.sum() > 0])
    return midD(roll) / n if n else 0


def hiness(roll):
    # number of onsets in the hi freq stream divided by the number of steps that have onsets
    n = sum([1 for x in roll if x.sum() > 0])
    return hiD(roll) / n if n else 0


def lowsync(roll):
    # syncopation value of the low-frequency stream
    return syncopation16(get_stream(roll, band="low"))


def midsync(roll):
    # syncopation value of the mid-frequency stream
    return syncopation16(get_stream(roll, band="mid"))


def hisync(roll):
    # syncopation value of the high-frequency stream
    return syncopation16(get_stream(roll, band="hi"))


def lowsyness(roll):
    # stream syncopation divided by the number of onsets of the stream
    d = lowD(roll)
    return lowsync(roll) / d if d else 0


def midsyness(roll):
    # stream syncopation divided by the number of onsets of the stream
    d = midD(roll)
    return midsync(roll) / d if d else 0


def hisyness(roll):
    # stream syncopation divided by the number of onsets of the stream
    d = hiD(roll)
    return hisync(roll) / d if d else 0


def polysync(roll):
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

    # number of time steps
    n = len(roll)

    # find pairs of N and Ndi notes events
    for i in range(n):
        lowstream_ = get_stream(roll, band="low")
        midstream_ = get_stream(roll, band="mid")
        histream_ = get_stream(roll, band="hi")

        # describe the instruments present in current and nex steps
        event = [lowstream_[i], midstream_[i], histream_[i]]
        event_next = [
            lowstream_[(i + 1) % n],
            midstream_[(i + 1) % n],
            histream_[(i + 1) % n],
        ]
        local_syncopation = 0

        # syncopation: events are different, and next one has greater or equal metric weight
        if event != event_next and salience_w[(i + 1) % n] >= salience_w[i]:
            # only process if there is a syncopation
            # now analyze what type of syncopation is found to assign instrumental weight
            # instrumental weight depends on the relationship between the instruments in the pair:

            # Three-stream syncopation
            # Low against mid and hi
            if event[0] == 1 and event_next[1] == 1 and event_next[2] == 1:
                instrumental_weight = 2
                local_syncopation = (
                    abs(salience_w[i] - salience_w[(i + 1) % n]) + instrumental_weight
                )

            # Mid against low and high mid against low and hi
            if event[1] == 1 and event_next[0] == 1 and event_next[2] == 1:
                instrumental_weight = 1
                local_syncopation = (
                    abs(salience_w[i] - salience_w[(i + 1) % n]) + instrumental_weight
                )

            # Two-stream syncopation
            # Low or mid against high
            if (event[0] == 1 or event[1] == 1) and event_next == [0, 0, 1]:
                instrumental_weight = 5
                local_syncopation = (
                    abs(salience_w[i] - salience_w[(i + 1) % n]) + instrumental_weight
                )

            # Low against mid (ATTENTION: not defined in [8])
            if event == [1, 0, 0] and event_next == [0, 1, 0]:
                instrumental_weight = 2
                local_syncopation = (
                    abs(salience_w[i] - salience_w[(i + 1) % n]) + instrumental_weight
                )

            # Mid against low (ATTENTION: not defined in [8])
            if event == [0, 1, 0] and event_next == [1, 0, 0]:
                instrumental_weight = 2
                local_syncopation = (
                    abs(salience_w[i] - salience_w[(i + 1) % n]) + instrumental_weight
                )

            syncopation_list.append(local_syncopation)

    return sum(syncopation_list)


def polyevenness(roll):
    # compute the polyphonic evenness
    # adapted from [7]
    lowstream_ = get_stream(roll, band="low")
    midstream_ = get_stream(roll, band="mid")
    histream_ = get_stream(roll, band="hi")

    low_evenness = evenness(lowstream_)
    mid_evenness = evenness(midstream_)
    hi_evenness = evenness(histream_)

    polyevenness = low_evenness * 3 + mid_evenness * 2 + hi_evenness

    return polyevenness


def polybalance(roll):
    # compute the polyphonic balance
    # adapted from [7]
    lowstream_ = get_stream(roll, band="low")
    midstream_ = get_stream(roll, band="mid")
    histream_ = get_stream(roll, band="hi")

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


def polyD(roll):
    # compute the total number of onsets
    return lowD(roll) + midD(roll) + hiD(roll)
