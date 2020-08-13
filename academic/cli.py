#!/usr/bin/env python3

import argparse
import logging
import subprocess
import sys
from argparse import RawTextHelpFormatter

from academic import __version__ as version
from academic import utils
from academic.import_assets import import_assets
from academic.import_bibtex import import_bibtex

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

# Initialise logger.
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s", level=logging.WARNING, datefmt="%I:%M:%S%p",
)
log = logging.getLogger(__name__)


class AcademicError(Exception):
    pass


def main():
    parse_args(sys.argv[1:])  # Strip command name, leave just args.


def parse_args(args):
    """Parse command-line arguments"""

    # Initialise command parser.
    parser = argparse.ArgumentParser(
        description=f"Academic Admin Tool v{version}\nhttps://sourcethemes.com/academic/", formatter_class=RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(help="Sub-commands", dest="command")

    # Sub-parser for import command.
    parser_a = subparsers.add_parser("import", help="Import data into Academic")
    parser_a.add_argument(
        "--assets", action="store_true", help="Import third-party JS and CSS for generating an offline site",
    )
    parser_a.add_argument("--bibtex", required=False, type=str, help="File path to your BibTeX file")
    parser_a.add_argument(
        "--publication-dir",
        required=False,
        type=str,
        default="publication",
        help="Directory that your publications are stored in (default `publication`)",
    )
    parser_a.add_argument("--featured", action="store_true", help="Flag publications as featured")
    parser_a.add_argument("--overwrite", action="store_true", help="Overwrite existing publications")
    parser_a.add_argument(
        "--normalize", action="store_true", help="Normalize each keyword to lowercase with uppercase first letter",
    )
    parser_a.add_argument("-v", "--verbose", action="store_true", required=False, help="Verbose mode")
    parser_a.add_argument(
        "-dr", "--dry-run", action="store_true", required=False, help="Perform a dry run (Bibtex only)",
    )

    known_args, unknown = parser.parse_known_args(args)

    # If no arguments, show help.
    if len(args) == 0:
        parser.print_help()
        parser.exit()

    # If no known arguments, wrap Hugo command.
    elif known_args is None and unknown:
        cmd = utils.hugo_in_docker_or_local()
        if args:
            cmd = " ".join([cmd, args])
        subprocess.call(cmd)
    else:
        # The command has been recognised, proceed to parse it.
        if known_args.command and known_args.verbose:
            # Set logging level to debug if verbose mode activated.
            logging.getLogger().setLevel(logging.DEBUG)
        if known_args.command and known_args.assets:
            # Run command to import assets.
            import_assets()
        elif known_args.command and known_args.bibtex:
            # Run command to import bibtex.
            import_bibtex(
                known_args.bibtex,
                pub_dir=known_args.publication_dir,
                featured=known_args.featured,
                overwrite=known_args.overwrite,
                normalize=known_args.normalize,
                dry_run=known_args.dry_run,
            )


if __name__ == "__main__":
    main()
