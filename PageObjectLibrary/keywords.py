"""PageObjectLibrary

A library to support the creation of page objects using
selenium and Seleniuim2Library.


"""

from __future__ import print_function, absolute_import, unicode_literals
import six
import robot.api
from robot.libraries.BuiltIn import BuiltIn
from .pageobject import PageObject
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

class PageObjectLibraryKeywords(object):

    ROBOT_LIBRARY_SCOPE = "TEST SUITE"

    def __init__(self):
        self.builtin = BuiltIn()
        self.logger = robot.api.logger

    @property
    def se2lib(self):
        # this is implemented as a property so that this class
        # can be imported outside the context of a running
        # suite (ie: by libdoc, robotframework-hub, etc)
        return self.builtin.get_library_instance("Selenium2Library")

    def the_current_page_should_be(self, page_name):
        """Fails if the name of the current page is not the given page name

        page_name is the name you would use to import the page

        This keyword will import the given page object, put it at the
        front of the robot library search order, then call the method
        ``_is_current_page`` on the library. The default
        implementation of this method will compare the page title to
        the ``PAGE_TITLE`` attribute of the page object, but this
        implementation can be overridden by each page object.

        """

        page = self._get_page_object(page_name)

        # This causes robot to automatically resolve keyword
        # conflicts by looking in the current page first.
        if page._is_current_page():
            # only way to get the current order is to set a
            # new order. Once done, if there actually was an
            # old order, preserve the old but make sure our
            # page is at the front of the list
            old_order = self.builtin.set_library_search_order()
            new_order = ([str(page)],) + old_order
            self.builtin.set_library_search_order(new_order)
            return

        # If we get here, we're not on the page we think we're on
        raise Exception("Expected page to be %s but it was not" % page_name)

    def go_to_page(self, page_name, page_root = None):
        """Go to the url for the given page object

        Unless explicitly provided, the URL root will be based on the
        root of the current page. For example, if the current page is
        http://www.example.com:8080 and the page object URL is
        /login, the url will be http://www.example.com:8080/login

        Example:

        Given a page object named `ExampleLoginPage` with the URL
        `/login`, and a browser open to `http://www.example.com`, the
        following statement will go to `http://www.example.com/login`,
        and place `ExampleLoginPage` at the front of robot's library
        search order.

        | go to page    ExampleLoginPage

        The effect is the same as if you had called the following three
        keywords

        | Selenium2Library.go to      http://www.example.com/login
        | Import Library              ExampleLoginPage
        | Set library search order    ExampleLoginPage

        Tags: selenium, page-object

        """

        page = self._get_page_object(page_name)

        url = page_root if page_root is not None else self.se2lib.get_location()
        (scheme, netloc, path, parameters, query, fragment) = urlparse(url)
        url = "%s://%s%s" % (scheme, netloc, page.PAGE_URL)

        with page._wait_for_page_refresh():
            self.logger.console("\ntrying to go to '%s'" % url)
            self.se2lib.go_to(url)
        # should I be calling this keyword? Should this keyword return
        # true/false, or should it throw an exception?
        self.the_current_page_should_be(page_name)

    def _get_page_object(self, page_name):
        """Import the page object if necessary, then return the handle to the library

        Note: If the page object has already been imported, it won't be imported again.
        """

        try:
            page = self.builtin.get_library_instance(page_name)

        except RuntimeError:
            self.builtin.import_library(page_name)
            page = self.builtin.get_library_instance(page_name)

        return page

