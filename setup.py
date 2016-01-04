from setuptools import setup, find_packages

from AnimeNFO.version import HOME_PAGE, __version__

setup(
    name='AnimeNFO',
    description='AnimeNFO Radio Notifier',
    author='Paul Traylor',
    url=HOME_PAGE,
    version=__version__,
    packages=find_packages(exclude=['test']),
    install_requires=[
        'BeautifulSoup4',
        'lxml',
        'requests',
    ],
    extras_require={
        'extras': [
            'clint',
            'gntp',
            'pillow',
        ]},
    entry_points={
        'console_scripts': {
            'radio = AnimeNFO.cli:simple',
            'radio-upcoming = AnimeNFO.cli:upcoming',
            'radio-growl = AnimeNFO.cli:main [extras]',
        }
    }
)
