import logging
import os
import sys
import time
from datetime import datetime
from selenium.common.exceptions import WebDriverException, NoSuchElementException

from driver.driver import Driver
from iterator.iteration import Interation
from ext.function import setup_logging

class Bot(Interation):
    """Classe que define um bot para interação automatizada com páginas da web."""

    def __init__(self, log_file=True):
        """
        Inicializa um objeto Bot.

        Args:
            log_file (bool): Define se os registros serão salvos em um arquivo de log (padrão: True).
        """
        logger = setup_logging(to_file=True)
        
        self.driver = Driver(
            browser='chrome',
            headless=False,
            incognito=False,
            download_path='',
            desabilitar_carregamento_imagem=False
        ).driver

        super().__init__(self.driver)

