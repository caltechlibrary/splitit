Split It!<img width="14%" align="right" src=".graphics/splitit-icon.svg">
=========

This is a simple program to reformat certain spreadsheets of results downloaded by Caltech Library staff from caltech.tind.io when they are doing inventory.

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat-square)](https://choosealicense.com/licenses/bsd-3-clause)
[![Latest release](https://img.shields.io/badge/Latest_release-1.0.0-b44e88.svg?style=flat-square)](http://shields.io)


Table of contents
-----------------

* [Introduction](#introduction)
* [Installation](#installation)
* [Usage](#usage)
* [Known issues and limitations](#known-issues-and-limitations)
* [Getting help](#getting-help)
* [Contributing](#contributing)
* [License](#license)
* [Authors and history](#authors-and-history)
* [Acknowledgments](#authors-and-acknowledgments)


Introduction
------------

The librarians at Caltech Library periodically have to perform library inventory.  In the process of doing that, they download spreadsheets of data from caltech.tind.io that have a format illustrated by the following example fragment:

```
574524,35047011136967,on shelf,,QA7 .A664 1991,
501345,350470002009169; 35047010046266,on shelf; on shelf,,QA7 .A67 1983,
381367,350470000767183; 350470000767192; 35047010794485,on shelf; on shelf; Limited circulation,,QA7 .S44,
```

The 2nd and 3rd lines above show examples where there are multiple results in a row, separated by semicolon (`;`) characters.  In these rows, columns 2 and 3 are parallel mappings of values, meaning that the barcode numbers in column 2 should be matched to the corresponding values in the semicolon-separated list of the 3rd column.  The other column values apply to each of the individual values in the compound.

_Split It!_ is a simple program that takes such as spreadsheet, splits the compound rows into separate rows, and produces a new spreadsheet with the collected results.  For the fragment above, it would look like this:

```
574524,35047011136967,on shelf,,QA7 .A664 1991,
501345,350470002009169,on shelf,,QA7 .A67 1983,
501345,35047010046266,on shelf,,QA7 .A67 1983,
381367,350470000767183,on shelf,,QA7 .S44,
381367,350470000767192,on shelf,,QA7 .S44,
381367,35047010794485,Limited circulation,,QA7 .S44,
```

Installation
------------

Binary installers for Windows can be downloaded from [the project's releases page on GitHub](https://github.com/caltechlibrary/splitit/releases).  Alternatively, you can use Python `pip` to install this from the repository using the following command:
```sh
sudo python3 -m pip install git+https://github.com/caltechlibrary/splitit.git --upgrade
```

As a final alternative, you can instead clone this GitHub repository and then run `setup.py` manually.  First, create a directory somewhere on your computer where you want to store the files, and cd to it from a terminal shell.  Next, execute the following commands:
```sh
git clone https://github.com/caltechlibrary/splitit.git
cd splitit
sudo python3 -m pip install . --upgrade
```


Usage
-----

_Split It!_ is a command line program.  It can be used from a terminal shell.  On all systems, the installation _should_ place a new program on your shell's search path called `splitit` (or `splitit.exe` on Windows), so that you can start _Split It!_ with a simple terminal command:
```csh
splitit
```

_Split It!_ accepts various command-line arguments.  To get information about the available options, use the `-h` argument (or `/h` on Windows):
```csh
splitit -h
```

In normal operation, _Split It!_ requires two arguments: an `-i` option (`/i` on Windows) to indicate the input CSV file, and an `-o` option (`/o` on Windows) to indicate the file where it should write the output in CSV format.  Here's an example to illustrate this:
```csh
splitit -i input.csv -o output.csv
```


Known issues and limitations
----------------------------

_Split It!_ currently assumes that the input spreadsheet has a format consisting of 5 columns, with the 2nd and 3rd columns being the ones that contain semicolon-separated values.  It does not verify that the input spreadsheet has this format; it simply proceeds on that assumption.  If the input spreadsheet does not conform to this format, the results are unpredictable.


Getting help
------------

If you find an issue, please submit it in [the GitHub issue tracker](https://github.com/caltechlibrary/splitit/issues) for this repository.


Contributing
------------

We would be happy to receive your help and participation with enhancing Split It!  Please visit the [guidelines for contributing](CONTRIBUTING.md) for some tips on getting started.


License
-------

Software produced by the Caltech Library is Copyright (C) 2019, Caltech.  This software is freely distributed under a BSD/MIT type license.  Please see the [LICENSE](LICENSE) file for more information.


Authors and history
---------------------------

[Mike Hucka](https://github.com/mhucka) designed and implemented Split It! based on requests from [Laurel Narizny](https://github.com/lnarizny) in mid-2019.


Acknowledgments
---------------

This work was funded by the California Institute of Technology Library.

The [vector artwork](https://thenounproject.com/term/page-break/31219/) of a "page break" icon used as a starting point for the logo for this repository was created by [Garrett Knoll](https://thenounproject.com/g_a.k_/) for the [Noun Project](https://thenounproject.com).  It is licensed under the Creative Commons [Attribution 3.0 Unported](https://creativecommons.org/licenses/by/3.0/deed.en) license.  The vector graphics was modified by Mike Hucka to change the color. 

_Split It!_ makes use of numerous open-source packages, without which it would have been effectively impossible to develop _Split It!_.  I want to acknowledge this debt.  In alphabetical order, the packages are:

* [colorama](https://github.com/tartley/colorama) &ndash; makes ANSI escape character sequences work under MS Windows terminals
* [ipdb](https://github.com/gotcha/ipdb) &ndash; the IPython debugger
* [plac](http://micheles.github.io/plac/) &ndash; a command line argument parser
* [setuptools](https://github.com/pypa/setuptools) &ndash; library for `setup.py`
* [termcolor](https://pypi.org/project/termcolor/) &ndash; ANSI color formatting for output in terminal
* [PyInstaller](http://www.pyinstaller.org) &ndash; a packaging program that creates standalone applications from Python programs for Windows, macOS, Linux and other platforms


<div align="center">
  <br>
  <a href="https://www.caltech.edu">
    <img width="100" height="100" src=".graphics/caltech-round.svg">
  </a>
</div>
