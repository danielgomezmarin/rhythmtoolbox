import numpy as np
from scipy import ndimage

from .descriptors import (
    bandness,
    density,
    get_n_onset_steps,
    noi,
    balance,
    evenness,
    poly_balance,
    poly_density,
    poly_evenness,
    poly_sync,
    step_density,
    syncopation16,
    syness,
)
from .midi_mapping import get_bands


DESCRIPTOR_NAMES = [
    "noi",
    "polyDensity",
    "lowDensity",
    "midDensity",
    "hiDensity",
    "lowness",
    "midness",
    "hiness",
    "stepDensity",
    "sync",
    "lowSync",
    "midSync",
    "hiSync",
    "syness",
    "lowSyness",
    "midSyness",
    "hiSyness",
    "balance",
    "polyBalance",
    "evenness",
    "polyEvenness",
    "polySync",
]


def pattlist_to_pianoroll(pattlist):
    """Convert from a pattern list representation to a piano roll representation"""
    roll = np.zeros((len(pattlist), 128))
    for i in range(len(roll)):
        roll[i][pattlist[i]] = 1
    return roll


def resample_pianoroll(roll, from_resolution, to_resolution):
    """Associate each onset in the roll with its closest 16th note position"""

    if from_resolution == to_resolution:
        return roll

    # Piano roll must be a 2D array
    assert len(roll.shape) == 2

    factor = to_resolution / from_resolution

    return ndimage.zoom(roll, (factor, 1), order=0)


def pianoroll2descriptors(roll, resolution=4, drums=True):
    """Compute all descriptors from a piano roll representation of a polyphonic drum pattern.

    Notes
        - A piano roll with a resolution other than 4 ticks per beat will be resampled, which can be lossy.
        - Some descriptors are valid only for 16-step patterns and will be None if the pattern is not divisible by 16.

    Parameters
        roll, np.ndarray
        The piano roll

        resolution, int
        The resolution of the piano roll in MIDI ticks per beat

        drums, bool
        Indicates whether the pattern is a drum pattern

    Returns
         Descriptors in a dict of {descriptor_name: descriptor_value}
    """

    # Piano roll must be a 2D array
    assert len(roll.shape) == 2

    # Initialize the return dict
    result = {d: None for d in DESCRIPTOR_NAMES}

    # Resample to a 16-note resolution
    resampled = resample_pianoroll(roll, resolution, 4)

    # No need to compute descriptors for empty patterns
    n_onset_steps = get_n_onset_steps(resampled)
    if n_onset_steps == 0:
        return result

    pattern = (resampled.sum(axis=1) > 0).astype(int)

    if not drums:
        result["noi"] = noi(resampled)
        result["stepDensity"] = step_density(resampled)
        result["polyDensity"] = density(pattern)

        if len(resampled) == 16:
            result["balance"] = balance(pattern)
            result["evenness"] = evenness(pattern)
            result["sync"] = syncopation16(resampled)
            result["syness"] = syness(pattern)

        for desc in DESCRIPTOR_NAMES:
            if desc not in result:
                result[desc] = None

        return result

    # Get the onset pattern of each frequency band
    low_band, mid_band, hi_band = get_bands(resampled)

    # Compute descriptors that are valid for any pattern length
    result["noi"] = noi(resampled)
    result["lowDensity"] = density(low_band)
    result["midDensity"] = density(mid_band)
    result["hiDensity"] = density(hi_band)
    result["polyDensity"] = poly_density(low_band, mid_band, hi_band)
    result["stepDensity"] = step_density(resampled)
    result["lowness"] = bandness(low_band, n_onset_steps)
    result["midness"] = bandness(mid_band, n_onset_steps)
    result["hiness"] = bandness(hi_band, n_onset_steps)

    # Compute descriptors that are valid only for 16-step patterns
    if len(resampled) == 16:
        result["sync"] = syncopation16(pattern)
        result["lowSync"] = syncopation16(low_band)
        result["midSync"] = syncopation16(mid_band)
        result["hiSync"] = syncopation16(hi_band)
        result["syness"] = syness(pattern)
        result["lowSyness"] = syness(low_band)
        result["midSyness"] = syness(mid_band)
        result["hiSyness"] = syness(hi_band)
        result["balance"] = balance(pattern)
        result["polyBalance"] = poly_balance(low_band, mid_band, hi_band)
        result["evenness"] = evenness(pattern)
        result["polyEvenness"] = poly_evenness(low_band, mid_band, hi_band)
        result["polySync"] = poly_sync(low_band, mid_band, hi_band)

    return result


def pattlist2descriptors(pattlist, resolution=4, drums=True):
    """Compute all descriptors from a pattern list representation of a polyphonic drum pattern.

    A pattern list is a list of lists representing time steps, each containing the MIDI note numbers that occur at that
    step, e.g. [[36, 42], [], [37], []]. Velocity is not included.

    Parameters
        pattlist, list
        The pattern list

        resolution, int
        The resolution of the piano roll in MIDI ticks per beat

        drums, bool
        Indicates whether the pattern is a drum pattern

    Returns
         Descriptors in a dict of {descriptor_name: descriptor_value}
    """
    roll = pattlist_to_pianoroll(pattlist)
    return pianoroll2descriptors(roll, resolution, drums=drums)


def midifile2descriptors(midi_filepath, drums=True):
    """Compute all descriptors from a MIDI file.

    Parameters
        midi_filepath, str
        Path to a MIDI file

        drums, bool
        Indicates whether the pattern is a drum pattern

    Returns
         Descriptors in a dict of {descriptor_name: descriptor_value}
    """
    import pypianoroll

    multitrack = pypianoroll.read(midi_filepath, resolution=4)
    return pianoroll2descriptors(multitrack[0].pianoroll, drums=drums)
