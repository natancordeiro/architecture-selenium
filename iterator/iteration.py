from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
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
        metodos = {
            'css': By.CSS_SELECTOR,
            'id': By.ID,
            'xpath': By.XPATH
        }
        method = metodos.get(metodo)
        el = WebDriverWait(self.driver, tempo).until(
            EC.element_to_be_clickable((method, tag)))
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
        metodos = {
            'css': By.CSS_SELECTOR,
            'id': By.ID,
            'xpath': By.XPATH
        }
        method = metodos.get(metodo)
        WebDriverWait(self.driver, tempo).until(
            EC.presence_of_element_located((method, tag)))
        elemento = self.driver.find_element(method, tag)
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

    def find(self, tag: str, tempo=15, metodo='xpath', element_is='clickable') -> WebElement:
        """
        Localiza um elemento na página.

        Args:
            tag (str): Identificador do elemento.
            tempo (int): Tempo máximo de espera em segundos (padrão: 15).
            metodo (str): Método de localização do elemento (padrão: 'xpath').

        Returns:
            selenium.webdriver.remote.webelement.WebElement: Elemento encontrado.
        """
        metodos = {
            'css': By.CSS_SELECTOR,
            'id': By.ID,
            'xpath': By.XPATH
        }

        method = metodos.get(metodo)
        
        if element_is is not None:
            atributos = {
            'clickable': EC.element_to_be_clickable,
            'selected': EC.element_to_be_selected,
            'text_in': EC.text_to_be_present_in_element,
            'presence': EC.presence_of_element_located,
            'visibled': EC.visibility_of_element_located
            }

            atributo = atributos.get(element_is)
        else:
            atributo = EC.element_to_be_clickable

        WebDriverWait(self.driver, tempo).until(
            atributo((method, tag)))
        elemento = self.driver.find_element(method, tag)
        return elemento

    def find_all(self, tag: str, tempo=15, metodo='xpath', element_is='presence') -> list[WebElement]:
        """
        Localiza todos os elementos correspondentes na página.

        Args:
            tag (str): Identificador do elemento.
            tempo (int): Tempo máximo de espera em segundos (padrão: 15).
            metodo (str): Método de localização do elemento (padrão: 'xpath').

        Returns:
            list: Lista de elementos encontrados.
        """
        metodos = {
            'css': By.CSS_SELECTOR,
            'id': By.ID,
            'xpath': By.XPATH
        }

        if element_is is not None:
            atributos = {
            'clickable': EC.element_to_be_clickable,
            'selected': EC.element_to_be_selected,
            'text_in': EC.text_to_be_present_in_element,
            'presence': EC.presence_of_element_located,
            'visibled': EC.visibility_of_element_located
            }

            atributo = atributos.get(element_is)
        else:
            atributo = EC.presence_of_element_located

        method = metodos.get(metodo)

        WebDriverWait(self.driver, tempo).until(
            atributo((method, tag)))
        elementos = self.driver.find_elements(method, tag)
        return elementos
    
    def wait_for(self, tag:str, timeout=15, metodo='xpath', element_is='clickable'):
        """
        Espera até que um elemento seja encontrado na página.

        Args:
            tag (str): Identificador do elemento.
            timeout (int): Tempo máximo de espera em segundos (padrão: 15).
            metodo (str): Método de localização do elemento (padrão: 'xpath').
        """
        metodos = {
            'css': By.CSS_SELECTOR,
            'id': By.ID,
            'xpath': By.XPATH
        }

        if element_is is not None:
            atributos = {
            'clickable': EC.element_to_be_clickable,
            'selected': EC.element_to_be_selected,
            'text_in': EC.text_to_be_present_in_element,
            'presence': EC.presence_of_element_located,
            'visibled': EC.visibility_of_element_located
            }

            atributo = atributos.get(element_is)
        else:
            atributo = EC.element_to_be_clickable

        method = metodos.get(metodo)
        return WebDriverWait(self.driver, timeout).until(
            atributo((method, tag)))
    
    def wait_for_url(self, target_url: str, timeout=10):
        """
        Espera até que a URL do navegador seja igual à URL alvo.

        Args:
            target_url (str): URL alvo que estamos esperando.
            timeout (int, opcional): Tempo máximo de espera em segundos. Padrão é 10 segundos.

        Exemplo de uso:
            driver = webdriver.Chrome()
            driver.get('https://www.example.com')
            wait_for_url(driver, 'https://www.example.com')
        """
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_contains(target_url))
        except TimeoutException:
            raise TimeoutException(f"A URL não correspondeu à URL alvo '{target_url}' dentro do tempo limite de {timeout} segundos.")

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
        metodos = {
            'css': By.CSS_SELECTOR,
            'id': By.ID,
            'xpath': By.XPATH
        }

        method = metodos.get(metodo)
        return self.find(tag, tempo, method).get_attribute(atributo)

    def click_js(self, tag: str, tempo=15, metodo='xpath'):
        """
        Executa um clique em um elemento usando JavaScript.

        Args:
            tag (str): Identificador do elemento.
            tempo (int): Tempo máximo de espera em segundos (padrão: 15).
            metodo (str): Método de localização do elemento (padrão: 'xpath').
        """
        metodos = {
            'css': By.CSS_SELECTOR,
            'id': By.ID,
            'xpath': By.XPATH
        }

        method = metodos.get(metodo)
        el = self.find(tag, tempo, method)
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
        metodos = {
            'css': By.CSS_SELECTOR,
            'id': By.ID,
            'xpath': By.XPATH
        }
        metodo = metodos.get(metodo)
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
        time.sleep(seconds)

    def quit(self):
        """
        Encerra a instância do navegador.
        """
        self.driver.quit()
