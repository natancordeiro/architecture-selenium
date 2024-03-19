import logging
import os
import sys
import time
from datetime import datetime
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from driver.driver import Driver
from iterator.iteration import Interation

class Bot(Interation):
    """Classe que define um bot para interação automatizada com páginas da web."""

    def __init__(self, log_file=True):
        """
        Inicializa um objeto Bot.

        Args:
            log_file (bool): Define se os registros serão salvos em um arquivo de log (padrão: True).
        """
        if log_file:
            data = datetime.now().strftime("%d-%m-%Y")
            nome_arquivo = f"{data}_logs.log"
            caminho_pasta_logs = "logs"
            self.caminho_completo_arquivo = os.path.join(caminho_pasta_logs, nome_arquivo)
            os.makedirs(caminho_pasta_logs, exist_ok=True)
            handle = [logging.FileHandler(self.caminho_completo_arquivo, 'a'), logging.StreamHandler()]
        else:
            handle = None

        logging.basicConfig(
            level=logging.INFO,
            encoding='utf-8',
            format='%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d',
            datefmt='%d-%m-%Y %H:%M:%S',
            handlers=handle
        )

        self.driver = Driver(
            browser='chrome',
            headless=False,
            incognito=False,
            download_path='',
            desabilitar_carregamento_imagem=False
        ).driver

        super().__init__(self.driver)

