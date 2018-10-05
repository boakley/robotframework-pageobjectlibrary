To run a short demo, run the following command from the same directory
as this file:

    $ robot demo

To run acceptance tests (which includes running the demo), run the following
command in same directory as this file:

    $ robot -A tests/config.args tests


By default the tests will run with chrome, but you can change to any
browser supported by your system by setting the variable BROWSER
from the command line.

Example:

    robot --variable browser:firefox demo

