[**中文**](./README.zh.md)

# [Academic File Converter](https://github.com/GetRD/academic-file-converter)

[![Download from PyPI](https://img.shields.io/pypi/v/academic.svg?style=for-the-badge)](https://pypi.python.org/pypi/academic)
[![Discord](https://img.shields.io/discord/722225264733716590?style=for-the-badge)](https://discord.com/channels/722225264733716590/742892432458252370/742895548159492138)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/gcushen?label=%E2%9D%A4%EF%B8%8F%20sponsor&style=for-the-badge)](https://github.com/sponsors/gcushen)
[![Twitter Follow](https://img.shields.io/twitter/follow/georgecushen?label=Follow%20on%20Twitter&style=for-the-badge)](https://twitter.com/GeorgeCushen)
[![GitHub followers](https://img.shields.io/github/followers/gcushen?label=Follow%20on%20GH&style=for-the-badge)](https://github.com/gcushen)  


### 📚 Easily import publications and Jupyter notebooks to your Markdown-formatted website or book

![](.github/media/demo.gif)

**Features**

* **Import Jupyter notebooks** as blog posts or book chapters
* **Import publications** (such as **books, conference proceedings, and journals**) from your reference manager to your Markdown-formatted website or book
  * Simply export a BibTeX file from your reference manager, such as [Zotero](https://www.zotero.org), and provide this as the input to the converter tool
* **Compatible with all static website generators** such as Next, Astro, Gatsby, Hugo, etc.
* **Easy to use** - 100% Python, no dependency on complex software such as Pandoc
* **Automate** file conversions using a [GitHub Action](https://github.com/HugoBlox/hugo-blox-builder/blob/main/starters/blog/.github/workflows/import-notebooks.yml)

**Community**

- 📚 [View the **documentation** below](#installation)
- 💬 [Chat live with the **community** on Discord](https://discord.gg/z8wNYzb)
- 🐦 Twitter: [@GetResearchDev](https://twitter.com/GetResearchDev) [@GeorgeCushen](https://twitter.com/GeorgeCushen) [#MadeWithAcademic](https://twitter.com/search?q=%23MadeWithAcademic&src=typed_query)

## ❤️ Support Open Research & Open Source

We are on a mission to foster **open research** by developing **open source** tools like this.

To help us develop this open source software sustainably under the MIT license, we ask all individuals and businesses that use it to help support its ongoing maintenance and development via sponsorship and contributing.

Support the open research movement:

  - ⭐️ [**Star** this project on GitHub](https://github.com/GetRD/academic-file-converter)
  - ❤️ [Become a **GitHub Sponsor** and **unlock perks**](https://github.com/sponsors/gcushen)
  - ☕️ [**Donate a coffee**](https://github.com/sponsors/gcushen?frequency=one-time)
  - 👩‍💻 [**Contribute**](#contribute)

## Installation

Open your **Terminal** or **Command Prompt** app and enter one of the installation commands below.

### With Pipx

For the **easiest** installation, install with [Pipx](https://pypa.github.io/pipx/): 

    pipx install academic

Pipx will **automatically install the required Python version for you** in a dedicated environment.

### With Pip

 To install using the Python's Pip tool, ensure you have [Python 3.11+](https://realpython.com/installing-python/) installed and then run:

    pip3 install -U academic

## Usage

Open your Command Line or Terminal app and use the `cd` command to navigate to the folder containing the files you wish to convert, for example:

    cd ~/Documents/my_website

### Import publications

Download references from your reference manager, such as Zotero, in the Bibtex format.

Say we downloaded our publications to a file named `my_publications.bib` within the website folder, let's import them into the `content/publication/` folder:

    academic import my_publications.bib content/publication/ --compact

Optional arguments:

* `--compact` Generate minimal markdown without comments or empty keys
* `--overwrite` Overwrite any existing publications in the output folder
* `--normalize` Normalize tags by converting them to lowercase and capitalizing the first letter (e.g. "sciEnCE" -> "Science")
* `--featured` Flag these publications as *featured* (to appear in your website's *Featured Publications* section)
* `--verbose` or `-v` Show verbose messages
* `--help` Help

### Import full text and cover image

After importing publications, we suggest you:
- Edit the Markdown body of each publication to add the full text directly to the page (if the publication is open access), or otherwise, to add supplementary notes for each publication
- Add an image named `featured` to each publication's folder to visually represent your publication on the page and for sharing on social media
- Add the publication PDF to each publication folder (for open access publications), to enable your website visitors to download your publication
  
[Learn more in the Hugo Blox Docs](https://docs.hugoblox.com/reference/content-types/).

### Import blog posts from Jupyter Notebooks

Say we have our notebooks in a `notebooks` folder within the website folder, let's import them into the `content/post/` folder:

    academic import 'notebooks/*.ipynb' content/post/ --verbose

Optional arguments:

* `--overwrite` Overwrite any existing blog posts in the output folder
* `--verbose` or `-v` Show verbose messages
* `--help` Help

## Contribute

Interested in contributing to **open source** and **open research**?

Learn [how to contribute code on Github](https://codeburst.io/a-step-by-step-guide-to-making-your-first-github-contribution-5302260a2940).

Check out the [open issues](https://github.com/GetRD/academic-file-converter/issues) and contribute a [Pull Request](https://github.com/GetRD/academic-file-converter/pulls). 

For local development, clone this repository and use Poetry to install and run the converter using the following commands:

    git clone https://github.com/GetRD/academic-file-converter.git
    cd academic-file-converter
    poetry install
    poetry run academic import tests/data/article.bib output/publication/ --overwrite --compact
    poetry run academic import 'tests/data/**/*.ipynb' output/post/ --overwrite --verbose

When preparing a contribution, run the following checks and ensure that they all pass:

- Lint: `make lint`
- Format: `make format`
- Test: `make test`
- Type check: `make type`

### Help beta test the dev version

You can help test the latest development version by installing the latest `main` branch from GitHub:

    pip3 install -U git+https://github.com/GetRD/academic-file-converter.git

## License

Copyright 2018-present [George Cushen](https://georgecushen.com).

Licensed under the [MIT License](https://github.com/GetRD/academic-file-converter/blob/main/LICENSE.md).

![PyPI - Downloads](https://img.shields.io/pypi/dm/academic?label=PyPi%20Downloads&style=for-the-badge)
[![License](https://img.shields.io/pypi/l/academic.svg?style=for-the-badge)](https://github.com/GetRD/academic-file-converter/blob/main/LICENSE.md)
