import os
import re
import logging
import sys
from iterator.iteration import Interation
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as GeckoOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import WebDriverException
import undetected_chromedriver as uc

class Driver(Interation):
    """Classe para gerenciar o WebDriver e as opções do navegador."""

    def __init__(self, browser='chrome', headless=False, incognito=False, download_path='', remote=False, desabilitar_carregamento_imagem=False):
        """
        Inicializa um objeto Driver.

        Args:
            browser (str): O navegador a ser utilizado (padrão: 'chrome').
            headless (bool): Define se o navegador será executado em modo headless (padrão: False).
            incognito (bool): Define se o navegador será iniciado no modo incognito (padrão: False).
            download_path (str): O caminho para o diretório de downloads (padrão: '').
            remote (bool): Define se a execução será remota (padrão: False).
            desabilitar_carregamento_imagem (bool): Define se o carregamento de imagens será desabilitado (padrão: False).
        """
        if download_path != '':
            download_path = self.get_download_dir()

        if remote:
            if browser == 'chrome':
                self.make_chrome(headless, incognito, download_path, desabilitar_carregamento_imagem, remote)
            elif browser == 'firefox':
                self.make_mozilla(headless, incognito, download_path, desabilitar_carregamento_imagem, remote)
            else:
                logging.error(f'{browser} não suportado para acesso remoto.')
                sys.exit(1)
        else:
            if browser == 'chrome':
                self.make_chrome(headless, incognito, download_path, desabilitar_carregamento_imagem, remote)
            elif browser == 'firefox':
                self.make_mozilla(headless, incognito, download_path, desabilitar_carregamento_imagem, remote)
            elif browser == 'undetected_chromedriver':
                self.make_uc(headless, incognito, download_path, desabilitar_carregamento_imagem)

    def get_download_dir(self):
        """
        Retorna o diretório padrão de downloads do sistema operacional.

        Returns:
            str: O diretório de downloads padrão.
        """
        if os.name == 'nt':
            return os.path.join(os.environ.get('USERPROFILE'), 'Downloads')
        elif os.name == 'posix':
            return os.path.join(os.path.expanduser('~'), 'Downloads')
        else:
            return None

    def make_uc(self, headless, incognito, download_path, desabilitar_carregamento_imagem):
        """
        Configura o navegador Chrome com Undetected Chromedriver.

        Args:
            headless (bool): Define se o navegador será executado em modo headless.
            incognito (bool): Define se o navegador será iniciado no modo incognito.
            download_path (str): O caminho para o diretório de downloads.
            desabilitar_carregamento_imagem (bool): Define se o carregamento de imagens será desabilitado.
        """
        user_data_dir = os.path.join(os.getcwd(), 'appdata')
        Service(ChromeDriverManager().install())
        options = uc.ChromeOptions()
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        options.add_argument("--no-sandbox")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--safebrowsing-disable-download-protection")
        options.add_experimental_option('prefs',
                                        {'download.prompt_for_download': False,
                                         'profile.default_content_setting_values.notifications': 2,
                                         'profile.default_content_setting_values.automatic_downloads': 1,
                                         'download.default_directory': download_path})
        if incognito:
            options.add_argument("--incognito")
        if desabilitar_carregamento_imagem:
            options.add_argument('--blink-settings=imagesEnabled=false')

        try:
            self.driver = uc.Chrome(options, user_data_dir, log_level=4, headless=headless)
        except WebDriverException as e:
            if 'This version of ChromeDriver only supports Chrome version' in str(e):
                versao_chromedriver_suporta = re.search("ChromeDriver only supports Chrome version (\\d+)", str(e)).group(1)
                versao_navegador_cliente = re.search("Current browser version is (\\d+\\.\\d+\\.\\d+\\.\\d+)", str(e)).group(1)
                logging.critical(f'Erro: Navegador está na versão {versao_navegador_cliente}. O ChromeDriver suporta apenas a vesão {versao_chromedriver_suporta}. Favor atualizar o Navegador.')
            else:
                logging.critical('Erro ao instânciar Navegador.')
                sys.exit(1)

    def make_chrome(self, headless, incognito, download_path, desabilitar_carregamento_imagem, remote):
        """
        Configura o navegador Chrome.

        Args:
            headless (bool): Define se o navegador será executado em modo headless.
            incognito (bool): Define se o navegador será iniciado no modo incognito.
            download_path (str): O caminho para o diretório de downloads.
            desabilitar_carregamento_imagem (bool): Define se o carregamento de imagens será desabilitado.
            remote (bool): Define se a execução será remota.
        """
        user_data_dir = os.path.join(os.getcwd(), 'appdata')
        service = Service(ChromeDriverManager().install())
        options = ChromeOptions()

        if remote:
            options.set_capability("browserVersion", "121.0")
            options.set_capability("selenoid:options", {"enableVNC": True})
            options.set_capability("selenoid:options", {"screenResolution ": "1280x1024x24"})
            options.set_capability("selenoid:options", {"enableVideo": False})
            self.driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub", options=options)
        else:
            options.add_argument(f"--user-data-dir={user_data_dir}")
            options.add_argument('--log-level=4')
            options.add_argument('--disable-notifications')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-gpu')
            options.add_argument("--no-sandbox")
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("--safebrowsing-disable-download-protection")
            options.add_experimental_option('prefs',
                                            {'download.prompt_for_download': False,
                                             'profile.default_content_setting_values.notifications': 2,
                                             'profile.default_content_setting_values.automatic_downloads': 1,
                                             'download.default_directory': download_path})

            if headless:
                options.add_argument('--headless')
            if incognito:
                options.add_argument("--incognito")
            if desabilitar_carregamento_imagem:
                options.add_argument('--blink-settings=imagesEnabled=false')
        try:
            self.driver = webdriver.Chrome(service=service, options=options)
        except WebDriverException as e:
            if 'This version of ChromeDriver only supports Chrome version' in str(e):
                versao_chromedriver_suporta = re.search("ChromeDriver only supports Chrome version (\\d+)", str(e)).group(1)
                versao_navegador_cliente = re.search("Current browser version is (\\d+\\.\\d+\\.\\d+\\.\\d+)", str(e)).group(1)
                logging.critical(f'Erro: Navegador está na versão {versao_navegador_cliente}. O ChromeDriver suporta apenas a vesão {versao_chromedriver_suporta}. Favor atualizar o Navegador.')
            else:
                logging.critical('Erro ao instânciar Navegador.')
                sys.exit(1)

    def make_mozilla(self, headless, incognito, download_path, desabilitar_carregamento_imagem, remote):
        """
        Configura o navegador Firefox.

        Args:
            headless (bool): Define se o navegador será executado em modo headless.
            incognito (bool): Define se o navegador será iniciado no modo incognito.
            download_path (str): O caminho para o diretório de downloads.
            desabilitar_carregamento_imagem (bool): Define se o carregamento de imagens será desabilitado.
            remote (bool): Define se a execução será remota.
        """
        user_data_dir = os.path.join(os.getcwd(), 'appdata')
        service = Service(GeckoDriverManager().install())
        options = GeckoOptions()

        if remote:
            options.set_capability("browserVersion", "121.0")
            options.set_capability("selenoid:options", {"enableVNC": True})
            options.set_capability("selenoid:options", {"screenResolution ": "1280x1024x24"})
            options.set_capability("selenoid:options", {"enableVideo": False})
            self.driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub", options=options)
        else:
            options.add_argument('--log-level=4')
            options.add_argument('--disable-notifications')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-plugins')
            options.add_argument('--disable-gpu')
            options.add_argument(f"--user-data-dir={user_data_dir}")

            options.set_preference("browser.download.folderList", 2)
            options.set_preference("browser.download.dir", download_path)
            options.set_preference("browser.download.useDownloadDir", True)
            options.set_preference("dom.webnotifications.enabled", False)
            options.set_preference("layers.acceleration.disabled", True)
            options.set_preference("toolkit.cosmeticAnimations.enabled", False)

            if headless:
                options.add_argument('--headless')
            if incognito:
                options.set_preference("browser.privatebrowsing.autostart", True)
            if desabilitar_carregamento_imagem:
                options.add_argument('--blink-settings=imagesEnabled=false')

        try:
            self.driver = webdriver.Firefox(service=service, options=options)
        except WebDriverException as e:
            if 'This version of ChromeDriver only supports Chrome version' in str(e):
                versao_chromedriver_suporta = re.search("ChromeDriver only supports Chrome version (\\d+)", str(e)).group(1)
                versao_navegador_cliente = re.search("Current browser version is (\\d+\\.\\d+\\.\\d+\\.\\d+)", str(e)).group(1)
                logging.critical(f'Erro: Navegador está na versão {versao_navegador_cliente}. O ChromeDriver suporta apenas a vesão {versao_chromedriver_suporta}. Favor atualizar o Navegador.')
            else:
                logging.critical('Erro ao instânciar Navegador.')
                sys.exit(1)
