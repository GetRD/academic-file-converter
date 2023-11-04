import calendar
import os
import re
from datetime import datetime
from pathlib import Path

import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.customization import convert_to_unicode

from academic.generate_markdown import GenerateMarkdown
from academic.publication_type import PUB_TYPES_BIBTEX_TO_CSL


def import_bibtex(
    bibtex,
    pub_dir=os.path.join("content", "publication"),
    featured=False,
    overwrite=False,
    normalize=False,
    compact=False,
    dry_run=False,
):
    """Import publications from BibTeX file"""
    from academic.cli import log
    from academic.utils import AcademicError

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
                compact=compact,
                dry_run=dry_run,
            )


def parse_bibtex_entry(
    entry,
    pub_dir=os.path.join("content", "publication"),
    featured=False,
    overwrite=False,
    normalize=False,
    compact=False,
    dry_run=False,
):
    """Parse a bibtex entry and generate corresponding publication bundle"""
    from academic.cli import log

    log.info(f"Parsing entry {entry['ID']}")

    bundle_path = os.path.join(pub_dir, slugify(entry["ID"]))
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

    # Save citation file.
    log.info(f"Saving citation to {cite_path}")
    db = BibDatabase()
    db.entries = [entry]
    writer = BibTexWriter()
    if not dry_run:
        with open(cite_path, "w", encoding="utf-8") as f:
            f.write(writer.write(db))

    # Prepare YAML front matter for Markdown file.
    if not dry_run:
        from importlib import resources as import_resources

        # Load the Markdown template from within the `templates` folder of the `academic` package
        template = import_resources.read_text(__package__ + ".templates", "publication.md")

        with open(markdown_path, "w") as f:
            f.write(template)

    page = GenerateMarkdown(Path(bundle_path), dry_run=dry_run, compact=compact)
    page.load(Path("index.md"))

    page.yaml["title"] = clean_bibtex_str(entry["title"])

    if "subtitle" in entry:
        page.yaml["subtitle"] = clean_bibtex_str(entry["subtitle"])

    year, month, day = "", "01", "01"
    if "date" in entry:
        date_parts = entry["date"].split("-")
        if len(date_parts) == 3:
            year, month, day = date_parts[0], date_parts[1], date_parts[2]
        elif len(date_parts) == 2:
            year, month = date_parts[0], date_parts[1]
        elif len(date_parts) == 1:
            year = date_parts[0]
    if "month" in entry and month == "01":
        month = month2number(entry["month"])
    if "year" in entry and year == "":
        year = entry["year"]
    if len(year) == 0:
        log.error(f'Invalid date for entry `{entry["ID"]}`.')

    page.yaml["date"] = f"{year}-{month}-{day}"
    page.yaml["publishDate"] = timestamp

    authors = None
    if "author" in entry:
        authors = entry["author"]
    elif "editor" in entry:
        authors = entry["editor"]

    if authors:
        authors = clean_bibtex_authors([i.strip() for i in authors.replace("\n", " ").split(" and ")])
        page.yaml["authors"] = authors

    # Convert Bibtex publication type to the universal CSL standard, defaulting to `manuscript`
    default_csl_type = "manuscript"
    pub_type = PUB_TYPES_BIBTEX_TO_CSL.get(entry["ENTRYTYPE"], default_csl_type)
    page.yaml["publication_types"] = [pub_type]

    if "abstract" in entry:
        page.yaml["abstract"] = clean_bibtex_str(entry["abstract"])
    else:
        page.yaml["abstract"] = ""

    page.yaml["featured"] = featured

    # Publication name.
    # This field is Markdown formatted, wrapping the publication name in `*` for italics
    if "booktitle" in entry:
        publication = "*" + clean_bibtex_str(entry["booktitle"]) + "*"
    elif "journal" in entry:
        publication = "*" + clean_bibtex_str(entry["journal"]) + "*"
    elif "publisher" in entry:
        publication = "*" + clean_bibtex_str(entry["publisher"]) + "*"
    else:
        publication = ""
    page.yaml["publication"] = publication

    if "keywords" in entry:
        page.yaml["tags"] = clean_bibtex_tags(entry["keywords"], normalize)

    if "doi" in entry:
        page.yaml["doi"] = clean_bibtex_str(entry["doi"])

    links = []
    if all(f in entry for f in ["archiveprefix", "eprint"]) and entry["archiveprefix"].lower() == "arxiv":
        links += [{"name": "arXiv", "url": "https://arxiv.org/abs/" + clean_bibtex_str(entry["eprint"])}]

    if "url" in entry:
        sane_url = clean_bibtex_str(entry["url"])

        if sane_url[-4:].lower() == ".pdf":
            page.yaml["url_pdf"] = sane_url
        else:
            links += [{"name": "URL", "url": sane_url}]

    if links:
        page.yaml["links"] = links

    # Save Markdown file.
    try:
        log.info(f"Saving Markdown to '{markdown_path}'")
        if not dry_run:
            page.dump()
    except IOError:
        log.error("Could not save file.")
    return page


def slugify(s, lower=True):
    bad_symbols = (".", "_", ":")  # Symbols to replace with hyphen delimiter.
    delimiter = "-"
    good_symbols = (delimiter,)  # Symbols to keep.
    for r in bad_symbols:
        s = s.replace(r, delimiter)

    s = re.sub(r"(\D+)(\d+)", r"\1\-\2", s)  # Delimit non-number, number.
    s = re.sub(r"(\d+)(\D+)", r"\1\-\2", s)  # Delimit number, non-number.
    s = re.sub(r"((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))", r"\-\1", s)  # Delimit camelcase.
    s = "".join(c for c in s if c.isalnum() or c in good_symbols).strip()  # Strip non-alphanumeric and non-hyphen.
    s = re.sub("-{2,}", "-", s)  # Remove consecutive hyphens.

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

        authors.append(" ".join(first_names) + " " + last_name)

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
    tags = [tag.strip() for tag in tags]

    if normalize:
        tags = [tag.lower().capitalize() for tag in tags]

    return tags


def month2number(month):
    """Convert BibTeX or BibLateX month to numeric"""
    from academic.cli import log

    if len(month) <= 2:  # Assume a 1 or 2 digit numeric month has been given.
        return month.zfill(2)
    else:  # Assume a textual month has been given.
        month_abbr = month.strip()[:3].title()
        try:
            return str(list(calendar.month_abbr).index(month_abbr)).zfill(2)
        except ValueError:
            log.error("Please update the entry with a valid month.")
