import logging

from academic import cli


def test_notebook_import_no_output(capfd):
    """
    The importer does not have a flag to determine what formats the user intends to convert.
    Instead, it relies on the file extension in the input string.
    If there is no file extension (e.g. just a wildcard), then expect no output.
    """
    cli.parse_args(["import", "--dry-run", "--verbose", "tests/data/notebooks/*", "content/post/"])
    out, err = capfd.readouterr()
    assert out == ""
    assert err == ""


def test_notebook_import_info_level(caplog):
    caplog.set_level(logging.INFO)

    cli.parse_args(
        [
            "import",
            "tests/data/notebooks/*.ipynb",
            "content/post/",
            "--dry-run",
        ]
    )
    # assert "Found notebook `test.ipynb`" in out
    assert "Searching for Jupyter notebooks in `tests/data/notebooks/*.ipynb`" in caplog.text


def test_notebook_import_debug_level(caplog):
    caplog.set_level(logging.DEBUG)

    cli.parse_args(
        [
            "import",
            "tests/data/notebooks/*.ipynb",
            "content/post/",
            "--dry-run",
        ]
    )

    # Note: this logging output should only be shown at DEBUG log level, so we set the corresponding level above
    assert "Found notebook `tests/data/notebooks/test.ipynb`" in caplog.text
    assert "Found notebook `tests/data/notebooks/blog-with-jupyter.ipynb`" in caplog.text
