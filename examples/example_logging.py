# This is a simple example of how to use the logging module in Python with output to the console and a log file. 

import logging
import sys

logger = logging.getLogger(__name__)

# Create a logger
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
logger.setLevel(logging.DEBUG)  # Set the desired logging level

# Create a StreamHandler for stdout
handler = logging.StreamHandler(sys.stdout)

# Create a formatter and set it for the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

# Example log messages
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")