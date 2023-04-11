from setuptools import setup, find_packages
from imod2relion.__init__ import __version__, __author__, __email__

setup(
    name = 'imod2relion',
    packages = find_packages(),
    version=f'{__version__}',
    license='BSD 3-Clause License',
    description='''A tool reading IMOD points, obtaining particles' info and generating .star file for RELION''',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author=f'{__author__}',
    author_email=f'{__email__}',
    url='https://github.com/ZhenHuangLab/imod2relion',
    keywords=['cryo-em', 'cryo-et', 'imod', 'relion', 'starfile'],
    python_requires='>=3.9',
    install_requires=[
        'starfile>=0.4.11',
        'numpy>=1.24.2',
        'pandas>=1.5.3'
    ],
    entry_points={
        'console_scripts': [
            'imod2relion = imod2relion.main:main'
        ]
    },
    exclude_package_data={
    '':['*.txt']
    }
)
