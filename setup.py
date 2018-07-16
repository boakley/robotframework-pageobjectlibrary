# N.B. to push a new version to PyPi, update the version number
# in rfhub/version.py and then run 'python setup.py sdist upload'
import sys

from setuptools import setup

from .version import __version__

exec(compile(open('PageObjectLibrary/version.py').read()))

setup(
    name='robotframework-pageobjectlibrary',
    version=__version__,
    author='Bryan Oakley',
    author_email='bryan.oakley@gmail.com',
    url='https://github.com/boakley/robotframework-pageobjectlibrary/',
    keywords='robotframework',
    license='Apache License 2.0',
    description='RobotFramework library that implements the Page Object pattern',
    long_description=open('README.md', encoding='latin-1').read(),
    zip_safe=True,
    include_package_data=True,
    install_requires=['robotframework', 'robotframework-seleniumlibrary', 'selenium', 'six'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Framework :: Robot Framework",
        "Programming Language :: Python",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "Intended Audience :: Developers",
        ],
    packages=[
        'PageObjectLibrary',
    ],
    scripts=[],
)
