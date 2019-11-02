from academic import cli


def test_bibtex_import():
    cli.parse_args(['import', '--dry-run', '--bibtex', 'tests/data/article.bib'])
