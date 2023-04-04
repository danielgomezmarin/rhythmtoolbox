# Rhythm Toolbox

This repository contains tools for studying rhythms in symbolic format. It was developed for the study of polyphonic
drum patterns, but can be adapted for other types of patterns. It implements various descriptors derived from scientific
literature; see [Descriptors](#descriptors) for a full list with references.

## Installation

```
pip install git+https://github.com/danielgomezmarin/rhythmtoolbox
```

## Usage

Rhythm Toolbox supports multiple representations of symbolic rhythm. Across all representations, Rhythm Toolbox operates
at a 16th note resolution, or 4 ticks per beat in MIDI terms. If data is passed in at a different resolution, it is
resampled by associating each onset with its closest 16th note position.

#### MIDI

To compute descriptors from a MIDI file:

```python
from rhythmtoolbox import midifile2descriptors

midifile2descriptors('midi/boska/3.mid')
```

#### Piano roll

A [piano roll](https://en.wikipedia.org/wiki/Piano_roll#In_digital_audio_workstations) is a `(N, V)` matrix, where `N`
is a number of time steps and `V` is a number of MIDI pitches. Any positive value represents an onset; Rhythm Toolbox
does not currently consider velocity.

To compute descriptors from a piano roll:

```python
from rhythmtoolbox import pianoroll2descriptors

pianoroll2descriptors(roll)
```

#### Pattern list

A pattern list is a list of lists representing time steps, each containing the MIDI note numbers that occur at that
step.

To compute descriptors from a pattern list:

```python
from rhythmtoolbox import pattlist2descriptors

pattlist = [
    [36, 38, 42],
    [],
    [],
    [38, 42],
    [46],
    [46],
    [36, 38, 42],
    [],
    [42],
    [38],
    [36, 42],
    [],
    [38, 46],
    [46],
    [42, 64],
    [],
]
pattlist2descriptors(pattlist)
```

## Descriptors

The following descriptors are discussed in [Gómez-Marín et al, 2020](https://doi.org/10.1080/09298215.2020.1806887).
Additional sources are listed where applicable. The mapping of MIDI instruments to frequency bands can be found
in [midi_mapping.py](./rhythmtoolbox/midi_mapping.py).

| Name        | Description                              |
|-------------|------------------------------------------|
| noi         | Number of instruments                    |
| polyDensity | Number of onsets                         |
| lowDensity  | Number of onsets in the low freq band    |
| midDensity  | Number of onsets in the mid freq band    |
| hiDensity   | Number of onsets in the high freq band   |
| lowness     | Fraction of onsets in the low freq band  |
| midness     | Fraction of onsets in the mid freq band  |
| hiness      | Fraction of onsets in the high freq band |
| stepDensity | Fraction of steps with onsets            |

The following descriptors are valid only for 16-step patterns:

| Name         | Description                                 | Reference                                                                |
|--------------|---------------------------------------------|--------------------------------------------------------------------------|
| sync         | Syncopation                                 |                                                                          |
| lowSync      | Syncopation of the low freq band            |                                                                          |
| midSync      | Syncopation of the mid freq band            |                                                                          |
| hiSync       | Syncopation of the high freq band           |                                                                          |
| syness       | Syncopation / density                       |                                                                          |
| lowSyness    | Syncopation / density of the low freq band  |                                                                          |
| midSyness    | Syncopation / density of the mid freq band  |                                                                          |
| hiSyness     | Syncopation / density of the high freq band |                                                                          |
| balance      | Monophonic balance                          | [Milne and Herff, 2020](https://doi.org/10.1016/j.cognition.2020.104233) |
| polyBalance  | Polyphonic balance                          |                                                                          |
| evenness     | Monophonic evenness                         | [Milne and Dean, 2016](https://doi.org/10.1162/COMJ_a_00343)             |
| polyEvenness | Polyphonic evenness                         |                                                                          |
| polySync     | Polyphonic syncopation                      | [Witek et al, 2014](https://doi.org/10.<br/>1371/journal.pone.0094446)   |

## Attribution

If this repository is useful for your research please cite the
following [paper](https://doi.org/10.1080/09298215.2020.1806887)
via the BibTeX below.

    @article{gomez2020drum,
      title={Drum rhythm spaces: From polyphonic similarity to generative maps},
      author={G{\'o}mez-Mar{\'\i}n, Daniel and Jord{\`a}, Sergi and Herrera, Perfecto},
      journal={Journal of New Music Research},
      volume={49},
      number={5},
      pages={438--456},
      year={2020},
      publisher={Taylor \& Francis}
    }

To cite the initial version of this repository (Nov 2018), checkout
commit [`6acdb69a60153d08`](https://github.com/danielgomezmarin/rhythmtoolbox/tree/6acdb69a60153d0874da87560df3d7c62765e27a).

The MIDI drum patterns examples included in [midi/boska](./midi/boska) and [midi/sano](./midi/sano) were provided by
Jon-Eirik Boska and Sebastián Hoyos, respectively.
