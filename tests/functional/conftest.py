"""
Configuração compartilhada para testes funcionais
Usa Firefox com GeckoDriver
"""

import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from faker import Faker
import time
import os
import shutil


def _clear_webdriver_cache():
    """Limpa o cache do webdriver-manager para evitar drivers corrompidos"""
    cache_path = os.path.join(os.path.expanduser("~"), ".wdm")
    if os.path.exists(cache_path):
        try:
            shutil.rmtree(cache_path)
        except:
            pass  


@pytest.fixture(scope="function")
def driver():
    """Fixture para inicializar e fechar o driver do Selenium (Firefox)"""
    firefox_options = Options()
    firefox_options.add_argument("--headless")  
    firefox_options.add_argument("--width=1920")
    firefox_options.add_argument("--height=1080")
    
    driver_instance = None
    
    try:
   
        try:
            driver_path = GeckoDriverManager().install()
            service = Service(driver_path)
            driver_instance = webdriver.Firefox(service=service, options=firefox_options)
        except Exception as e:
     
            _clear_webdriver_cache()
            try:
                driver_path = GeckoDriverManager().install()
                service = Service(driver_path)
                driver_instance = webdriver.Firefox(service=service, options=firefox_options)
            except Exception as e2:
               
                try:
                    driver_instance = webdriver.Firefox(options=firefox_options)
                except Exception as e3:
                    pytest.skip(f"Não foi possível inicializar o GeckoDriver. Erros: {e}, {e2}, {e3}")
    except Exception as e:
        pytest.skip(f"Não foi possível inicializar o driver do navegador: {e}")
    
    if driver_instance is None:
        pytest.skip("Não foi possível inicializar o driver do navegador")
    
    try:
        driver_instance.set_window_size(1920, 1080)
        driver_instance.get("https://bugbank.netlify.app/")
    except Exception as e:
        if driver_instance:
            try:
                driver_instance.quit()
            except:
                pass
        pytest.skip(f"Não foi possível acessar o site BugBank: {e}")
    
    yield driver_instance
    
    if driver_instance:
        try:
            driver_instance.quit()
        except:
            pass


@pytest.fixture
def fake():
    """Fixture para gerar dados falsos"""
    return Faker('pt_BR')


@pytest.fixture
def wait(driver):
    """Fixture para WebDriverWait"""
    return WebDriverWait(driver, 10)

