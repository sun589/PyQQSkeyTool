from setuptools import setup, find_packages
from PyQQSkeyTool.constant import AUTHOR,VERSION,EMAIL

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PyQQSkeyTool',
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description=long_description,
    url='https://github.com/sun589/PyQQSkeyTool',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'requests>=2.25.1',
        'urlextract>=1.6.0'
    ],
    python_requires='>=3.6'
)
