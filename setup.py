# try using distribute or setuptools or distutils.
try:
    import distribute_setup
    distribute_setup.use_setuptools()
except:
    pass

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


import sys
import re

# parse version from package/module without importing or evaluating the code
with open('labbook/__init__.py') as fh:
    for line in fh:
        m = re.search(r"^__version__ = '(?P<version>[^']+)'$", line)
        if m:
            version = m.group('version')
            break

if sys.version_info <= (3, 6):
    sys.stderr.write("ERROR: labbook requires Python3.6 (exiting)\n")
    sys.exit(1)

setup(
    name="labbook",
    version=version,
    author="Leighton Pritchard",
    author_email="leighton.pritchard@hutton.ac.uk",
    description="labbook is a module providing tools for managing an" +
    "electronic laboratory notebook.",
    license="MIT",
    keywords="science notebook enotebook laboratory",
    platforms="Posix; MacOS X",
    url="https://github.com/widdowquinn/labbook",
    download_url="https://github.com/widdowquinn/labbook/releases",
    scripts=['mylabbook.py'],
    packages=['labbook'],
    install_requires=[],
    package_data={},
    data_files=[('templates', ['templates/preflight_tuftenotebook.tex'])],
    classifiers=[],
    )
