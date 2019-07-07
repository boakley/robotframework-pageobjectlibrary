from io import open
from setuptools import setup

exec(open('PageObjectLibrary/version.py').read())

setup(
    name             = 'robotframework-pageobjectlibrary',
    version          = __version__,
    author           = 'Bryan Oakley',
    author_email     = 'bryan.oakley@gmail.com',
    url              = 'https://github.com/boakley/robotframework-pageobjectlibrary/',
    keywords         = 'robotframework',
    license          = 'Apache License 2.0',
    description      = 'RobotFramework library that implements the Page Object pattern',
    long_description = open('README.md', encoding='latin-1').read(),
    zip_safe         = True,
    include_package_data=True,
    install_requires = ['robotframework', 'robotframework-seleniumlibrary', 'selenium', 'six'],
    classifiers      = [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Framework :: Robot Framework",
        "Programming Language :: Python",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "Intended Audience :: Developers",
        ],
    packages         = [
        'PageObjectLibrary',
    ],
    scripts          = [],
)
