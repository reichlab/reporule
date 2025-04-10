"""Command line interface entrypoint for the Reichlab package."""

from reichlab.logging import setup_logging
from reichlab.main import main

# Set up logging
setup_logging()

if __name__ == "__main__":
    main()
