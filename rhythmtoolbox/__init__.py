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
from .midi_mapping import get_bands


def pattlist_to_pianoroll(pattlist):
    """Convert from a pattern list representation to a piano roll representation"""
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
    lowband, midband, hiband = get_bands(roll)

    result["noi"] = noi(roll)
    result["lowD"] = density(lowband)
    result["midD"] = density(midband)
    result["hiD"] = density(hiband)
    result["polyD"] = polyD(lowband, midband, hiband)
    result["stepD"] = stepD(roll)
    result["lowness"] = bandness(lowband, n_onset_steps)
    result["midness"] = bandness(midband, n_onset_steps)
    result["hiness"] = bandness(hiband, n_onset_steps)

    # Compute descriptors that are valid only for 16-step patterns
    if len(roll) == 16:
        result["lowsync"] = syncopation16(lowband)
        result["midsync"] = syncopation16(midband)
        result["hisync"] = syncopation16(hiband)
        result["lowsyness"] = syness(lowband)
        result["midsyness"] = syness(midband)
        result["hisyness"] = syness(hiband)
        result["polybalance"] = polybalance(lowband, midband, hiband)
        result["polyevenness"] = polyevenness(lowband, midband, hiband)
        result["polysync"] = polysync(lowband, midband, hiband)

    return result


def pattlist2descriptors(pattlist):
    """Compute all descriptors from a pattern list representation of a polyphonic drum pattern.

    A pattern list is a list of lists representing time steps, each containing the MIDI note numbers that occur at that
    step, e.g. [[36, 42], [], [37], []]. Velocity is not included.

    Some descriptors are valid only for 16-step patterns and will be None if the pattern length is not divisible by 16.
    """
    roll = pattlist_to_pianoroll(pattlist)
    return pianoroll2descriptors(roll)


def midifile2descriptors(midi_filepath):
    """Compute all descriptors from a MIDI file."""
    import pypianoroll

    multitrack = pypianoroll.read(midi_filepath, resolution=4)
    return pianoroll2descriptors(multitrack[0].pianoroll)
