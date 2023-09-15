import tomllib

with open("pyproject.toml", "rb") as f:
    _META = tomllib.load(f)

NAME = _META["tool"]["poetry"]["name"]
VERSION = _META["tool"]["poetry"]["version"]
DESCRIPTION = _META["tool"]["poetry"]["description"]
