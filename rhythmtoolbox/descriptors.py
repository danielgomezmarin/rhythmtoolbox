"""
This module implements various descriptors derived from scientific publications related to polyphonic drum pattern
analysis and generation.

References

- Gómez Marín, D. (2018). Similarity and style in electronic dance music drum rhythms (Doctoral dissertation,
  Universitat Pompeu Fabra).

- Gómez-Marín, D., Jorda, S., & Herrera, P. (2016). Strictly Rhythm: Exploring the effects of identical regions and
  meter induction in rhythmic similarity perception. In Music, Mind, and Embodiment: 11th International Symposium, CMMR
  2015, Plymouth, UK, June 16-19, 2015, Revised Selected Papers 11 (pp. 449-463). Springer International Publishing.

- Gómez Marín, D., Jordà Puig, S., & Boyer, H. (2015). Pad and Sad: Two awareness-Weighted rhythmic similarity
  distances. In Müller M, Wiering F, editors. Proceedings of the 16th International Society for Music Information
  Retrieval (ISMIR) Conference; 2015 Oct 26-30; Málaga, Spain. Canada: International Society for Music Information
  Retrieval; 2015.. International Society for Music Information Retrieval (ISMIR).

- Gómez-Marín, D., Jordà, S., & Herrera, P. (2020). Drum rhythm spaces: From polyphonic similarity to generative maps.
  Journal of New Music Research, 49(5), 438-456.

- Haki, B., Nieto, M., Pelinski, T., & Jordà, S. Real-Time Drum Accompaniment Using Transformer Architecture.

- Milne, A. J., & Dean, R. T. (2016). Computational creation and morphing of multilevel rhythms by control of evenness
  Computer Music Journal, 40(1), 35-53.

- Milne, A. J., & Herff, S. A. (2020). The perceptual relevance of balance, evenness, and entropy in musical rhythms.
  Cognition, 203, 104233.

- Witek, M. A., Clarke, E. F., Wallentin, M., Kringelbach, M. L., & Vuust, P. (2014). Syncopation, body-movement and
  pleasure in groove music. PloS one, 9(4), e94446.
"""

import math

import numpy as np


# Monophonic descriptors


def syncopation16(pattern):
    """Compute the syncopation value of a 16-step pattern

    pattern, list
        a monophonic pattern as a list of 0s and 1s (1s indicating an onset)
    """

    if isinstance(pattern, np.ndarray):
        pattern = pattern.tolist()

    synclist = [0] * 16
    salience_lhl = [5, 1, 2, 1, 3, 1, 2, 1, 4, 1, 2, 1, 3, 1, 2, 1]

    n_steps = len(pattern)
    for ix in range(n_steps):
        next_ix = (ix + 1) % n_steps
        # look for an onset preceding a silence
        if pattern[ix] == 1 and pattern[next_ix] == 0:
            # compute syncopation
            synclist[ix] = salience_lhl[next_ix] - salience_lhl[ix]

    return sum(synclist)


def syncopation16_awareness(pattern):
    # input a monophonic pattern as a list of 0s and 1s (1s indicating an onset)
    # and obtain its awareness-weighted syncopation value
    # awareness is reported in [2]
    synclist = [0] * 16
    salience = [5, 1, 2, 1, 3, 1, 2, 1, 4, 1, 2, 1, 3, 1, 2, 1]
    awareness = [5, 1, 4, 2]
    n_steps = len(pattern)
    for ix in range(n_steps):
        next_ix = (ix + 1) % n_steps
        # look for an onset and a silence following
        if pattern[ix] == 1 and pattern[next_ix] == 0:
            # compute syncopation
            synclist[ix] = salience[next_ix] - salience[ix]

    # apply awareness
    sync_and_awareness = [
        sum(synclist[0:4]) * awareness[0],
        sum(synclist[4:8]) * awareness[1],
        sum(synclist[8:12]) * awareness[2],
        sum(synclist[12:16]) * awareness[3],
    ]

    return sum(sync_and_awareness)


def evenness(pattern):
    # how well distributed are the D onsets of a pattern
    # if they are compared to a perfect D sided polygon
    # input patterns are phase-corrected to start always at step 0
    # i.e. if we have 4 onsets in a 16 step pattern, what is the distance of onsets
    # o1, o2, o3, o4 to positions 0 4 8 and 12
    # here we will use a simple algorithm that does not involve DFT computation
    # evenness is well described in [Milne and Dean, 2016] but this implementation is much simpler
    d = density(pattern)
    if d == 0:
        return 0

    iso_angle_16 = 2 * math.pi / 16
    first_onset_step = [i for i, x in enumerate(pattern) if x == 1][0]
    first_onset_angle = first_onset_step * iso_angle_16
    iso_angle = 2 * math.pi / d
    iso_pattern_radians = [x * iso_angle for x in range(d)]
    pattern_radians = [i * iso_angle_16 for i, x in enumerate(pattern) if x == 1]
    cosines = [
        abs(math.cos(x - pattern_radians[i] + first_onset_angle))
        for i, x in enumerate(iso_pattern_radians)
    ]
    return sum(cosines) / d


def balance(pattern):
    # balance is described in [Milne and Herff, 2020] as:
    # "a quantification of the proximity of that rhythm's
    # “centre of mass” (the mean position of the points)
    # to the centre of the unit circle."
    d = density(pattern)
    if d == 0:
        return 1

    center = np.array([0, 0])
    iso_angle_16 = 2 * math.pi / 16
    X = [math.cos(i * iso_angle_16) for i, x in enumerate(pattern) if x == 1]
    Y = [math.sin(i * iso_angle_16) for i, x in enumerate(pattern) if x == 1]
    matrix = np.array([X, Y])
    matrix_sum = matrix.sum(axis=1)
    magnitude = np.linalg.norm(matrix_sum - center) / d
    return 1 - magnitude


# Polyphonic descriptors


def noi(roll):
    """Returns the number of instruments (noi) used in the roll"""
    return (roll.sum(axis=0) > 0).sum()


def density(pattern):
    """Computes the density of the pattern."""
    return sum(pattern)


def get_n_onset_steps(roll):
    """Returns the number of steps with onsets"""
    return (roll.sum(axis=1) > 0).sum()


def step_density(roll):
    """Returns the percentage of steps with onsets"""
    return get_n_onset_steps(roll) / len(roll)


def bandness(pattern, n_onset_steps):
    """Computes a measure of how concentrated the pattern is in the given frequency band.

    pattern, list
        The pattern of the band of interest.

    n_onset_steps, int
        The number of steps with onsets of the entire roll.
    """
    return density(pattern) / n_onset_steps if n_onset_steps else 0


def syness(pattern):
    """Returns the syncopation of the pattern divided by the number of onsets in the pattern"""
    d = density(pattern)
    return syncopation16(pattern) / d if d else 0


def poly_sync(low_stream, mid_stream, hi_stream):
    """Computes the polyphonic syncopation of a rhythm, as described in [Witek et al., 2014].

    If N is a note that precedes a rest R, and R has a metric weight greater than or equal to N, then the pair (N, R)
    is said to constitute a monophonic syncopation. If N is a note on a certain instrument that precedes a note on a
    different instrument (Ndi), and Ndi has a metric weight greater than or equal to N, then the pair (N, Ndi) is said
    to constitute a polyphonic syncopation.
    """

    # Metric profile as described by Witek et al. (2014)
    salience_w = [0, -3, -2, -3, -1, -3, -2, -3, -1, -3, -2, -3, -1, -3, -2, -3]
    syncopation_list = []

    # number of time steps
    n = len(low_stream)

    # find pairs of N and Ndi notes events
    for ix in range(n):
        # describe the instruments present in current and next steps
        event = [low_stream[ix], mid_stream[ix], hi_stream[ix]]

        next_ix = (ix + 1) % n
        event_next = [
            low_stream[next_ix],
            mid_stream[next_ix],
            hi_stream[next_ix],
        ]

        # syncopation occurs when adjacent events are different, and succeeding event has greater or equal metric weight
        if event != event_next and salience_w[next_ix] >= salience_w[ix]:
            # only process if there is a syncopation
            # analyze what type of syncopation is found to assign instrumental weight
            # instrumental weight depends on the relationship between the instruments in the pair

            instrumental_weight = None

            # Three-stream syncopation
            # Low against mid and hi
            if event[0] == 1 and event_next[1] == 1 and event_next[2] == 1:
                instrumental_weight = 2

            # Mid against low and high
            if event[1] == 1 and event_next[0] == 1 and event_next[2] == 1:
                instrumental_weight = 1

            # Two-stream syncopation
            # Low or mid against high
            if (event[0] == 1 or event[1] == 1) and event_next == [0, 0, 1]:
                instrumental_weight = 5

            # Low against mid (NOTE: not defined in [Witek et al., 2014])
            if event == [1, 0, 0] and event_next == [0, 1, 0]:
                instrumental_weight = 2

            # Mid against low (NOTE: not defined in [Witek et al., 2014])
            if event == [0, 1, 0] and event_next == [1, 0, 0]:
                instrumental_weight = 2

            local_syncopation = 0
            if instrumental_weight:
                local_syncopation = (
                    abs(salience_w[ix] - salience_w[next_ix]) + instrumental_weight
                )
            syncopation_list.append(local_syncopation)

    return sum(syncopation_list)


def poly_evenness(low_stream, mid_stream, hi_stream):
    """Compute the polyphonic evenness. Adapted from [Milne and Herff, 2020]"""
    low_evenness = evenness(low_stream)
    mid_evenness = evenness(mid_stream)
    hi_evenness = evenness(hi_stream)

    return low_evenness * 3 + mid_evenness * 2 + hi_evenness


def poly_balance(low_stream, mid_stream, hi_stream):
    """Compute the polyphonic balance of a rhythm. Adapted from [Milne and Herff, 2020]"""

    d = density(low_stream) * 3 + density(mid_stream) * 2 + density(hi_stream)
    if d == 0:
        return 1

    center = np.array([0, 0])
    iso_angle_16 = 2 * math.pi / 16

    Xlow = [3 * math.cos(i * iso_angle_16) for i, x in enumerate(low_stream) if x == 1]
    Ylow = [3 * math.sin(i * iso_angle_16) for i, x in enumerate(low_stream) if x == 1]
    matrixlow = np.array([Xlow, Ylow])
    matrixlowsum = matrixlow.sum(axis=1)

    Xmid = [2 * math.cos(i * iso_angle_16) for i, x in enumerate(mid_stream) if x == 1]
    Ymid = [2 * math.sin(i * iso_angle_16) for i, x in enumerate(mid_stream) if x == 1]
    matrixmid = np.array([Xmid, Ymid])
    matrixmidsum = matrixmid.sum(axis=1)

    Xhi = [2 * math.cos(i * iso_angle_16) for i, x in enumerate(hi_stream) if x == 1]
    Yhi = [2 * math.sin(i * iso_angle_16) for i, x in enumerate(hi_stream) if x == 1]
    matrixhi = np.array([Xhi, Yhi])
    matrixhisum = matrixhi.sum(axis=1)

    matrixsum = matrixlowsum + matrixmidsum + matrixhisum

    magnitude = np.linalg.norm(matrixsum - center) / d

    return 1 - magnitude


def poly_density(low_stream, mid_stream, hi_stream):
    # compute the total number of onsets
    return density(low_stream) + density(mid_stream) + density(hi_stream)
