import logging
from datetime import datetime

class Logger:
    @staticmethod
    def setup():
        logging.basicConfig(
            filename=f'logs/cms_{datetime.now().strftime("%Y%m%d")}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    @staticmethod
    def info(message):
        logging.info(message)

    @staticmethod
    def error(message, exc=None):
        if exc:
            logging.error(f"{message}: {str(exc)}")
        else:
            logging.error(message)
