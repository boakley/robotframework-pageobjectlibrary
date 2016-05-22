from __future__ import absolute_import, unicode_literals
import robot.api
from robot.libraries.BuiltIn import BuiltIn
from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
from abc import ABCMeta
import six

from .locatormap import LocatorMap

class PageObject(six.with_metaclass(ABCMeta, object)):
    """Base class for page objects

    Classes that inherit from this class need to define the
    following class variables:

    PAGE_TITLE   the title of the page; used by the default 
                 implementation of _is_current_page
    PAGE_URL     this should be the URL of the page, minus
                 the hostname and port (eg: /loginpage.html)

    By default, the PageObjectLibrary keyword 'the current page should
    be' calls the method _is_current_page. A default implementation is
    provided by this class. It compares the current page title to the
    class variable PAGE_TITLE. A class can override this method if the
    page title is not unique or is indeterminate.
    
    Classes that inherit from this class have access to the
    following properties:

    * se2lib    a reference to an instance of Selenium2Library
    * browser   a reference to the current webdriver instance
    * logger    a reference to robot.api.logger
    * locator   a wrapper around the page object's ``_locators`` dictionary 

    This class implements the following context managers:

    * _wait_for_page_refresh  

    This context manager is designed to be used in page objects when a
    keyword should wait to return until the html element has been
    refreshed.

    """

    PAGE_URL = None
    PAGE_TITLE = None

    def __init__(self):
        self.logger = robot.api.logger
        self.locator = LocatorMap(getattr(self, "_locators", {}))

    # N.B. se2lib, browser use @property so that a
    # subclass can be instantiated outside of the context of a running
    # test (eg: by libdoc, robotframework-hub, etc)
    @property
    def se2lib(self):
        return BuiltIn().get_library_instance("Selenium2Library")

    @property
    def browser(self):
        return self.se2lib._current_browser()

    def __str__(self):
        return self.__class__.__name__

    def get_page_name(self):
        """Return the name of the current page """
        return self.__class__.__name__

    @contextmanager
    def _wait_for_page_refresh(self, timeout=10):
        """Context manager that waits for a page transition.

        This keyword works by waiting for two things to happen:

        1) the <html> tag to go stale and get replaced, and
        2) the javascript document.readyState variable to be set
           to "complete"
        """
        old_page = self.browser.find_element_by_tag_name('html')
        yield
        WebDriverWait(self.browser, timeout).until(
            staleness_of(old_page)
        )
        self.se2lib.wait_for_condition("return (document.readyState == 'complete')", timeout=10)

    def _is_current_page(self):
        """Determine if this page object represents the current page.

        This works by comparing the current page title to the class
        variable PAGE_TITLE.

        Unless their page titles are unique, page objects should
        override this function. For example, a common solution is to
        look at the url of the current page, or to look for a specific
        heading or element on the page.

        """

        actual_title = self.se2lib.get_title()
        expected_title = self.PAGE_TITLE

        if actual_title.lower() == expected_title.lower():
            return True

        self.logger.info("expected title: '%s'" % expected_title)
        self.logger.info("  actual title: '%s'" % actual_title)
        raise Exception("expected title to be '%s' but it was '%s'" % (expected_title, actual_title))
        return False

