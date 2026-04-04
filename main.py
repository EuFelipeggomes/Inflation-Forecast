import logging

import config
from src.data_loader import data_loader
from src.preprocessing import clean_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(message)s")
log = logging.getLogger(__name__)


def main():
    log.info("Iniciando pipeline...")

    rawData = data_loader()

    data = clean_data(rawData)

if __name__ == "__main__":
    main()