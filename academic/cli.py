#!/usr/bin/env python3

import subprocess
import sys
import os
import re
import argparse
from argparse import RawTextHelpFormatter
from pathlib import Path
import toml
from requests import get
from urllib.parse import urlparse
import tempfile
import calendar
from datetime import datetime
from academic import __version__ as version

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.customization import convert_to_unicode

JS_FILENAME = 'static/js/vendor/main.min.js'
CSS_FILENAME = 'static/css/vendor/main.min.css'

# Map BibTeX to Academic publication types.
PUB_TYPES = {
    'article': 2,
    'book': 5,
    'inbook': 6,
    'incollection': 6,
    'inproceedings': 1,
    'manual': 4,
    'mastersthesis': 7,
    'misc': 0,
    'phdthesis': 7,
    'proceedings': 0,
    'techreport': 4,
    'unpublished': 3,
    'patent': 8
}


def main():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description=f'Academic Admin Tool v{version}\nhttps://sourcethemes.com/academic/',
        formatter_class=RawTextHelpFormatter)
    subparsers = parser.add_subparsers(help='Sub-commands', dest="command")

    # Sub-parser for import command.
    parser_a = subparsers.add_parser('import', help='Import data into Academic')
    parser_a.add_argument("--assets", action='store_true',
                          help='Import third-party JS and CSS for generating an offline site')
    parser_a.add_argument("--bibtex", required=False, type=str, help='File path to your BibTeX file')
    parser_a.add_argument("--publication-dir", required=False, type=str, default='publication',
                          help='Directory that your publications are stored in (default `publication`)')
    parser_a.add_argument("--featured", action='store_true', help='Flag publications as featured')
    parser_a.add_argument("--overwrite", action='store_true', help='Overwrite existing publications')
    parser_a.add_argument("--normalize", action='store_true', help='Normalize each keyword to lowercase with uppercase first letter')

    args, unknown = parser.parse_known_args()

    # If no arguments, show help.
    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()

    # If no known arguments, wrap Hugo command.
    elif args is None and unknown:
        cmd = []
        cmd.append('hugo')
        if sys.argv[1:]:
            cmd.append(sys.argv[1:])
        subprocess.call(cmd)
    elif args.command and args.assets:
        import_assets()
    elif args.command and args.bibtex:
        import_bibtex(args.bibtex, pub_dir=args.publication_dir, featured=args.featured, overwrite=args.overwrite, normalize=args.normalize)


def import_bibtex(bibtex, pub_dir='publication', featured=False, overwrite=False, normalize=False):
    """Import publications from BibTeX file"""

    # Check BibTeX file exists.
    if not Path(bibtex).is_file():
        print('Please check the path to your BibTeX file and re-run.')
        return

    # Load BibTeX file for parsing.
    with open(bibtex, 'r', encoding='utf-8') as bibtex_file:
        parser = BibTexParser(common_strings=True)
        parser.customization = convert_to_unicode
        bib_database = bibtexparser.load(bibtex_file, parser=parser)
        for entry in bib_database.entries:
            parse_bibtex_entry(entry, pub_dir=pub_dir, featured=featured, overwrite=overwrite, normalize=normalize)


def parse_bibtex_entry(entry, pub_dir='publication', featured=False, overwrite=False, normalize=False):
    """Parse a bibtex entry and generate corresponding publication bundle"""
    print(f"Parsing entry {entry['ID']}")

    bundle_path = f"content/{pub_dir}/{slugify(entry['ID'])}"
    markdown_path = os.path.join(bundle_path, 'index.md')
    cite_path = os.path.join(bundle_path, f"{slugify(entry['ID'])}.bib")
    date = datetime.utcnow()
    timestamp = date.isoformat('T') + 'Z'  # RFC 3339 timestamp.

    # Do not overwrite publication bundle if it already exists.
    if not overwrite and os.path.isdir(bundle_path):
        print(f'Skipping creation of {bundle_path} as it already exists. To overwrite, add the `--overwrite` argument.')
        return

    # Create bundle dir.
    print(f'Creating folder {bundle_path}')
    Path(bundle_path).mkdir(parents=True, exist_ok=True)

    # Save citation file.
    print(f'Saving citation to {cite_path}')
    db = BibDatabase()
    db.entries = [entry]
    writer = BibTexWriter()
    with open(cite_path, 'w', encoding='utf-8') as f:
        f.write(writer.write(db))

    # Prepare YAML front matter for Markdown file.
    frontmatter = ['---']
    frontmatter.append(f'title: "{clean_bibtex_str(entry["title"])}"')
    if 'month' in entry:
        frontmatter.append(f"date: {entry['year']}-{month2number(entry['month'])}-01")
    else:
        frontmatter.append(f"date: {entry['year']}-01-01")

    frontmatter.append(f"publishDate: {timestamp}")

    authors = None
    if 'author' in entry:
        authors = entry['author']
    elif 'editor' in entry:
        authors = entry['editor']
    if authors:
        authors = clean_bibtex_authors([i.strip() for i in authors.replace('\n', ' ').split(' and ')])
        frontmatter.append(f"authors: [{', '.join(authors)}]")

    frontmatter.append(f'publication_types: ["{PUB_TYPES.get(entry["ENTRYTYPE"], 0)}"]')

    if 'abstract' in entry:
        frontmatter.append(f'abstract: "{clean_bibtex_str(entry["abstract"])}"')
    else:
        frontmatter.append('abstract: ""')

    frontmatter.append(f'featured: {str(featured).lower()}')

    # Publication name.
    if 'booktitle' in entry:
        frontmatter.append(f'publication: "*{clean_bibtex_str(entry["booktitle"])}*"')
    elif 'journal' in entry:
        frontmatter.append(f'publication: "*{clean_bibtex_str(entry["journal"])}*"')
    else:
        frontmatter.append('publication: ""')

    if 'keywords' in entry:
        frontmatter.append(f'tags: [{clean_bibtex_tags(entry["keywords"], normalize)}]')

    if 'url' in entry:
        frontmatter.append(f'url_pdf: "{clean_bibtex_str(entry["url"])}"')

    if 'doi' in entry:
        frontmatter.append(f'doi: "{entry["doi"]}"')

    frontmatter.append('---\n\n')

    # Save Markdown file.
    try:
        print(f"Saving Markdown to '{markdown_path}'")
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(frontmatter))
    except IOError:
        print('ERROR: could not save file.')


def slugify(s, lower=True):
    bad_symbols = ('.', '_', ':')  # Symbols to replace with hyphen delimiter.
    delimiter = '-'
    good_symbols = (delimiter,)  # Symbols to keep.
    for r in bad_symbols:
        s = s.replace(r, delimiter)

    s = re.sub(r'(\D+)(\d+)', r'\1\-\2', s)  # Delimit non-number, number.
    s = re.sub(r'(\d+)(\D+)', r'\1\-\2', s)  # Delimit number, non-number.
    s = re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r'\-\1', s)  # Delimit camelcase.
    s = ''.join(c for c in s if c.isalnum() or c in good_symbols).strip()  # Strip non-alphanumeric and non-hyphen.
    s = re.sub('\-+', '-', s)  # Remove consecutive hyphens.

    if lower:
        s = s.lower()
    return s


def clean_bibtex_authors(author_str):
    """Convert author names to `firstname(s) lastname` format."""
    authors = []
    for s in author_str:
        s = s.strip()
        if len(s) < 1:
            continue
        if ',' in s:
            split_names = s.split(',', 1)
            last_name = split_names[0].strip()
            first_names = [i.strip() for i in split_names[1].split()]
        else:
            split_names = s.split()
            last_name = split_names.pop()
            first_names = [i.replace('.', '. ').strip() for i in split_names]
        if last_name in ['jnr', 'jr', 'junior']:
            last_name = first_names.pop()
        for item in first_names:
            if item in ['ben', 'van', 'der', 'de', 'la', 'le']:
                last_name = first_names.pop() + ' ' + last_name
        authors.append(f'"{" ".join(first_names)} {last_name}"')
    return authors


def clean_bibtex_str(s):
    """Clean BibTeX string and escape TOML special characters"""
    s = s.replace('\\', '')
    s = s.replace('"', '\\"')
    s = s.replace('{', '').replace('}', '')
    s = s.replace('\t', ' ').replace('\n', ' ').replace('\r', '')
    return s


def clean_bibtex_tags(s, normalize=False):
    """Clean BibTeX keywords and convert to TOML tags"""
    tags = clean_bibtex_str(s).split(',')
    tags = [f'"{tag.strip()}"' for tag in tags]
    if normalize:
        tags = [tag.lower().capitalize() for tag in tags]
    tags_str = ', '.join(tags)
    return tags_str


def month2number(month):
    """Convert BibTeX month to numeric"""
    month_abbr = month.strip()[:3].title()
    try:
        return str(list(calendar.month_abbr).index(month_abbr)).zfill(2)
    except ValueError:
        raise ValueError('Please update your BibTeX with valid months')


def import_assets():
    """Download and import third-party JS and CSS assets to enable offline sites"""

    # Check that we are in an Academic website folder.
    if not Path('content').is_dir():
        print('Please navigate to your website folder and re-run.')
        return

    # Check compatibility with user's Academic version (v2.4.0+ required for local asset bundling)
    # `academic.toml` was added in Academic v2.4.0, so can simply check for the existence of that file.
    academic_filename = 'themes/academic/data/academic.toml'
    if not Path(academic_filename).is_file():
        print('Could not detect Academic version in `themes/academic/data/academic.toml`. You may need to update Academic in order to use this tool.')
        return

    # Check assets file exists
    # Note that the order of assets in `assets.toml` matters since they will be concatenated in the order they appear.
    assets_filename = 'themes/academic/data/assets.toml'
    if not Path(assets_filename).is_file():
        print('Could not detect assets file. You may need to update Academic in order to use this tool.')
        return

    # Create output dirs if necessary
    Path(JS_FILENAME).parent.mkdir(parents=True, exist_ok=True)
    Path(CSS_FILENAME).parent.mkdir(parents=True, exist_ok=True)

    # Parse TOML file which lists assets
    parsed_toml = toml.load(assets_filename)

    # Create temporary directory for downloaded assets.
    with tempfile.TemporaryDirectory() as d:
        # Parse JS assets
        js_files = []
        for i, j in parsed_toml['js'].items():
            url = j['url'].replace('%s', j['version'], 1)  # Replace placeholder with asset version.
            filename = os.path.basename(urlparse(url).path)
            filepath = os.path.join(d, filename)
            js_files.append(filepath)

            print(f'Downloading {filename} from {url}...')
            download_file(url, filepath)

        print(f'Merging JS assets into {JS_FILENAME}')
        merge_files(js_files, JS_FILENAME)

        # Parse CSS assets
        css_files = []
        for i, j in parsed_toml['css'].items():
            url = j['url'].replace('%s', j['version'], 1)  # Replace placeholder with asset version.

            # Special case for highlight.js style
            if i == 'highlight':
                # Assume user is using a light theme.
                # TODO: Set to .Site.Params.highlight_style if set, or dracula if using a dark theme.
                hl_theme = 'github'
                url = url.replace('%s', hl_theme)  # Replace the second placeholder with style name.
            filename = os.path.basename(urlparse(url).path)
            filepath = os.path.join(d, filename)
            css_files.append(filepath)

            print(f'Downloading {filename} from {url}...')
            download_file(url, filepath)

        print(f'Merging CSS assets into {CSS_FILENAME}')
        merge_files(css_files, CSS_FILENAME)


def download_file(url, file_name):
    """Download file from URL"""
    with open(file_name, 'wb') as file:
        # Get file at URL.
        response = get(url)

        # Check that we can access the specified URL OK.
        if response.status_code != 200:
            print(f'ERROR could not download {url}')
            return

        # Write to file.
        file.write(response.content)


def merge_files(file_path_list, destination):
    """Merge multiple files into one file"""
    with open(destination, 'w', encoding='utf-8') as f:
        for file_path in file_path_list:
            with open(file_path, 'r', encoding='utf-8') as source_file:
                f.write(source_file.read() + '\n')


if __name__ == '__main__':
    main()
