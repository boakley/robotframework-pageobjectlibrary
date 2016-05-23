PageObjectLibrary
=================

Overview
--------

PageObjectLibrary is a lightweight `robot
framework <http://www.robotframework.org>`__ keyword library that makes
it possible to use the page object pattern when testing web pages with
the keyword based approach of robot framework.

Installing
----------

::

    $ pip install --upgrade robotframework-pageobjectlibrary

Source code
-----------

The source code is hosted on github at the following url:

::

    [https://github.com/boakley/robotframework-pageobjectlibrary.git]

Running the demo
----------------

In the github repository is a small demonstration suite that includes a
self-contained webserver and web site.

For the demo to run you must have robotframework 2.9+ and
Selenium2Library installed. You must also have cloned the github
repository to have access to the demo files.

To run the demo, clone the github repository, cd to the folder that
contains this file, and then run the following command:
::

    $ robot -d demo/results demo

A simple tutorial
----------------

For a simple tutorial, see https://github.com/boakley/robotframework-pageobjectlibrary/wiki/Tutorial

How it works
------------

The page object library is quite simple. Page object classes are
implemented as standard robot keyword libraries, and relies on robot
frameworks built-in `Set library search order keyword
<http://robotframework.org/robotframework/latest/libraries/BuiltIn.html#Set%20Library%20Search%20Order>`_.

The core concept is that when you use PageObjectLibrary keywords to go
to a page or assert you are on a specific page, the keyword will
automatically load the library for that page and put it at the front of
the library search order, guaranteeing that the page object keywords are
available to your test case.

Why page objects makes writing tests easier
-------------------------------------------

The purpose of the page object pattern is to encapsulate the knowledge
of how a web page is constructed into an object. Your test uses the
object as an interface to the application, isolating your test cases
from the details of the implementation of a page.

With page objects, developers are free to modify web pages as much as
they want, and the only thing they need to do to keep existing tests
from failing is to update the page object class. Because test cases
aren't directly tied to the implementation, they become more stable and
more resistent to change as the website matures.

A typical test without page objects
-----------------------------------

With traditional testing using Selenium, a simple login test might look
something like the following: (using the pipe-separated format for
clarity):

::

    *** Test Cases ***
    | Login with valid credentials
    | | Go to | ${ROOT}/Login.html
    | | Wait for page to contain | id=id_username
    | | Input text | id=id_username | ${USERNAME}
    | | Input text | id=id_password | ${PASSWORD}
    | | Click button | id=id_form_submit
    | | Wait for page to contain | Your Dashboard
    | | Location should be | ${ROOT}/dashboard.html

Notice how this test is tightly coupled to the implementation of the
page. It has to know that the input field has an id of "id\_username",
and the password field has an id of "id\_password". It also has to know
the URL of the page being tested.

Of course, you can put those hard-coded values into variables and import
them from a resource file or environment variables, which makes it
easier to update tests when locators change. However, there's still the
overhead of additional keywords that are often required to make a test
robust, such as waiting for a page to be reloaded. The provided
PageObject superclass handles some of those details for you.

The same test, using page objects
---------------------------------

Using page objects, the same test could be written like this:

::

    *** Test Cases ***
    | Login with valid credentials
    | | Go to page | LoginPage
    | | Login as a normal user
    | | The current page should be | DashboardPage

Notice how there are no URLs or element locators in the test whatsoever,
and that we've been able to eliminate some keywords that typically are
necessary for selenium to work but which aren't part of the test logic
*per se*. What we end up with is test case that is nearly
indistinguishable from typical acceptance criteria of an agile story.

Writing a Page Object class
===========================

Page objects are simple python classes that inherit from
``PageObjectLibrary.PageObject``. There are only a couple of
requirements for the class:

-  The class should define a variable named PAGE\_TITLE
-  The class should define a variable named PAGE\_URL which is a URI
   relative to the site root.

By inheriting from ``PageObjectLibrary.PageObject``, methods have access
to the folloing special object attributes:

-  ``self.se2lib`` - a reference to an instance of Selenium2Library.
   With this you can call any of the Selenium2Library keywords via their
   python method names (eg: self.se2lib.input\_text)
-  ``self.browser`` - a reference to the webdriver object created when a
   browser was opened by Selenium2Library. With this you can bypass
   Selenium2Library and directly call all of the functions provided by
   the core selenium library.
-  ``self.locator`` - a wrapper around the ``_locators`` dictionary of
   the page. This dictionary can contain all of the locators used by the
   page object keywords. ``self.locators`` adds the ability to access
   the locators with dot notation rather than the slightly more verbose
   dictionary syntax (eg: ``self.locator.username`` vs
   ``self._locators["username"]``.

An example page object
----------------------

A page object representing a login page might look like this:

::

    from PageObjectLibrary import PageObject

    class LoginPage(PageObject):
        PAGE_TITLE = "Login - PageObjectLibrary Demo"
        PAGE_URL = "/login.html"

        _locators = {
            "username": "id=id_username",
            "password": "id=id_password",
            "submit_button": "id=id_submit",
        }

        def enter_username(self, username):
            """Enter the given string into the username field"""
            self.se2lib.input_text(self.locator.username, username)

        def enter_password(self,password):
            """Enter the given string into the password field"""
            self.se2lib.input_text(self.locator.password, password)

        def click_the_submit_button(self):
            """Click the submit button, and wait for the page to reload"""
            with self._wait_for_page_refresh():
                self.se2lib.click_button(self.locator.submit_button)
