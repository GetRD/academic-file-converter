import glob
import json
import os
import re
from datetime import datetime
from pathlib import Path

import nbconvert as nbc
import nbformat as nbf
import yaml
from traitlets.config import Config

from academic.jupyter_whitespace_remover import JupyterWhitespaceRemover


def _get_slug(text: str) -> str:
    return text.lower().replace(" ", "-")


def import_notebook(
    input_path,
    output_dir=os.path.join("content", "post"),
    overwrite=False,
    dry_run=False,
):
    """Import blog posts from Jupyter Notebook files"""
    from academic.cli import log

    log.info(f"Searching for Jupyter notebooks in `{input_path}`")
    for filename in glob.glob(input_path, recursive=True):
        if not (filename.endswith(".ipynb") and os.path.basename(filename) != ".ipynb_checkpoints"):
            continue

        log.debug(f"Found notebook `{filename}`")

        # Read Notebook
        nb = nbf.read(open(filename, "r"), as_version=4)

        # Export Markdown
        nbc_config = Config()
        nbc_config.MarkdownExporter.preprocessors = [JupyterWhitespaceRemover]
        exporter = nbc.MarkdownExporter(config=nbc_config)
        if not dry_run:
            _export(nb, exporter, output_dir, filename, ".md", overwrite)


def _export(nb, exporter, output_dir, filename, extension, overwrite):
    from academic.cli import log

    # Determine output path for page bundle
    filename_base = Path(filename).stem
    slug = _get_slug(filename_base)
    page_bundle_path = Path(output_dir) / slug

    # Do not overwrite blog post if it already exists
    if not overwrite and os.path.isdir(page_bundle_path):
        log.debug(f"Skipping creation of `{page_bundle_path}` as it already exists. To overwrite, add the `--overwrite` argument.")
        return

    log.info(f"Importing notebook `{filename}`")

    # Create page bundle folder
    if not os.path.exists(page_bundle_path):
        os.makedirs(page_bundle_path)

    # Check for front matter variables in notebook metadata
    if "front_matter" in nb["metadata"]:
        front_matter_from_file = dict(nb["metadata"]["front_matter"])
        log.info(f"Found front matter metadata in notebook: {json.dumps(front_matter_from_file)}")
    else:
        front_matter_from_file = {}

    # Convert notebook to markdown
    (body, resources) = exporter.from_notebook_node(nb)

    # Export notebook resources
    for name, data in resources.get("outputs", {}).items():
        output_filename = Path(page_bundle_path) / name
        with open(output_filename, "wb") as image_file:
            image_file.write(data)

    # Try to find title as top-level heading (h1), falling back to filename
    search = re.search("^#{1}(.*)", body)
    if search:
        title = search.group(1).strip()
        # Remove the h1 heading as static site generators expect the title to be defined via front matter instead.
        body = re.sub("^#{1}(.*)", "", body)
    else:
        # Fallback to using filename as title
        # Apply transformation as expect *nix-style file naming with hyphens/underscores separating words rather than spaces.
        title = filename_base.replace("-", " ").replace("_", " ").title()

    # Initialise front matter variables
    date = datetime.now().strftime("%Y-%m-%d")
    front_matter = {"title": title, "date": date}
    front_matter.update(front_matter_from_file)
    log.info(f"Generating page with title: {front_matter['title']}")

    # Unlike the Bibtex converter, we can't easily use Ruamel YAML library here as we need to output to string
    front_matter_yaml = yaml.safe_dump(front_matter, sort_keys=False, allow_unicode=True)
    # Strip final newline as our `output` will auto-add newlines below
    front_matter_yaml = front_matter_yaml.rstrip()
    # Wrap front matter variables with triple hyphens to represent Markdown front matter
    output = "\n".join(("---", front_matter_yaml, "---", clean_markdown(body)))

    # Write output file
    output_filename = os.path.join(page_bundle_path, "index" + extension)
    with open(output_filename, "w") as text_file:
        text_file.write(output)


def clean_markdown(body: str) -> str:
    """
    `nbconvert` creates too much whitespace and newlines.
    Try to tidy up the output by removing multiple new lines.
    """
    return re.sub(r"\n+(?=\n)", "\n", body)
