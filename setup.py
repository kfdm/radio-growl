import sys
from setuptools import setup
from AnimeNFO.version import __version__, HOME_PAGE

install_requires = ['BeautifulSoup4', 'requests']
packages = ['AnimeNFO']
console_scripts = [
    'radio = AnimeNFO.cli:simple',
    'radio-upcoming = AnimeNFO.cli:upcoming',
]

if '--extras' in sys.argv:
    sys.argv.remove('--extras')
    install_requires += ['gntp', 'clint', 'pillow']
    packages += ['AnimeNFO.cli']
    console_scripts += ['radio-growl = AnimeNFO.cli:main']


setup(
    name='AnimeNFO',
    description='AnimeNFO Radio Notifier',
    author='Paul Traylor',
    url=HOME_PAGE,
    version=__version__,
    packages=packages,
    install_requires=install_requires,
    entry_points={
        'console_scripts': console_scripts
    }
)
