# Rhythm Toolbox

This repository contains tools for studying rhythms in symbolic format, implements various descriptors for both
monophonic and polyphonic patterns. It is tailored to the analysis of polyphonic drum patterns but can be adapted for
other types of patterns. The descriptors are derived from scientific papers which are cited in the source.

To go to the initial version of the repo (Nov 2018), checkout commit `6acdb69a60153d08`.

## Usage

Install this package from source using `pip install git+https://github.com/danielgomezmarin/rhythmtoolbox`.

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

## Attribution

If this repository is useful for your research please cite [our paper](https://doi.org/10.1080/09298215.2020.1806887)
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
