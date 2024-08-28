# napari-mock

[![License MIT](https://img.shields.io/pypi/l/napari-mock.svg?color=green)](https://github.com/githubuser/napari-mock/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-mock.svg?color=green)](https://pypi.org/project/napari-mock)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-mock.svg?color=green)](https://python.org)
[![tests](https://github.com/githubuser/napari-mock/workflows/tests/badge.svg)](https://github.com/githubuser/napari-mock/actions)
[![codecov](https://codecov.io/gh/githubuser/napari-mock/branch/main/graph/badge.svg)](https://codecov.io/gh/githubuser/napari-mock)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/napari-mock)](https://napari-hub.org/plugins/napari-mock)

mock

----------------------------------

This [napari] plugin was generated with [Cookiecutter] using [@napari]'s [cookiecutter-napari-plugin] template.

<!--
Don't miss the full getting started guide to set up your new package:
https://github.com/napari/cookiecutter-napari-plugin#getting-started

and review the napari docs for plugin developers:
https://napari.org/stable/plugins/index.html
-->

## Installation

You can install `napari-mock` via [pip]:

    pip install napari-mock

## Pre-reqs for Developers
 
### For GUI Designing:

Install Qt Designer from [here]{https://build-system.fman.io/qt-designer-download} 

### Create the conda environment using the requirments file

We will use Python 3.10 as the python version

```Shell
conda create -n napari-env python=3.10
```

Activate the conda environment

```Shell
conda activate napari-env
```

Install the required packages using pip

```Shell
pip install -r requirements.txt
```

Open napari by typing the command
```Shell
napari
```

The plugin will be found in the **Plugins** menu as "Mock Widget"


## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [MIT] license,
"napari-mock" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

[napari]: https://github.com/napari/napari
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[cookiecutter-napari-plugin]: https://github.com/napari/cookiecutter-napari-plugin

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
