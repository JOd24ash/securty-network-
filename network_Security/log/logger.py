import logging
import os
from datetime import datetime

LOG_file=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
loge_path=os.path.join(os.getcwd(),'logs',LOG_file)
os.makedirs(loge_path,exist_ok=True)

LOG_FILE_PATH=os.path.join(loge_path,LOG_file)

logging.basicConfig(filename=LOG_FILE_PATH,
                    format="[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d] - %(message)s",
                    level=logging.INFO)