import logging

from prompt_toolkit.utils import to_int

import config
from src.data_loader import data_loader

logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(message)s")
log = logging.getLogger(__name__)


def main():
    log.info("Iniciando pipeline...")
    data_loader()

if __name__ == "__main__":
    main()