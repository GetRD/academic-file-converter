# Admin Tool for Academic

[![Download from PyPI](https://img.shields.io/pypi/v/academic.svg)](https://pypi.python.org/pypi/academic)
[![License](https://img.shields.io/pypi/l/academic.svg)](https://pypi.python.org/pypi/academic)

An admin tool for [Academic](https://sourcethemes.com/academic/).

Features

* Import publications from BibTeX
* Import third-party assets to generate an entirely offline site

## Prerequisites

1. Install the [Academic](https://sourcethemes.com/academic/) website framework
2. Install [Python 3](https://realpython.com/installing-python/) if it’s not already installed
3. [Version control](https://guides.github.com/introduction/git-handbook/#version-control) your website with [Git](http://rogerdudler.github.io/git-guide/) so that you can review the proposed changes and accept or reject them without risking breaking your site. Otherwise, if not using Git, backup your site prior to running this tool.

## Installation

Open your Terminal or Command Prompt app and install Academic’s admin tool:

    pip3 install -U academic

## Usage

Use the `cd` command to navigate to your website folder in the terminal:

    cd <MY_WEBSITE_FOLDER>

**Help:**

    academic

**Import publications:**

    academic import --bibtex my_publications.bib

Optional arguments:

* `--help` Help
* `--featured` Flag publications as *featured* (to appear in *Selected Publications* widget)
* `--overwrite` Overwrite existing publications
* `--publication-dir PUBLICATION_DIR` Your publications directory (defaults to `publication`)

After importing publications, [a full text PDF and image can be associated with each item and further details added via extra parameters](https://sourcethemes.com/academic/docs/managing-content/#manually).

**Import third-party JS and CSS assets for building an offline website:**

    academic import --assets

*Importing assets requires Academic v3+.*

**Run a Hugo command (pass-through):**

    academic server

## Contribute

For local development, clone this repository and install the tool using the following command:

    pip3 install -e .

## License

Copyright 2018-present [George Cushen](https://georgecushen.com).

Licensed under the [MIT License](https://github.com/sourcethemes/academic-admin/blob/master/LICENSE.md).
