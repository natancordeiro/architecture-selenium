import yaml
from selenium.common.exceptions import WebDriverException, NoSuchElementException

from driver.driver import Driver
from iterator.iteration import Interation
from utils.logger_config import logger

class Bot(Interation):
    """Classe que define um bot para interação automatizada com páginas da web."""

    def __init__(self, config_path):
        """
        Inicializa um objeto Bot.

        Args:
            log_file (bool): Define se os registros serão salvos em um arquivo de log (padrão: True).
        """
        
        self.driver = Driver(
            browser='chrome',
            headless=False,
            incognito=False,
            download_path='',
            desabilitar_carregamento_imagem=False
        ).driver

        # Carrega dados do arquivo de configuração
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        configuracoes = config['Configuracao']
        self.configura = configuracoes['config']

        super().__init__(self.driver)
