import numpy as np

from .descriptors import (
    hiD,
    hiness,
    hisync,
    hisyness,
    lowD,
    lowness,
    lowsync,
    lowsyness,
    midD,
    midness,
    midsync,
    midsyness,
    noi,
    polybalance,
    polyD,
    polyevenness,
    polysync,
    stepD,
)


def pattlist_to_pianoroll(pattlist):
    roll = np.zeros((len(pattlist), 128))
    for i in range(len(roll)):
        roll[i][pattlist[i]] = 1
    return roll


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

    roll = pattlist_to_pianoroll(pattlist)

    result = {}
    for key, func in descriptors.items():
        result[key] = func(roll)

    for key, func in sixteen_step_descriptors.items():
        result[key] = None
        if len(roll) % 16 == 0:
            # Compute the descriptors for each 16-step subpattern
            vals = []
            for i in range(len(roll) - 16 + 1):
                vals.append(func(roll[i : i + 16]))
            result[key] = np.mean(vals)

    return result
