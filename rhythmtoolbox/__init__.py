import numpy as np
from scipy import ndimage

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


def compute_16_descriptors(lowband, midband, hiband):
    """Compute descriptors that are valid only for 16-step patterns"""
    descriptors = {}

    if not all(len(x) == 16 for x in [lowband, midband, hiband]):
        return descriptors

    descriptors["lowsync"] = syncopation16(lowband)
    descriptors["midsync"] = syncopation16(midband)
    descriptors["hisync"] = syncopation16(hiband)
    descriptors["lowsyness"] = syness(lowband)
    descriptors["midsyness"] = syness(midband)
    descriptors["hisyness"] = syness(hiband)
    descriptors["polybalance"] = polybalance(lowband, midband, hiband)
    descriptors["polyevenness"] = polyevenness(lowband, midband, hiband)
    descriptors["polysync"] = polysync(lowband, midband, hiband)

    return descriptors


def resample_pianoroll(roll, from_resolution, to_resolution):
    """Associate each onset in the roll with its closest 16th note position"""

    if from_resolution == to_resolution:
        return roll

    # Piano roll must be a 2D array
    assert len(roll.shape) == 2

    factor = to_resolution / from_resolution

    return ndimage.zoom(roll, (factor, 1), order=0)


def pianoroll2descriptors(roll, resolution=4):
    """Compute all descriptors from a piano roll representation of a polyphonic drum pattern.

    Notes
        - A piano roll with a resolution other than 4 ticks per beat will be resampled, which can be lossy.
        - Some descriptors are valid only for 16-step patterns and will be None if the pattern is not divisible by 16.

    Parameters
        roll, np.ndarray
        The piano roll

        resolution, int
        The resolution of the piano roll in MIDI ticks per beat

    Returns
         Descriptors in a dict of {descriptor_name: descriptor_value}
    """

    # Piano roll must be a 2D array
    assert len(roll.shape) == 2

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

    # Resample to a 16-note resolution
    resampled = resample_pianoroll(roll, resolution, 4)

    # Get the onset pattern of each frequency band
    lowband, midband, hiband = get_bands(resampled)

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
    if len(resampled) == 16:
        sixteen_descs = compute_16_descriptors(lowband, midband, hiband)
        result.update(sixteen_descs)

    return result


def pattlist2descriptors(pattlist, resolution=4):
    """Compute all descriptors from a pattern list representation of a polyphonic drum pattern.

    A pattern list is a list of lists representing time steps, each containing the MIDI note numbers that occur at that
    step, e.g. [[36, 42], [], [37], []]. Velocity is not included.

    Some descriptors are valid only for 16-step patterns and will be None if the pattern length is not divisible by 16.
    """
    roll = pattlist_to_pianoroll(pattlist)
    return pianoroll2descriptors(roll, resolution)


def midifile2descriptors(midi_filepath):
    """Compute all descriptors from a MIDI file."""
    import pypianoroll

    multitrack = pypianoroll.read(midi_filepath, resolution=4)
    return pianoroll2descriptors(multitrack[0].pianoroll)
