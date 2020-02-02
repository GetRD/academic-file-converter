#!/usr/bin/env python3

import subprocess
import sys
import os
import re
import argparse
from argparse import RawTextHelpFormatter
from pathlib import Path
import calendar
import logging
from datetime import datetime
from academic import __version__ as version
from academic.import_assets import import_assets

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.customization import convert_to_unicode

# Map BibTeX to Academic publication types.
PUB_TYPES = {
    "article": 2,
    "book": 5,
    "inbook": 6,
    "incollection": 6,
    "inproceedings": 1,
    "manual": 4,
    "mastersthesis": 7,
    "misc": 0,
    "phdthesis": 7,
    "proceedings": 0,
    "techreport": 4,
    "unpublished": 3,
    "patent": 8,
}

# Map BibLaTeX to Academic publication types.
# See https://github.com/zotero/translators/blob/master/BibLaTeX.js
# NOTE: This will require changes in the following to fully support:
# - the language packs in the local i18n folder (not in the theme folder)
# - the local data/publication_types.toml (not in the theme folder)

BIBLATEX_PUB_TYPES = {
    "article": 2,
    "artwork": 11,
    "audio": 16,
    "audiorecording": 16,
    "bill": 14,
    "blogPost": 12,
    "book": 5,
    "bookSection": 6,
    "case": 15,
    "computerProgram": 18,
    "conferencePaper": 1,
    "dictionaryEntry": 19,
    "document": 0,
    "email": 9,
    "encyclopediaArticle": 19,
    "film": 10,
    "forumPost": 12,
    "hearing": 15,
    "inbook": 6,
    "incollection": 6,
    "inproceedings": 1,
    "inreference": 19,
    "instantMessage": 0,
    "interview": 0,
    "journalArticle": 2,
    "jurisdiction": 15,
    "legislation": 14,
    "letter": 9,
    "magazineArticle": 2,
    "manual": 4,
    "manuscript": 3,
    "map": 0,
    "mastersthesis": 7,
    "misc": 0,
    "movie": 10,
    "newspaperArticle": 2,
    "online": 12,
    "patent": 8,
    "phdthesis": 7,
    "podcast": 16,
    "presentation": 3,
    "proceedings": 0,
    "radioBroadcast": 0,
    "report": 13,
    "software": 18,
    "statute": 14,
    "techreport": 4,
    "thesis": 7,
    "tvBroadcast": 0,
    "unpublished": 3,
    "video": 17,
    "videoRecording": 17,
    "webpage": 12
}

# Initialise logger.
logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=logging.WARNING, datefmt="%I:%M:%S%p")
log = logging.getLogger(__name__)


class AcademicError(Exception):
    pass


def main():
    parse_args(sys.argv[1:])  # Strip command name, leave just args.


def parse_args(args):
    """Parse command-line arguments"""

    # Initialise command parser.
    parser = argparse.ArgumentParser(
        description=f"Academic Admin Tool v{version}\nhttps://sourcethemes.com/academic/", formatter_class=RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(help="Sub-commands", dest="command")

    # Sub-parser for import command.
    parser_a = subparsers.add_parser("import", help="Import data into Academic")
    parser_a.add_argument("--assets", action="store_true", help="Import third-party JS and CSS for generating an offline site")
    parser_a.add_argument("--bibtex", required=False, type=str, help="File path to your BibTeX file")
    parser_a.add_argument("--biblatex", required=False, type=str, help="File path to your BibLaTeX file")
    parser_a.add_argument(
        "--publication-dir",
        required=False,
        type=str,
        default="publication",
        help="Directory that your publications are stored in (default `publication`)",
    )
    parser_a.add_argument("--featured", action="store_true", help="Flag publications as featured")
    parser_a.add_argument("--overwrite", action="store_true", help="Overwrite existing publications")
    parser_a.add_argument("--normalize", action="store_true", help="Normalize each keyword to lowercase with uppercase first letter")
    parser_a.add_argument("--date-title-folders", action="store_true", help="Create folders for imported publications named by date and title")
    parser_a.add_argument("--title-folders", action="store_true", help="Create folders for imported publications named by title")
    parser_a.add_argument("-v", "--verbose", action="store_true", required=False, help="Verbose mode")
    parser_a.add_argument("-dr", "--dry-run", action="store_true", required=False, help="Perform a dry run (Bibtex only)")
    known_args, unknown = parser.parse_known_args(args)

    # If no arguments, show help.
    if len(args) == 0:
        parser.print_help()
        parser.exit()

    # If no known arguments, wrap Hugo command.
    elif known_args is None and unknown:
        cmd = []
        cmd.append("hugo")
        if args:
            cmd.append(args)
        subprocess.call(cmd)
    else:
        # The command has been recognised, proceed to parse it.
        if known_args.command and known_args.verbose:
            # Set logging level to debug if verbose mode activated.
            logging.getLogger().setLevel(logging.DEBUG)
        if known_args.command and known_args.assets:
            # Run command to import assets.
            import_assets()
        elif known_args.command and known_args.bibtex and known_args.biblatex:
            err = "cannot specify both --bibtex and --biblatex"
            log.error(err)
            raise AcademicError(err)
        elif known_args.command and known_args.date_title_folders and known_args.title_folders:
            err = "cannot specify both --date-title-folders and --title-folders"
            log.error(err)
            raise AcademicError(err)
        elif known_args.command and known_args.bibtex:
            # Run command to import bibtex.
            import_bibtex(
                known_args.bibtex,
                pub_dir=known_args.publication_dir,
                featured=known_args.featured,
                overwrite=known_args.overwrite,
                normalize=known_args.normalize,
                dry_run=known_args.dry_run,
                date_title_folders=known_args.date_title_folders,
                title_folders=known_args.title_folders,
                use_biblatex=False
            )
        elif known_args.command and known_args.biblatex:
            # Run command to import biblatex.
            import_bibtex(
                known_args.biblatex,
                pub_dir=known_args.publication_dir,
                featured=known_args.featured,
                overwrite=known_args.overwrite,
                normalize=known_args.normalize,
                dry_run=known_args.dry_run,
                date_title_folders=known_args.date_title_folders,
                title_folders=known_args.title_folders,
                use_biblatex=True
            )

def import_bibtex(
    bibtex,
    pub_dir="publication",
    featured=False,
    overwrite=False,
    normalize=False,
    dry_run=False,
    date_title_folders=False,
    title_folders=False,
    use_biblatex=False
):
    """Import publications from BibTeX file"""

    # Check BibTeX file exists.
    if not Path(bibtex).is_file():
        err = "Please check the path to your BibTeX file and re-run"
        log.error(err)
        raise AcademicError(err)

    # Load BibTeX file for parsing.
    with open(bibtex, "r", encoding="utf-8") as bibtex_file:
        parser = BibTexParser(common_strings=True)
        parser.customization = convert_to_unicode
        parser.ignore_nonstandard_types = False
        bib_database = bibtexparser.load(bibtex_file, parser=parser)
        for entry in bib_database.entries:
            parse_bibtex_entry(
                entry,
                pub_dir=pub_dir,
                featured=featured,
                overwrite=overwrite,
                normalize=normalize,
                dry_run=dry_run,
                date_title_folders=date_title_folders,
                title_folders=title_folders,
                use_biblatex=use_biblatex
            )


# Move date-related logic to the beginning so that date value is
# available for generating folder name.
#
# Truncate title to 68 characters in folder name to keep overall
# filename limit to 79 characters which includes the date.
#
# Accept use_biblatex flag to determine whether to validate tyoes
# against BibLaTex list.

def parse_bibtex_entry(
    entry,
    pub_dir="publication",
    featured=False,
    overwrite=False,
    normalize=False,
    dry_run=False,
    date_title_folders=False,
    title_folders=False,
    use_biblatex=False
):
    """Parse a bibtex entry and generate corresponding publication bundle"""
    log.info(f"Parsing entry {entry['ID']}")

    year = ""
    month = "01"
    day = "01"
    if "date" in entry:
        dateparts = entry["date"].split("-")
        if len(dateparts) == 3:
            year, month, day = dateparts[0], dateparts[1], dateparts[2]
        elif len(dateparts) == 2:
            year, month = dateparts[0], dateparts[1]
        elif len(dateparts) == 1:
            year = dateparts[0]
    if "month" in entry and month == "01":
        month = month2number(entry["month"])
    if "year" in entry and year == "":
        year = entry["year"]
    if len(year) == 0:
        log.error(f'Invalid date for entry `{entry["ID"]}`.')

    title = entry["title"].strip()
    if date_title_folders and "title" in entry and title:
        file_name = f"{year}-{month}-{day}-{title:.68}"
    elif title_folders and "title" in entry and title:
        file_name = f"{title:.79}"
    else:
        file_name = entry["ID"]
        
    bundle_path = f"content/{pub_dir}/{slugify(file_name)}"
    markdown_path = os.path.join(bundle_path, "index.md")
    cite_path = os.path.join(bundle_path, "cite.bib")
    date = datetime.utcnow()
    timestamp = date.isoformat("T") + "Z"  # RFC 3339 timestamp.

    # Do not overwrite publication bundle if it already exists.
    if not overwrite and os.path.isdir(bundle_path):
        log.warning(f"Skipping creation of {bundle_path} as it already exists. " f"To overwrite, add the `--overwrite` argument.")
        return

    # Create bundle dir.
    log.info(f"Creating folder {bundle_path}")
    if not dry_run:
        Path(bundle_path).mkdir(parents=True, exist_ok=True)
    else:
        print(bundle_path)

    # Save citation file.
    log.info(f"Saving citation to {cite_path}")
    db = BibDatabase()
    db.entries = [entry]
    writer = BibTexWriter()
    if not dry_run:
        with open(cite_path, "w", encoding="utf-8") as f:
            f.write(writer.write(db))

    # Prepare YAML front matter for Markdown file.
    frontmatter = ["---"]
    frontmatter.append(f'title: "{clean_bibtex_str(entry["title"])}"')
    frontmatter.append(f"date: {year}-{month}-{day}")

    frontmatter.append(f"publishDate: {timestamp}")

    authors = None
    if "author" in entry:
        authors = entry["author"]
    elif "editor" in entry:
        authors = entry["editor"]
    if authors:
        authors = clean_bibtex_authors([i.strip() for i in authors.replace("\n", " ").split(" and ")])
        frontmatter.append(f"authors: [{', '.join(authors)}]")

    if use_biblatex:
        frontmatter.append(f'publication_types: ["{BIBLATEX_PUB_TYPES.get(entry["ENTRYTYPE"], 0)}"]')
    else:
        frontmatter.append(f'publication_types: ["{PUB_TYPES.get(entry["ENTRYTYPE"], 0)}"]')

    if "abstract" in entry:
        frontmatter.append(f'abstract: "{clean_bibtex_str(entry["abstract"])}"')
    else:
        frontmatter.append('abstract: ""')

    frontmatter.append(f"featured: {str(featured).lower()}")

    # Publication name.
    if "booktitle" in entry:
        frontmatter.append(f'publication: "*{clean_bibtex_str(entry["booktitle"])}*"')
    elif "journal" in entry:
        frontmatter.append(f'publication: "*{clean_bibtex_str(entry["journal"])}*"')
    elif "publisher" in entry:
        frontmatter.append(f'publication: "*{clean_bibtex_str(entry["publisher"])}*"')
    else:
        frontmatter.append('publication: ""')

    if "keywords" in entry:
        frontmatter.append(f'tags: [{clean_bibtex_tags(entry["keywords"], normalize)}]')

    if "url" in entry:
        frontmatter.append(f'url_pdf: "{clean_bibtex_str(entry["url"])}"')

    if "doi" in entry:
        frontmatter.append(f'doi: "{entry["doi"]}"')

    frontmatter.append("---\n\n")

    # Save Markdown file.
    try:
        log.info(f"Saving Markdown to '{markdown_path}'")
        if not dry_run:
            with open(markdown_path, "w", encoding="utf-8") as f:
                f.write("\n".join(frontmatter))
    except IOError:
        log.error("Could not save file.")


# Add the space character to bad_symbols so that spaces are replaced by
# hyphens when the "--date-title-folders" argument is used.
#
# Remove trailing hyphen.

def slugify(s, lower=True):
    bad_symbols = (".", "_", ":", " ")  # Symbols to replace with hyphen delimiter.
    delimiter = "-"
    good_symbols = (delimiter,)  # Symbols to keep.
    for r in bad_symbols:
        s = s.replace(r, delimiter)

    s = re.sub(r"(\D+)(\d+)", r"\1\-\2", s)  # Delimit non-number, number.
    s = re.sub(r"(\d+)(\D+)", r"\1\-\2", s)  # Delimit number, non-number.
    s = re.sub(r"((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))", r"\-\1", s)  # Delimit camelcase.
    s = "".join(c for c in s if c.isalnum() or c in good_symbols).strip()  # Strip non-alphanumeric and non-hyphen.
    s = re.sub("-{2,}", "-", s)  # Remove consecutive hyphens.
    s = re.sub("-$", "", s) # Remove trailing hyphen.

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
        if "," in s:
            split_names = s.split(",", 1)
            last_name = split_names[0].strip()
            first_names = [i.strip() for i in split_names[1].split()]
        else:
            split_names = s.split()
            last_name = split_names.pop()
            first_names = [i.replace(".", ". ").strip() for i in split_names]
        if last_name in ["jnr", "jr", "junior"]:
            last_name = first_names.pop()
        for item in first_names:
            if item in ["ben", "van", "der", "de", "la", "le"]:
                last_name = first_names.pop() + " " + last_name
        authors.append(f'"{" ".join(first_names)} {last_name}"')
    return authors


def clean_bibtex_str(s):
    """Clean BibTeX string and escape TOML special characters"""
    s = s.replace("\\", "")
    s = s.replace('"', '\\"')
    s = s.replace("{", "").replace("}", "")
    s = s.replace("\t", " ").replace("\n", " ").replace("\r", "")
    return s


def clean_bibtex_tags(s, normalize=False):
    """Clean BibTeX keywords and convert to TOML tags"""
    tags = clean_bibtex_str(s).split(",")
    tags = [f'"{tag.strip()}"' for tag in tags]
    if normalize:
        tags = [tag.lower().capitalize() for tag in tags]
    tags_str = ", ".join(tags)
    return tags_str


def month2number(month):
    """Convert BibTeX or BibLateX month to numeric"""
    if len(month) <= 2:  # Assume a 1 or 2 digit numeric month has been given.
        return month.zfill(2)
    else:  # Assume a textual month has been given.
        month_abbr = month.strip()[:3].title()
        try:
            return str(list(calendar.month_abbr).index(month_abbr)).zfill(2)
        except ValueError:
            raise log.error("Please update the entry with a valid month.")


if __name__ == "__main__":
    main()
