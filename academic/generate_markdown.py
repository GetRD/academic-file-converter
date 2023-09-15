from pathlib import Path

from ruamel.yaml import YAML

yaml = YAML()


class EditableFM:
    def __init__(self, base_path: Path, delim: str = "---", dry_run: bool = False):
        self.base_path = base_path
        if delim != "---":
            raise NotImplementedError("Currently, YAML is the only supported front-matter format.")
        self.delim = delim
        self.fm = []
        self.content = []
        self.path = ""
        self.dry_run = dry_run

    def load(self, file: Path):
        self.fm = []
        self.content = []
        self.path = self.base_path / file
        if self.dry_run and not self.path.exists():
            self.fm = dict()
            return

        with self.path.open("r", encoding="utf-8") as f:
            lines = f.readlines()

        delims_seen = 0
        for line in lines:
            if line.startswith(self.delim):
                delims_seen += 1
            else:
                if delims_seen < 2:
                    self.fm.append(line)
                else:
                    self.content.append(line)

        # Parse YAML, trying to preserve comments and whitespace
        self.fm = yaml.load("".join(self.fm))

    def dump(self):
        assert self.path, "You need to `.load()` first."
        if self.dry_run:
            return

        with open(self.path, "w", encoding="utf-8") as f:
            f.write("{}\n".format(self.delim))
            yaml.dump(self.fm, f)
            f.write("{}\n".format(self.delim))
            f.writelines(self.content)
