from setuptools import setup

setup(
    name='files_sorter',
    version='3.0.0',
    py_modules=['files_sorter'],
    install_requires=[
        'Click', 'termcolor'
    ],
    entry_points={
        'console_scripts': [
            'files_sorter = main:file_sorter'
        ]
    }
    
)