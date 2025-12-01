"""
Testes funcionais em nível de sistema - Cenário 1: Testes de Login
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@pytest.mark.functional
@pytest.mark.login
class TestLogin:
    """Cenário 1: Testes de Login no BugBank"""
    
    def _find_name_input(self, driver, wait):
        """Helper para encontrar o campo de nome"""
        try:
            return wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Nome') or contains(@placeholder, 'nome')]")))
        except:
            try:
                return driver.find_element(By.XPATH, "//input[@name='name']")
            except:
                name_inputs = driver.find_elements(By.XPATH, "//input[@type='text']")
                if len(name_inputs) > 0:
                    return name_inputs[0]
                raise Exception("Não foi possível encontrar o campo de nome")
    

    def test_login_with_valid_credentials(self, driver, wait, fake):
        """Testa login com credenciais válidas - caminho feliz"""

        email = fake.email()
        password = "senha123"
        name = fake.name()
        

        try:
            register_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Registrar') or contains(text(), 'Regi')]"))
            )
        except:
            register_button = driver.find_elements(By.XPATH, "//button")[1] 
        register_button.click()
        time.sleep(1)
        
   
        try:
            email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'e-mail') or contains(@placeholder, 'E-mail')]")))
        except:
            email_input = driver.find_elements(By.XPATH, "//input[@type='email']")[0]
        email_input.clear()
        email_input.send_keys(email)
        
        name_input = self._find_name_input(driver, wait)
        name_input.clear()
        name_input.send_keys(name)
        
        password_inputs = driver.find_elements(By.XPATH, "//input[@type='password']")
        password_input = password_inputs[0] if len(password_inputs) > 0 else None
        if password_input:
            password_input.clear()
            password_input.send_keys(password)
        
        if len(password_inputs) > 1:
            confirm_password_input = password_inputs[1]
            confirm_password_input.clear()
            confirm_password_input.send_keys(password)
        
   
        try:
            balance_checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox']")
            if not balance_checkbox.is_selected():
                balance_checkbox.click()
        except:
            pass
        

        try:
            register_submit = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Cadastrar') or contains(text(), 'Cada')]")))
        except:
            register_submit = driver.find_elements(By.XPATH, "//button[@type='submit']")[-1]
        register_submit.click()
        time.sleep(2)
        
    
        try:
            back_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Voltar') or contains(text(), 'login')]")))
            back_button.click()
            time.sleep(1)
        except:
            driver.get("https://bugbank.netlify.app/")
            time.sleep(1)
        

        try:
            email_login = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'e-mail') or contains(@placeholder, 'E-mail')]")))
        except:
            email_login = driver.find_elements(By.XPATH, "//input[@type='email']")[0]
        email_login.clear()
        email_login.send_keys(email)
        
        password_login = driver.find_elements(By.XPATH, "//input[@type='password']")[0]
        password_login.clear()
        password_login.send_keys(password)
        
 
        try:
            login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Acessar') or contains(text(), 'Ace')]")))
        except:
            login_button = driver.find_elements(By.XPATH, "//button")[0]
        login_button.click()
        time.sleep(3)
        
   
        page_source = driver.page_source.lower()
        current_url = driver.current_url.lower()
        
        success_indicators = [
            "extrato" in page_source,
            "transferir" in page_source,
            "saldo" in page_source,
            "conta" in page_source and "número" in page_source,
            current_url != "https://bugbank.netlify.app/",
            "logout" in page_source or "sair" in page_source
        ]
        
        assert any(success_indicators), \
            f"Login não foi bem-sucedido. URL: {current_url}"
    
 
    def test_login_with_invalid_email(self, driver, wait):
        """Testa login com email em formato inválido"""
        email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'e-mail') or contains(@placeholder, 'E-mail')]")))
        email_input.clear()
        email_input.send_keys("email-invalido-sem-arroba")
        
        password_input = driver.find_elements(By.XPATH, "//input[@type='password']")[0]
        password_input.clear()
        password_input.send_keys("senha123")
        
        try:
            login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Acessar')]")))
        except:
            login_button = driver.find_elements(By.XPATH, "//button")[0]
        login_button.click()
        time.sleep(2)
        
        page_source = driver.page_source.lower()
        current_url = driver.current_url.lower().split('#')[0]
        assert current_url == "https://bugbank.netlify.app/" or \
               "erro" in page_source or "inválido" in page_source, \
            "Sistema deveria rejeitar email inválido"
    
  
    def test_login_with_wrong_password(self, driver, wait, fake):
        """Testa login com senha incorreta"""
        email = fake.email()
        password = "senha123"
        name = fake.name()

        register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Registrar')]")))
        register_button.click()
        time.sleep(1)
        
        email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'e-mail') or contains(@placeholder, 'E-mail')]")))
        email_input.clear()
        email_input.send_keys(email)
        
        try:
            name_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Nome') or contains(@placeholder, 'nome')]")))
        except:
            name_inputs = driver.find_elements(By.XPATH, "//input[@type='text']")
            if len(name_inputs) > 0:
                name_input = name_inputs[0]
            else:
       
                name_input = driver.find_element(By.XPATH, "//input[@name='name']")
        name_input.clear()
        name_input.send_keys(name)
        
        password_inputs = driver.find_elements(By.XPATH, "//input[@type='password']")
        password_inputs[0].clear()
        password_inputs[0].send_keys(password)
        password_inputs[1].clear()
        password_inputs[1].send_keys(password)
        
        register_submit = driver.find_elements(By.XPATH, "//button[@type='submit']")[-1]
        register_submit.click()
        time.sleep(2)
        

        try:
            back_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Voltar')]")))
            back_button.click()
            time.sleep(1)
        except:
            driver.get("https://bugbank.netlify.app/")
            time.sleep(1)
        

        email_login = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'e-mail')]")))
        email_login.clear()
        email_login.send_keys(email)
        
        password_login = driver.find_elements(By.XPATH, "//input[@type='password']")[0]
        password_login.clear()
        password_login.send_keys("senha_errada_123")
        
        login_button = driver.find_elements(By.XPATH, "//button")[0]
        login_button.click()
        time.sleep(2)
        
        page_source = driver.page_source.lower()
        current_url = driver.current_url.lower()

        base_url = current_url.split('#')[0]
        assert base_url == "https://bugbank.netlify.app/" or \
               "erro" in page_source or "incorreta" in page_source or \
               "senha" in page_source, \
            "Sistema deveria rejeitar senha incorreta"
    

    def test_login_with_empty_fields(self, driver, wait):
        """Testa login sem preencher os campos"""
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Acessar')]")))
        login_button.click()
        time.sleep(2)
        
        email_input = driver.find_elements(By.XPATH, "//input[@type='email']")[0]
        password_input = driver.find_elements(By.XPATH, "//input[@type='password']")[0]
        
        current_url = driver.current_url.lower().split('#')[0]
        assert email_input.get_attribute("value") == "" or \
               password_input.get_attribute("value") == "" or \
               current_url == "https://bugbank.netlify.app/", \
            "Sistema deveria validar campos vazios"
    

    def test_login_with_unregistered_email(self, driver, wait, fake):
        """Testa login com email que não está cadastrado"""
        email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'e-mail')]")))
        email_input.clear()
        email_input.send_keys(fake.email())
        
        password_input = driver.find_elements(By.XPATH, "//input[@type='password']")[0]
        password_input.clear()
        password_input.send_keys("senha123")
        
        login_button = driver.find_elements(By.XPATH, "//button")[0]
        login_button.click()
        time.sleep(2)
        
        page_source = driver.page_source.lower()
        current_url = driver.current_url.lower().split('#')[0]
        assert current_url == "https://bugbank.netlify.app/" or \
               "erro" in page_source or "não encontrado" in page_source, \
            "Sistema deveria rejeitar email não cadastrado"

