import logging 
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%d_%m_%Y')}.log"

logs_path = os.path.join(os.getcwd(), "logs")
if not os.path.exists(os.path.dirname(logs_path)):
    os.makedirs(os.path.dirname(logs_path))

LOG_FILE_PATH = os.path.join(logs_path,LOG_FILE)

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(filename)s - %(lineno)d %(name)s - %(levelname)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S'))

# Console handler (this is what was missing)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(
    '%(levelname)s - %(message)s'))

# Add handlers (avoid duplicates if rerun)
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


'''

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format='[%(asctime)s] %(filename)s - %(lineno)d %(name)s- %(levelname)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    filemode='a'
)
'''