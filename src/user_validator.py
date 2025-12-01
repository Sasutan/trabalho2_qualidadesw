"""
Módulo de validação de usuário
Valida emails, senhas e nomes de usuário
"""

import re


class UserValidator:
    """Classe para validação de dados de usuário"""
    
    @staticmethod
    def validate_email(email):
        """
        Valida formato de email
        
        Args:
            email (str): Email a ser validado
            
        Returns:
            tuple: (bool, str) - (é_válido, mensagem_erro)
        """
        if not email or not isinstance(email, str):
            return False, "Email não pode ser vazio"
        
        if len(email) > 255:
            return False, "Email muito longo (máximo 255 caracteres)"
        
    
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, email):
            return False, "Formato de email inválido"
        
        return True, "Email válido"
    
    @staticmethod
    def validate_password(password):
        """
        Valida força da senha
        
        Args:
            password (str): Senha a ser validada
            
        Returns:
            tuple: (bool, str) - (é_válido, mensagem_erro)
        """
        if not password or not isinstance(password, str):
            return False, "Senha não pode ser vazia"
        
        if len(password) < 6:
            return False, "Senha deve ter no mínimo 6 caracteres"
        
        if len(password) > 50:
            return False, "Senha muito longa (máximo 50 caracteres)"
        
 
        has_letter = bool(re.search(r'[a-zA-Z]', password))
        has_number = bool(re.search(r'\d', password))
        
        if not has_letter:
            return False, "Senha deve conter pelo menos uma letra"
        
        if not has_number:
            return False, "Senha deve conter pelo menos um número"
        
        return True, "Senha válida"
    
    @staticmethod
    def validate_name(name):
        """
        Valida nome de usuário
        
        Args:
            name (str): Nome a ser validado
            
        Returns:
            tuple: (bool, str) - (é_válido, mensagem_erro)
        """
        if not name or not isinstance(name, str):
            return False, "Nome não pode ser vazio"
        
        name = name.strip()
        
        if len(name) < 2:
            return False, "Nome deve ter no mínimo 2 caracteres"
        
        if len(name) > 100:
            return False, "Nome muito longo (máximo 100 caracteres)"
        
   
        if not re.match(r'^[a-zA-ZÀ-ÿ\s\-\']+$', name):
            return False, "Nome contém caracteres inválidos"

        if not re.search(r'[a-zA-ZÀ-ÿ]', name):
            return False, "Nome deve conter pelo menos uma letra"
        
        return True, "Nome válido"
    
    @staticmethod
    def validate_user_data(email, password, name=None):
        """
        Valida todos os dados do usuário
        
        Args:
            email (str): Email do usuário
            password (str): Senha do usuário
            name (str, optional): Nome do usuário
            
        Returns:
            tuple: (bool, list) - (é_válido, lista_de_erros)
        """
        errors = []
        
        email_valid, email_msg = UserValidator.validate_email(email)
        if not email_valid:
            errors.append(email_msg)
        
        password_valid, password_msg = UserValidator.validate_password(password)
        if not password_valid:
            errors.append(password_msg)
        
        if name is not None:
            name_valid, name_msg = UserValidator.validate_name(name)
            if not name_valid:
                errors.append(name_msg)
        
        return len(errors) == 0, errors

