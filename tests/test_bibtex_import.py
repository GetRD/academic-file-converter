import logging
import tempfile
from pathlib import Path

import bibtexparser
from bibtexparser.bparser import BibTexParser

from academic import cli
from academic import import_bibtex
from academic.editFM import EditableFM


bibtex_dir = Path(__file__).parent / 'data'


def test_bibtex_import():
    cli.parse_args(["import", "--dry-run", "--bibtex", "tests/data/article.bib"])


def _process_bibtex(file, expected_count=1):
    parser = BibTexParser(common_strings=True)
    parser.customization = import_bibtex.convert_to_unicode
    parser.ignore_nonstandard_types = False
    with Path(bibtex_dir, file).open("r", encoding="utf-8") as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file, parser=parser)
        results = []
        for entry in bib_database.entries:
            results.append(import_bibtex.parse_bibtex_entry(entry, dry_run=True))
        assert len(results) == expected_count
        return results

def _test_publication_type(metadata: EditableFM, expected_type: import_bibtex.PublicationType):
    assert metadata.fm["publication_types"] == [str(expected_type.value)]

def test_bibtex_types():
    _test_publication_type(_process_bibtex('article.bib')[0], import_bibtex.PublicationType.JournalArticle)
    _test_publication_type(_process_bibtex('report.bib')[0], import_bibtex.PublicationType.Report)
