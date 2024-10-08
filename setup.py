from setuptools import setup, find_packages

setup(
    name='PyQQSkeyTool',
    version='1.0.0',
    author='sun589',
    author_email='goodluck1787@outlook.com',
    description='一款集成了QQSkey/QQClientkey获取的库',
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
