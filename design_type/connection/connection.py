
from utils.common.load import Load
from main import Main
import logging
class OurLog(logging.Handler):

    def __init__(self, key):
        logging.Handler.__init__(self)
        self.key = key
        # self.key.setText("INDIA")

    def handle(self, record):
        msg = self.format(record)
        self.key.append(msg)

class Connection(Main):
    def set_osdaglogger(key):
        global logger
        logger = logging.getLogger('osdag')

        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = logging.FileHandler('logging_text.log')

        handler.setLevel(logging.WARNING)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = OurLog(key)
        handler.setLevel(logging.WARNING)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)



if __name__ == "__main__":
    connection = Connection()
    connection.test()
    connection.design()
