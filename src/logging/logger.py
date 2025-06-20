import logging 
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%d_%m_%Y')}.log"

logs_path = os.path.join(os.getcwd(), "logs")
if not os.path.exists(os.path.dirname(logs_path)):
    os.makedirs(os.path.dirname(logs_path))

LOG_FILE_PATH = os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format='[%(asctime)s] %(filename)s - %(lineno)d %(name)s- %(levelname)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    filemode='a'
)