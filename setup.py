import os
import sys
import re
import shutil
from setuptools import setup, find_packages


def get_version(package):
    """Return package version as listed in `__version__` in `init.py`."""
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('academic')

if sys.argv[-1] == 'publish':
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
    shutil.rmtree('dist')
    shutil.rmtree('build')
    shutil.rmtree('academic.egg-info')
    sys.exit()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='academic',
    version=version,
    author='George Cushen',
    author_email='hugo-discuss@googlegroups.com',
    url='https://sourcethemes.com/academic/',
    description='The website designer for Hugo',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='cli academic hugo theme static-site-generator cms blog-engine github-pages netlify hugo-theme documentation-generator',
    include_package_data=True,
    license='MIT',
    packages=find_packages(),
    install_requires=['toml', 'requests', 'bibtexparser'],
    entry_points="""
        [console_scripts]
        academic=academic.cli:main
    """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
