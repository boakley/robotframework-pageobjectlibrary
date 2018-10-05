*** Settings ***
| Documentation | Verify that the demo works as expected
| Library       | Process
| Variables     | resources/config.py

*** Variables ***
| ${BROWSER} | chrome

*** Test Cases ***
| Verify the demo works without error
| | [Documentation]
| | ... | Verify that the demo runs and completes with no errors
| | ${result}= | Run process | robot | --outputdir | ${OUTPUT_DIR}/demo_results | demo | cwd=${CONFIG.repo_root}
| | Set suite metadata | Status code | ${result.rc}
| | Set suite metadata | Demo log.html | [demo_results/log.html|demo_results/log./html]
| | run keyword if | '${result.rc}' != 0 | log | stdout: ${result.stdout}\nstderr: ${result.stderr}
| | Should be equal as integers | ${result.rc} | 0 
| | ... | expected result code to be zero but it was ${result.rc} 
| | ... | values=False
