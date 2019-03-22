import os
import sys

class Config(object):
    """Configuration for this test suite

    This creates a variable named CONFIG (${CONFIG} when included
    in a test as a variable file. It also configures PYTHONPATH
    so that the tests can find the libraries being tested.

    Example:

    *** Settings ***
    | Variable | ../resources/config.py

    *** Test Cases ***
    | Example
    | | log | username: ${CONFIG.username}
    | | log | root url: ${CONFIG.root_url}

    """

    def __init__(self):
        _here = os.path.abspath(os.path.dirname(__file__))
        _root = os.path.join(_here, "..", "..", "..")

        self.repo_root = _root
        self.demo_root = os.path.join(_root, "demo", )

        self.python = sys.executable
        self.port = 8015
        self.root_url = "http://localhost:%s" % self.port
        self.username="test user"
        self.password="password"

        # add the repository root, the test folder, and also this directory
        # to the path
        sys.path.insert(0, _root)
        sys.path.insert(0, os.path.join(_root, "tests"))
        sys.path.insert(0, os.path.join(_here))

    def __str__(self):
        return "<Config: %s>" % str(self.__dict__)
        
# This creates a variable that robot can see named ${CONFIG}
CONFIG = Config()
