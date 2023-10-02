import typing
from pathlib import Path

import bibtexparser
from bibtexparser.bparser import BibTexParser

from academic import cli, import_bibtex
from academic.generate_markdown import GenerateMarkdown

bibtex_dir = Path(__file__).parent / "data"


def test_bibtex_import():
    cli.parse_args(["import", "--dry-run", "tests/data/article.bib", "content/publication/"])


def _process_bibtex(file, expected_count=1) -> "typing.List[GenerateMarkdown]":
    """
    Parse a BibTeX .bib file and return the parsed metadata
    :param file: The .bib file to parse
    :param expected_count: The expected number of entries inside the .bib
    :return: The parsed metadata as a list of EditableFM
    """
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


def _test_publication_type(metadata: GenerateMarkdown, expected_type: str):
    """
    Check that the publication_types field of the parsed metadata is set to the expected type.
    """
    assert metadata.yaml["publication_types"] == [expected_type]


def test_bibtex_types():
    """
    This test uses the import_bibtex functions to parse a .bib file and checks that the
    resulting metadata has the correct publication type set.
    """
    _test_publication_type(_process_bibtex("article.bib")[0], "article-journal")
    for metadata in _process_bibtex("report.bib", expected_count=2):
        _test_publication_type(metadata, "report")
    for metadata in _process_bibtex("thesis.bib", expected_count=3):
        _test_publication_type(metadata, "thesis")
    for metadata in _process_bibtex("book.bib", expected_count=2):
        _test_publication_type(metadata, "book")
