*** Settings ***
| Documentation | Show the browser "about:" page, for debugging purposes
| Library       | SeleniumLibrary

*** Variables ***
| ${BROWSER} | chrome

*** Test Cases ***
| The browser 'about:' page
| | [Documentation]
| | ... | Displays the browser's 'about:' page
| | 
| | [Setup]     | open browser  | about:  | ${BROWSER}
| | capture page screenshot
| | [Teardown]  | close browser
