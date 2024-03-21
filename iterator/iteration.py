from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

class Interation:
    """Classe para interação do usuário com o navegador."""

    def __init__(self, driver, tempo=10):
        """
        Inicializa um objeto Interacao.

        Args:
            driver: Objeto WebDriver do Selenium.
            tempo (int): Tempo máximo de espera em segundos (padrão: 10).
        """
        self.wait = WebDriverWait(driver, tempo)
        self.driver = driver

    def click(self, tag: str, metodo='xpath', tempo=10):
        """
        Clica em um elemento da página.

        Args:
            tag (str): Identificador do elemento.
            metodo (str): Método de localização do elemento (padrão: 'xpath').
            tempo (int): Tempo máximo de espera em segundos (padrão: 10).

        Returns:
            bool: True se o clique for bem-sucedido, False caso contrário.
        """
        el = WebDriverWait(self.driver, tempo).until(
            EC.element_to_be_clickable((metodo, tag)))
        self.driver.execute_script("arguments[0].click();", el)
        return True

    def key(self, tag: str, tecla='enter', tempo=15, metodo='xpath'):
        """
        Pressiona uma tecla em um elemento da página.

        Args:
            tag (str): Identificador do elemento.
            tecla (str): Tecla a ser pressionada (padrão: 'enter').
            tempo (int): Tempo máximo de espera em segundos (padrão: 15).
            metodo (str): Método de localização do elemento (padrão: 'xpath').

        Returns:
            bool: True se a ação for bem-sucedida, False caso contrário.
        """
        WebDriverWait(self.driver, tempo).until(
            EC.presence_of_element_located((metodo, tag)))
        elemento = self.driver.find_element(metodo, tag)
        acoes = {
            'enter': Keys.ENTER,
            'esc': Keys.ESCAPE,
            'down': Keys.DOWN,
            'home': Keys.HOME,
            'tab': Keys.TAB
        }
        if tecla in acoes:
            elemento.send_keys(acoes[tecla])
        else:
            elemento.send_keys(tecla)
        return True

    def find(self, tag: str, tempo=15, metodo='xpath'):
        """
        Localiza um elemento na página.

        Args:
            tag (str): Identificador do elemento.
            tempo (int): Tempo máximo de espera em segundos (padrão: 15).
            metodo (str): Método de localização do elemento (padrão: 'xpath').

        Returns:
            selenium.webdriver.remote.webelement.WebElement: Elemento encontrado.
        """
        WebDriverWait(self.driver, tempo).until(
            EC.element_to_be_clickable((metodo, tag)))
        elemento = self.driver.find_element(metodo, tag)
        return elemento

    def find_all(self, tag: str, timeout=15, metodo='xpath'):
        """
        Localiza todos os elementos correspondentes na página.

        Args:
            tag (str): Identificador do elemento.
            tempo (int): Tempo máximo de espera em segundos (padrão: 15).
            metodo (str): Método de localização do elemento (padrão: 'xpath').

        Returns:
            list: Lista de elementos encontrados.
        """
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((metodo, tag)))
        elementos = self.driver.find_elements(metodo, tag)
        return elementos
    
    def wait_for(self, tag:str, timeout=15, metodo='xpath'):
        """
        Espera até que um elemento seja encontrado na página.

        Args:
            tag (str): Identificador do elemento.
            timeout (int): Tempo máximo de espera em segundos (padrão: 15).
            metodo (str): Método de localização do elemento (padrão: 'xpath').
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((metodo, tag)))

    def get_attribute(self, tag: str, atributo='value', tempo=15, metodo='xpath'):
        """
        Obtém o valor de um atributo de um elemento.

        Args:
            tag (str): Identificador do elemento.
            atributo (str): Nome do atributo a ser obtido (padrão: 'value').
            tempo (int): Tempo máximo de espera em segundos (padrão: 15).
            metodo (str): Método de localização do elemento (padrão: 'xpath').

        Returns:
            str: Valor do atributo especificado.
        """
        return self.find(tag, tempo, metodo).get_attribute(atributo)

    def click_js(self, tag: str, tempo=15, metodo='xpath'):
        """
        Executa um clique em um elemento usando JavaScript.

        Args:
            tag (str): Identificador do elemento.
            tempo (int): Tempo máximo de espera em segundos (padrão: 15).
            metodo (str): Método de localização do elemento (padrão: 'xpath').
        """
        el = self.find(tag, tempo, metodo)
        self.driver.execute_script("arguments[0].click();", el)

    def write_js(self, tag, valor):
        """
        Insere um valor em um campo usando JavaScript.

        Args:
            tag (str): Identificador do elemento.
            valor: Valor a ser inserido no campo.
        """
        js = f'document.querySelector("{tag}").value = "{valor}"'
        self.driver.execute_script(js)

    def write(self, seletor, valor: str, tempo=15, metodo='xpath'):
        """
        Insere um valor em um campo de entrada.

        Args:
            seletor (str): Identificador do elemento.
            valor (str): Valor a ser inserido no campo.
            tempo (int): Tempo máximo de espera em segundos (padrão: 15).
            metodo (str): Método de localização do elemento (padrão: 'xpath').
        """
        el = self.find(seletor, tempo, metodo)
        el.send_keys(str(valor))

    def load_page(self, url):
        """
        Carrega uma página no navegador.

        Args:
            url (str): URL da página a ser carregada.
        """
        self.driver.get(url)

    def sleep(self, seconds: float):
        """
        Espera um determinado tempo, em segundos.

        Args:
            seconds (float): Número em segundos.
        """
        time.sleep()

    def quit(self):
        """
        Encerra a instância do navegador.
        """
        self.driver.quit()