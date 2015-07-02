from setuptools import setup
from AnimeNFO.version import __version__, HOME_PAGE

setup(
    name='AnimeNFO',
    description='AnimeNFO Radio Notifier',
    author='Paul Traylor',
    url=HOME_PAGE,
    version=__version__,
    packages=['AnimeNFO', 'AnimeNFO.cli'],
    install_requires=['BeautifulSoup4', 'requests'],
    extras_require={'extras': ['gntp', 'clint', 'pillow']},
    entry_points={
        'console_scripts': {
            'radio = AnimeNFO.cli:simple',
            'radio-upcoming = AnimeNFO.cli:upcoming',
            'radio-growl = AnimeNFO.cli:main [extras]',
        }
    }
)
