import logging
import os
import tempfile
from pathlib import Path
from urllib.parse import urlparse

import toml
from requests import get

JS_FILENAME = "static/js/vendor/main.min.js"
CSS_FILENAME = "static/css/vendor/main.min.css"

log = logging.getLogger(__name__)


def import_assets():
    """Download and import third-party JS and CSS assets to enable offline sites"""

    # Check that we are in an Academic website folder.
    if not Path("content").is_dir():
        log.error("Please navigate to your website folder and re-run.")
        return

    # Check compatibility with user's Academic version (v2.4.0+ required for local asset bundling)
    # `academic.toml` was added in Academic v2.4.0, so can simply check for the existence of that file.
    academic_filename = "themes/academic/data/academic.toml"
    if not Path(academic_filename).is_file():
        log.error(
            "Could not detect Academic version in `themes/academic/data/academic.toml`. " "You may need to update Academic in order to use this tool."
        )
        return

    # Check assets file exists
    # Note that the order of assets in `assets.toml` matters since they will be concatenated in the order they appear.
    assets_filename = "themes/academic/data/assets.toml"
    if not Path(assets_filename).is_file():
        log.error("Could not detect assets file. You may need to update Academic in order to use this tool.")
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
        for i, j in parsed_toml["js"].items():
            url = j["url"].replace("%s", j["version"], 1)  # Replace placeholder with asset version.
            filename = os.path.basename(urlparse(url).path)
            filepath = os.path.join(d, filename)
            js_files.append(filepath)

            log.info(f"Downloading {filename} from {url}...")
            download_file(url, filepath)

        log.info(f"Merging JS assets into {JS_FILENAME}")
        merge_files(js_files, JS_FILENAME)

        # Parse CSS assets
        css_files = []
        for i, j in parsed_toml["css"].items():
            url = j["url"].replace("%s", j["version"], 1)  # Replace placeholder with asset version.

            # Special case for highlight.js style
            if i == "highlight":
                # Assume user is using a light theme.
                # TODO: Set to .Site.Params.highlight_style if set, or dracula if using a dark theme.
                hl_theme = "github"
                url = url.replace("%s", hl_theme)  # Replace the second placeholder with style name.
            filename = os.path.basename(urlparse(url).path)
            filepath = os.path.join(d, filename)
            css_files.append(filepath)

            log.info(f"Downloading {filename} from {url}...")
            download_file(url, filepath)

        log.info(f"Merging CSS assets into {CSS_FILENAME}")
        merge_files(css_files, CSS_FILENAME)


def download_file(url, file_name):
    """Download file from URL"""
    with open(file_name, "wb") as file:
        # Get file at URL.
        response = get(url)

        # Check that we can access the specified URL OK.
        if response.status_code != 200:
            log.error(f"Could not download {url}")
            return

        # Write to file.
        file.write(response.content)


def merge_files(file_path_list, destination):
    """Merge multiple files into one file"""
    with open(destination, "w", encoding="utf-8") as f:
        for file_path in file_path_list:
            with open(file_path, "r", encoding="utf-8") as source_file:
                f.write(source_file.read() + "\n")
