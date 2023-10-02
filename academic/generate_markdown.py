from pathlib import Path

import ruamel.yaml


class GenerateMarkdown:
    """
    Load a Markdown file, enable its YAML front matter to be edited (currently, directly via `self.yaml[...]`), and then save it.
    """

    def __init__(self, base_path: Path, delim: str = "---", dry_run: bool = False, compact: bool = False):
        """
        Initialise the class.

        Args:
            base_path: the folder to save the Markdown file to
            delim: the front matter delimiter, i.e. `---` for YAML front matter
            dry_run: whether to actually save the output to file
            compact: whether to strip comments, line breaks, and empty keys from the generated Markdown
        """
        self.base_path = base_path
        if delim != "---":
            raise NotImplementedError("Currently, YAML is the only supported front-matter format.")
        self.delim = delim
        self.yaml = {}
        self.content = []
        self.path = ""
        self.dry_run = dry_run
        self.compact = compact
        # We use Ruamel's default round-trip loading to preserve key order and comments, rather than `YAML(typ='safe')`
        self.yaml_parser = ruamel.yaml.YAML()

    def load(self, file: Path):
        """
        Load the Markdown file to edit.

        Args:
            file: the Markdown filename to load. By default, it will be a copy of the Markdown template file saved to the output folder.

        Returns: n/a - directly saves output to `self.yaml`

        """
        front_matter_text = []
        self.yaml = {}
        self.content = []
        self.path = self.base_path / file
        if self.dry_run and not self.path.exists():
            self.yaml = dict()
            return

        with self.path.open("r", encoding="utf-8") as f:
            lines = f.readlines()

        # Detect both the YAML front matter and the Markdown content in the template
        delims_seen = 0
        for line in lines:
            if line.startswith(self.delim):
                delims_seen += 1
            else:
                if delims_seen < 2:
                    front_matter_text.append(line)
                # In Compact mode, we don't add any placeholder content to the page
                elif not self.compact:
                    # Append any Markdown content from the template body (after the YAML front matter)
                    self.content.append(line)

        # Parse YAML, trying to preserve key order, comments, and whitespace
        self.yaml = self.yaml_parser.load("".join(front_matter_text))

    def recursive_delete_comment_attribs(self, d):
        """
        Delete comments from the YAML template for Compact mode

        Args:
            d: the named attribute to delete from the YAML dict
        """
        if isinstance(d, dict):
            for k, v in d.items():
                self.recursive_delete_comment_attribs(k)
                self.recursive_delete_comment_attribs(v)
        elif isinstance(d, list):
            for elem in d:
                self.recursive_delete_comment_attribs(elem)
        try:
            # literal scalarstring might have comment associated with them
            attr = "comment" if isinstance(d, ruamel.yaml.scalarstring.ScalarString) else ruamel.yaml.comments.Comment.attrib  # type: ignore
            delattr(d, attr)
        except AttributeError:
            pass

    def dump(self):
        """
        Save the generated markdown to file.
        """
        assert self.path, "You need to `.load()` first."
        if self.dry_run:
            return

        with open(self.path, "w", encoding="utf-8") as f:
            f.write("{}\n".format(self.delim))
            if self.compact:
                # For compact output, strip comments, new lines, and empty keys
                # Strip `image` key in Compact mode as it cannot currently be set via Bibtex, it's just set in template.
                # Note: a better implementation may be just to start with a different template for Compact mode,
                # rather than remove items from the detailed template.
                self.recursive_delete_comment_attribs(self.yaml)
                elems_to_delete = []
                for elem in self.yaml:
                    if (
                        self.yaml[elem] is None
                        or self.yaml[elem] == ""
                        or self.yaml[elem] == []
                        or (elem == "featured" and self.yaml[elem] is False)
                        or (elem == "image")
                    ):
                        elems_to_delete.append(elem)
                for elem in elems_to_delete:
                    del self.yaml[elem]
                del elems_to_delete
            self.yaml_parser.dump(self.yaml, f)
            f.write("{}\n".format(self.delim))
            f.writelines(self.content)
