#!/usr/bin/env python3

import argparse
import importlib.metadata
import logging
import sys
from argparse import RawTextHelpFormatter

from academic.import_bibtex import import_bibtex
from academic.import_notebook import import_notebook

# Initialise logger.
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.WARNING,
    datefmt="%I:%M:%S%p",
)
log = logging.getLogger(__name__)


def main():
    # Strip command name (currently `academic`) and feed arguments to the parser
    parse_args(sys.argv[1:])


def parse_args(args):
    """Parse command-line arguments"""

    # Initialise command parser.
    version = importlib.metadata.version("academic")
    parser = argparse.ArgumentParser(
        description=f"Academic CLI v{version}\nhttps://github.com/GetRD/academic-file-converter",
        formatter_class=RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(help="Sub-commands", dest="command")

    # Sub-parser for import command.
    parser_a = subparsers.add_parser("import", help="Import content into your website or book")
    parser_a.add_argument("input", type=str, help="File path to your BibTeX or Jupyter Notebook file(s)")
    parser_a.add_argument("output", type=str, help="Output path (e.g. `content/publication/`)")
    parser_a.add_argument("--featured", action="store_true", help="Flag publications as featured")
    parser_a.add_argument("--overwrite", action="store_true", help="Overwrite existing files in output path")
    parser_a.add_argument("--compact", action="store_true", help="Generate minimal markdown")
    parser_a.add_argument(
        "--normalize",
        action="store_true",
        help="Normalize each BibTeX keyword to lowercase with uppercase first letter",
    )
    parser_a.add_argument("-v", "--verbose", action="store_true", required=False, help="Verbose mode")
    parser_a.add_argument(
        "-dr",
        "--dry-run",
        action="store_true",
        required=False,
        help="Perform a dry run (e.g. for testing purposes)",
    )

    known_args, unknown = parser.parse_known_args(args)

    # If no arguments, show help.
    if len(args) == 0:
        parser.print_help()
        parser.exit()
    else:
        # The command has been recognised, proceed to parse it.
        if known_args.command:
            if known_args.verbose:
                # Set logging level to debug if verbose mode activated.
                logging.getLogger().setLevel(logging.INFO)
            if known_args.input.lower().endswith(".bib"):
                # Run command to import bibtex.
                import_bibtex(
                    known_args.input,
                    pub_dir=known_args.output,
                    featured=known_args.featured,
                    overwrite=known_args.overwrite,
                    normalize=known_args.normalize,
                    compact=known_args.compact,
                    dry_run=known_args.dry_run,
                )
            elif known_args.input.lower().endswith(".ipynb"):
                # Run command to import bibtex.
                import_notebook(
                    known_args.input,
                    output_dir=known_args.output,
                    overwrite=known_args.overwrite,
                    dry_run=known_args.dry_run,
                )


if __name__ == "__main__":
    main()
