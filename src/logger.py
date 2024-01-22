import logging
import os


logging.basicConfig(level=logging.WARNING,  # Set higher level for root logger
    format='=> %(levelname)s - %(module)s - %(asctime)s - %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),  # Logs to the console
    ])

logger = logging.getLogger("Analysis")
logger.setLevel(logging.DEBUG)  # Set DEBUG level for MarketResearch logger
