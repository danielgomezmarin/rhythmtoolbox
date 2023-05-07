from collections import defaultdict

import numpy as np
import pretty_midi as pm
from scipy import ndimage

from rhythmtoolbox.descriptors import (
    balance,
    bandness,
    density,
    evenness,
    get_n_onset_steps,
    noi,
    poly_balance,
    poly_density,
    poly_evenness,
    poly_sync,
    step_density,
    syncopation16,
    syness,
)
from rhythmtoolbox.midi_mapping import get_bands

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
    """Convert a pattern list to a piano roll"""
    roll = np.zeros((len(pattlist), 128))
    for i in range(len(roll)):
        roll[i, pattlist[i]] = 1
    return roll


def resample_pianoroll(roll, from_resolution, to_resolution):
    """Associate each onset in the roll with its closest 16th note position"""

    if from_resolution == to_resolution:
        return roll

    assert len(roll.shape) == 2, "Piano roll must be a 2D array"

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

    assert len(roll.shape) == 2, "Piano roll must be a 2D array"

    # Initialize the output dictionary
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

        if len(resampled) % 16 == 0:
            sub_descs = defaultdict(list)
            for subroll in np.split(resampled, len(resampled) / 16):
                subpattern = (subroll.sum(axis=1) > 0).astype(int)
                sub_descs["balance"] = balance(subpattern)
                sub_descs["evenness"] = evenness(subpattern)
                sub_descs["sync"] = syncopation16(subpattern)
                sub_descs["syness"] = syness(subpattern)

            for desc in sub_descs:
                result[desc] = np.mean(sub_descs[desc])

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
    # For patterns w lengths greater than and divisible by 16, compute descriptors for each 16-step subpattern and return the mean
    if len(resampled) % 16 == 0:
        sub_descs = defaultdict(list)
        for subroll in np.split(resampled, len(resampled) / 16):
            sub_low, sub_mid, sub_hi = get_bands(subroll)
            subpattern = (subroll.sum(axis=1) > 0).astype(int)

            sub_descs["sync"].append(syncopation16(subpattern))
            sub_descs["lowSync"].append(syncopation16(sub_low))
            sub_descs["midSync"].append(syncopation16(sub_mid))
            sub_descs["hiSync"].append(syncopation16(sub_hi))
            sub_descs["syness"].append(syness(subpattern))
            sub_descs["lowSyness"].append(syness(sub_low))
            sub_descs["midSyness"].append(syness(sub_mid))
            sub_descs["hiSyness"].append(syness(sub_hi))
            sub_descs["balance"].append(balance(subpattern))
            sub_descs["polyBalance"].append(poly_balance(sub_low, sub_mid, sub_hi))
            sub_descs["evenness"].append(evenness(subpattern))
            sub_descs["polyEvenness"].append(poly_evenness(sub_low, sub_mid, sub_hi))
            sub_descs["polySync"].append(poly_sync(sub_low, sub_mid, sub_hi))

        for desc in sub_descs:
            result[desc] = np.mean(sub_descs[desc])

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


def get_subdivisions(pmid, resolution):
    """Parse beats from a PrettyMIDI object and create an array of subdivisions at a given resolution.

    :param pmid: PrettyMIDI object
    :param resolution: Resolution of the output array
    :return: Array of subdivisions
    """
    beats = pmid.get_beats()

    # Assume a single 4-beat bar
    if len(beats) <= 1:
        beats = np.arange(0, 4)

    beat_sep = beats[-1] - beats[-2]
    additional_beat = beats[-1] + beat_sep
    additional_beats = np.array(additional_beat)
    if additional_beat % 1 != 0:
        additional_beats = np.append(additional_beats, additional_beat + beat_sep)
    beats = np.append(beats, additional_beats)

    # Upsample beat times to the input resolution using linear interpolation
    subdivisions = []
    for start, end in zip(beats, beats[1:]):
        for j in range(resolution):
            subdivisions.append((end - start) / resolution * j + start)
    subdivisions.append(beats[-1])

    return np.array(subdivisions)


def get_onset_roll_from_pmid(pmid, resolution=4):
    """Converts a PrettyMIDI object to a piano roll at the given resolution, preserving only onsets.

    - If input MIDI is multi-track, we consider only the first track
    - The input MIDI is quantized to the given resolution

    :param pmid: PrettyMIDI object
    :param resolution: Resolution of the piano roll in MIDI ticks per beat
    :return: Onset roll of shape (N, V), where N is the number of time steps and V is the number of MIDI pitches
    """
    if not pmid.instruments:
        return np.zeros((0, 128), np.uint8)

    # Consider only the first instrument
    instrument = pmid.instruments[0]
    if len(instrument.notes) == 0:
        return np.zeros((0, 128), np.uint8)

    subdivisions = get_subdivisions(pmid, resolution=resolution)

    n_ticks = len(subdivisions) - 1

    onsets_unquantized = [note.start for note in instrument.notes]
    onsets = [np.argmin(np.abs(t - subdivisions)) for t in onsets_unquantized]

    # If an onset is quantized to the last tick, move it to the previous tick
    for ix, onset in enumerate(onsets):
        if onset == n_ticks:
            onsets[onsets.index(onset)] = onset - 1

    pitches = [note.pitch for note in instrument.notes]
    velocities = [note.velocity for note in instrument.notes]

    onset_roll = np.zeros((n_ticks, 128), np.uint8)
    onset_roll[onsets, pitches] = velocities

    return onset_roll


def midifile2descriptors(filepath, drums=True):
    """Compute all descriptors from a MIDI file.

    Parameters
        filepath, str
        Path to a MIDI file

        drums, bool
        Indicates whether the pattern is a drum pattern

    Returns
         Descriptors in a dict of {descriptor_name: descriptor_value}
    """
    pmid = pm.PrettyMIDI(filepath, resolution=4)
    onset_roll = get_onset_roll_from_pmid(pmid)
    return pianoroll2descriptors(onset_roll, drums=drums)
