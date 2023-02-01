import numpy as np

from .descriptors import (
    bandness,
    density,
    get_n_onset_steps,
    noi,
    polybalance,
    polyD,
    polyevenness,
    polysync,
    stepD,
    syncopation16,
    syness,
)
from .midi_mapping import hi_instruments, low_instruments, mid_instruments


def get_stream(roll, band="low"):
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

    return ((roll[:, range_map[band]]).sum(axis=1) > 0).astype(int)


def get_streams(roll):
    return (
        get_stream(roll, band="low"),
        get_stream(roll, band="mid"),
        get_stream(roll, band="hi"),
    )


def pattlist_to_pianoroll(pattlist):
    roll = np.zeros((len(pattlist), 128))
    for i in range(len(roll)):
        roll[i][pattlist[i]] = 1
    return roll


def pianoroll2descriptors(roll):
    """Compute all descriptors from a piano roll representation of a polyphonic drum pattern.

    Some descriptors are valid only for 16-step patterns and will be None if the pattern is not divisible by 16.
    """
    descriptor_names = [
        "noi",
        "lowD",
        "midD",
        "hiD",
        "stepD",
        "lowness",
        "midness",
        "hiness",
        "lowsync",
        "midsync",
        "hisync",
        "lowsyness",
        "midsyness",
        "hisyness",
        "polybalance",
        "polyevenness",
        "polysync",
        "polyD",
    ]

    # Initialize the return dict
    result = {d: None for d in descriptor_names}

    # No need to compute descriptors for empty patterns
    n_onset_steps = get_n_onset_steps(roll)
    if n_onset_steps == 0:
        return result

    # Get the onset pattern of each instrument band
    lowstream, midstream, histream = get_streams(roll)

    result["noi"] = noi(roll)
    result["lowD"] = density(lowstream)
    result["midD"] = density(midstream)
    result["hiD"] = density(histream)
    result["stepD"] = stepD(roll)
    result["lowness"] = bandness(lowstream, n_onset_steps)
    result["midness"] = bandness(midstream, n_onset_steps)
    result["hiness"] = bandness(histream, n_onset_steps)

    # Compute descriptors that are valid only for 16-step patterns
    if len(roll) == 16:
        result["lowsync"] = syncopation16(lowstream)
        result["midsync"] = syncopation16(midstream)
        result["hisync"] = syncopation16(histream)
        result["lowsyness"] = syness(lowstream)
        result["midsyness"] = syness(midstream)
        result["hisyness"] = syness(histream)
        result["polybalance"] = polybalance(lowstream, midstream, histream)
        result["polyevenness"] = polyevenness(lowstream, midstream, histream)
        result["polysync"] = polysync(lowstream, midstream, histream)
        result["polyD"] = polyD(lowstream, midstream, histream)

    return result


def pattlist2descriptors(pattlist):
    """Compute all descriptors from a pattern list representation of a polyphonic drum pattern.

    A pattern list is a list of lists representing time steps, each containing the MIDI note numbers that occur at that
    step, e.g. [[36, 42], [], [37], []]. Velocity is not included.

    Some descriptors are valid only for 16-step patterns and will be None if the pattern is not divisible by 16.
    """
    roll = pattlist_to_pianoroll(pattlist)
    return pianoroll2descriptors(roll)
