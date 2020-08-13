import os
import re
import shutil
import sys

from setuptools import find_packages, setup


def get_version(package):
    """Return package version as listed in `__version__` in `init.py`."""
    version_py = open(os.path.join(package, "version.py")).read()
    return re.search("version = ['\"]([^'\"]+)['\"]", version_py).group(1)


version = get_version("academic")
requirements = ["ruamel.yaml==0.16.10", "toml", "requests", "bibtexparser==1.1.0"]

if sys.argv[-1] == "publish":
    if os.system("pip3 freeze --all | grep wheel"):
        print("wheel not installed.\nUse `pip install wheel`.\nExiting.")
        sys.exit()
    if os.system("pip3 freeze --all | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python3 setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    print("You probably want to also tag the version now:")
    print("  git tag -a {0} -m 'version {0}'".format(version))
    print("  git push --tags")
    shutil.rmtree("dist")
    shutil.rmtree("build")
    shutil.rmtree("academic.egg-info")
    sys.exit()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="academic",
    version=version,
    author="George Cushen",
    author_email="hugo-discuss@googlegroups.com",
    url="https://sourcethemes.com/academic/",
    description="The website designer for Hugo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=("cli academic hugo theme static-site-generator cms blog-engine" "github-pages netlify hugo-theme documentation-generator"),
    include_package_data=True,
    license="MIT",
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points="""
        [console_scripts]
        academic=academic.cli:main
    """,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
