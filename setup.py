import os
import codecs
from setuptools import setup, find_packages


NAME = 'pytj'
PACKAGES = find_packages()
META_PATH = os.path.join("lib/pytj", "__init__.py")
KEYWORDS = ['task', 'juggler', 'project', 'management']
CLASSIFIERS = ["Programming Language :: Python",
               "Programming Language :: Python :: 2",
               "Programming Language :: Python :: 2.6",
               "Programming Language :: Python :: 2.7",
               "Programming Language :: Python :: 3",
               "Programming Language :: Python :: 3.0",
               "Programming Language :: Python :: 3.1",
               "Programming Language :: Python :: 3.2",
               "Programming Language :: Python :: 3.3",
               "Programming Language :: Python :: 3.4",
               "Programming Language :: Python :: 3.5",
               "Programming Language :: Python :: 3.6",
               "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
               "Operating System :: OS Independent",
               "Development Status :: 5 - Production/Stable",
               "Intended Audience :: Developers",
               "Intended Audience :: End Users/Desktop",
               "Topic :: Database", "Topic :: Software Development",
               "Topic :: Utilities",
               "Topic :: Office/Business :: Scheduling", ]
INSTALL_REQUIRES = [
    'pytz', 'tzlocal',
]
TEST_REQUIRES = ['pytest', 'pytest-xdist', 'pytest-cov', 'coverage']
DATA_FILES = [(
    '',
    ['COPYING', 'COPYING.LESSER', 'INSTALL', 'MANIFEST.in', 'README.rst']),
]

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


README = read(HERE, 'README.rst')
CHANGES = open(os.path.join(HERE, 'CHANGELOG.rst')).read()
META_FILE = read(META_PATH)


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    import re
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta),
        META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


if __name__ == '__main__':
    setup(
        name=NAME,
        description=find_meta('description'),
        long_description=README,
        license=find_meta('license'),
        url=find_meta("uri"),
        version=find_meta('version'),
        author=find_meta('author'),
        author_email=find_meta('email'),
        classifiers=CLASSIFIERS,
        keywords=KEYWORDS,
        packages=PACKAGES,
        include_package_data=True,
        data_files=DATA_FILES,
        zip_safe=True,
        test_suite='pytj',
        install_requires=INSTALL_REQUIRES,
        test_requires=TEST_REQUIRES
    )

