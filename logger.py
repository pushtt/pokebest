import logging
import sys
from datetime import datetime

stdout_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("./log/pokemon_{}".format(datetime.now().strftime("%Y-%m-%d")), mode="a")

def init_logger(name:str, level=logging.INFO) -> logging.Logger:
    logging.basicConfig(
            level=level,
            format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[stdout_handler, file_handler]
            )
    return logging.getLogger(name)




