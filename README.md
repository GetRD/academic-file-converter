# Admin Tool for Academic

[![Download from PyPI](https://img.shields.io/pypi/v/academic.svg)](https://pypi.python.org/pypi/academic)
[![License](https://img.shields.io/pypi/l/academic.svg)](https://pypi.python.org/pypi/academic)

An admin tool for [Academic](https://sourcethemes.com/academic/).

Features

* Import publications from BibTeX
* Import third-party assets to generate an entirely offline site

## Installation

    pip3 install -U academic

## Prerequisites

Install the [Academic](https://sourcethemes.com/academic/) website framework.

## Usage

Please ensure that your website is checked into Git prior to running this tool so that you can review the changes proposed by this tool in Git and accept or reject them without risking breaking your site. If not using Git, it's strongly recommended to make a full backup of your site prior to running this tool.

Start the admin tool within your Academic website folder by running the `academic` command in your Terminal/Command Prompt app.

Import featured (selected) publications:

    academic import --bibtex my_featured_publications.bib --featured

Import publications:

    academic import --bibtex my_publications.bib

Import third-party JS and CSS assets for building an offline website (requires Academic v3+):

    academic import --assets

## Contribute

For local development, clone this repository and install the tool using the following command:

    pip3 install -e .

## License

Copyright 2018-present [George Cushen](https://twitter.com/GeorgeCushen).

Licensed under the MIT License.
