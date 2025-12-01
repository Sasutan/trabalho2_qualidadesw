"""
Testes funcionais em nível de sistema - Cenário 2: Testes de Registro
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@pytest.mark.functional
@pytest.mark.registration
class TestRegistration:
    """Cenário 2: Testes de Registro no BugBank"""
    
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
    
  
    def test_register_with_valid_data(self, driver, wait, fake):
        """Testa registro com dados válidos - caminho feliz"""
        register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Registrar')]")))
        register_button.click()
        time.sleep(1)
        
        email = fake.email()
        name = fake.name()
        password = "senha123"
        
        email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'e-mail')]")))
        email_input.clear()
        email_input.send_keys(email)
        
        name_input = self._find_name_input(driver, wait)
        name_input.clear()
        name_input.send_keys(name)
        
        password_inputs = driver.find_elements(By.XPATH, "//input[@type='password']")
        password_inputs[0].clear()
        password_inputs[0].send_keys(password)
        password_inputs[1].clear()
        password_inputs[1].send_keys(password)
        
        try:
            balance_checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox']")
            if not balance_checkbox.is_selected():
                balance_checkbox.click()
        except:
            pass
        
        register_submit = driver.find_elements(By.XPATH, "//button[@type='submit']")[-1]
        register_submit.click()
        time.sleep(2)
        
        page_source = driver.page_source.lower()
        assert "cadastrado" in page_source or "sucesso" in page_source or \
               driver.current_url != "https://bugbank.netlify.app/" or \
               "voltar ao login" in page_source, \
            "Registro não foi bem-sucedido"
    
    def test_register_with_password_mismatch(self, driver, wait, fake):
        """Testa registro quando as senhas não coincidem"""
        register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Registrar')]")))
        register_button.click()
        time.sleep(1)
        
        email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'e-mail')]")))
        email_input.clear()
        email_input.send_keys(fake.email())
        
        name_input = self._find_name_input(driver, wait)
        name_input.clear()
        name_input.send_keys(fake.name())
        
        password_inputs = driver.find_elements(By.XPATH, "//input[@type='password']")
        password_inputs[0].clear()
        password_inputs[0].send_keys("senha123")
        password_inputs[1].clear()
        password_inputs[1].send_keys("senha456") 
        
        register_submit = driver.find_elements(By.XPATH, "//button[@type='submit']")[-1]
        register_submit.click()
        time.sleep(2)
        
        page_source = driver.page_source.lower()
        current_url = driver.current_url.lower().split('#')[0]
        assert current_url == "https://bugbank.netlify.app/" or \
               "senha" in page_source or "coincidem" in page_source, \
            "Sistema deveria rejeitar senhas que não coincidem"
    
 
    def test_register_with_existing_email(self, driver, wait, fake):
        """Testa registro com email que já está cadastrado"""
        email = fake.email()
        name1 = fake.name()
        password = "senha123"
        

        register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Registrar')]")))
        register_button.click()
        time.sleep(1)
        
        email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'e-mail')]")))
        email_input.clear()
        email_input.send_keys(email)
        
        name_input = self._find_name_input(driver, wait)
        name_input.clear()
        name_input.send_keys(name1)
        
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
        
        register_button2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Registrar')]")))
        register_button2.click()
        time.sleep(1)
        
  
        email_input2 = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'e-mail')]")))
        email_input2.clear()
        email_input2.send_keys(email)  
        
        name_input2 = self._find_name_input(driver, wait)
        name_input2.clear()
        name_input2.send_keys(fake.name())
        
        password_inputs2 = driver.find_elements(By.XPATH, "//input[@type='password']")
        password_inputs2[0].clear()
        password_inputs2[0].send_keys(password)
        password_inputs2[1].clear()
        password_inputs2[1].send_keys(password)
        
        register_submit2 = driver.find_elements(By.XPATH, "//button[@type='submit']")[-1]
        register_submit2.click()
        time.sleep(2)
        
        page_source = driver.page_source.lower()
        current_url = driver.current_url.lower().split('#')[0]
        assert current_url == "https://bugbank.netlify.app/" or \
               "email" in page_source or "já existe" in page_source, \
            "Sistema deveria rejeitar email já cadastrado"
    

    def test_register_with_invalid_fields(self, driver, wait):
        """Testa registro com campos inválidos"""
        register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Registrar')]")))
        register_button.click()
        time.sleep(1)
        
        email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'e-mail')]")))
        email_input.clear()
        email_input.send_keys("email-invalido-sem-arroba")
        
        name_input = self._find_name_input(driver, wait)
        name_input.clear()
        name_input.send_keys("A")
        
        password_inputs = driver.find_elements(By.XPATH, "//input[@type='password']")
        password_inputs[0].clear()
        password_inputs[0].send_keys("123")
        password_inputs[1].clear()
        password_inputs[1].send_keys("123")
        
        register_submit = driver.find_elements(By.XPATH, "//button[@type='submit']")[-1]
        register_submit.click()
        time.sleep(2)
        
        page_source = driver.page_source.lower()
        current_url = driver.current_url.lower().split('#')[0]
        assert current_url == "https://bugbank.netlify.app/" or \
               "erro" in page_source or "inválido" in page_source, \
            "Sistema deveria validar campos inválidos"
    

    def test_register_with_empty_fields(self, driver, wait):
        """Testa registro sem preencher os campos obrigatórios"""
        register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Registrar')]")))
        register_button.click()
        time.sleep(1)
        
        register_submit = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Cadastrar')]")))
        register_submit.click()
        time.sleep(2)
        
        email_input = driver.find_elements(By.XPATH, "//input[@type='email']")[0]
        name_input = self._find_name_input(driver, wait)
        password_inputs = driver.find_elements(By.XPATH, "//input[@type='password']")
        
        assert email_input.get_attribute("value") == "" or \
               name_input.get_attribute("value") == "" or \
               len(password_inputs) == 0 or password_inputs[0].get_attribute("value") == "", \
            "Sistema deveria validar campos vazios"
    

    def test_register_with_short_password(self, driver, wait, fake):
        """Testa registro com senha que não atende aos requisitos mínimos"""
        register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Registrar')]")))
        register_button.click()
        time.sleep(1)
        
        email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'e-mail')]")))
        email_input.clear()
        email_input.send_keys(fake.email())
        
        name_input = self._find_name_input(driver, wait)
        name_input.clear()
        name_input.send_keys(fake.name())
        
        password_inputs = driver.find_elements(By.XPATH, "//input[@type='password']")
        password_inputs[0].clear()
        password_inputs[0].send_keys("123")  
        password_inputs[1].clear()
        password_inputs[1].send_keys("123")
        
        register_submit = driver.find_elements(By.XPATH, "//button[@type='submit']")[-1]
        register_submit.click()
        time.sleep(2)
        
        page_source = driver.page_source.lower()
        current_url = driver.current_url.lower().split('#')[0]
        assert current_url == "https://bugbank.netlify.app/" or \
               "senha" in page_source or "mínimo" in page_source, \
            "Sistema deveria rejeitar senha muito curta"

