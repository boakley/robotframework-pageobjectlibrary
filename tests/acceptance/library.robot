*** Settings ***
Library     SeleniumLibrary
Library     PageObjectLibrary
Library     Process
Variables   resources/config.py

Suite Setup      Set report metadata
Suite Teardown   Stop webapp and close all browsers

*** Variables ***
${BROWSER}    chrome

*** Keywords ***
Set report metadata
    ${selib version}=    evaluate    SeleniumLibrary.__version__    SeleniumLibrary
    ${polib version}=    evaluate    PageObjectLibrary.__version__   PageObjectLibrary
    Set suite metadata   SeleniumLibrary     version ${selib version}    append=True    top=True
    Set suite metadata   PageObjectLibrary   version ${polib version}    append=True    top=True
    
Start webapp and open browser
    start process    ${CONFIG.python}    ${CONFIG.demo_root}/webapp/demoserver.py
    open browser     ${CONFIG.root_url}  ${BROWSER}

Stop webapp and close all browsers
    Terminate all processes
    Close all browsers

*** Test Cases ***
Library is importable
    import library    PageObjectLibrary
