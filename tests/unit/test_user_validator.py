"""
Testes unitários para o módulo de validação de usuário
Cenário 1: Validação de dados de usuário
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from user_validator import UserValidator


@pytest.mark.unit
class TestUserValidator:
    """Cenário 1: Testes de validação de dados de usuário"""
    

    def test_validate_email_valid(self):
        """Testa validação de email com formato válido"""
        valid_emails = [
            "usuario@example.com",
            "test.email@domain.co.uk",
            "user123@test.com.br",
            "nome.sobrenome@empresa.com"
        ]
        
        for email in valid_emails:
            is_valid, message = UserValidator.validate_email(email)
            assert is_valid, f"Email válido {email} foi rejeitado: {message}"
            assert message == "Email válido"
    

    def test_validate_email_invalid(self):
        """Testa validação de email com formatos inválidos"""
        invalid_emails = [
            ("", "Email não pode ser vazio"),
            ("email-sem-arroba.com", "Formato de email inválido"),
            ("@domain.com", "Formato de email inválido"),
            ("user@", "Formato de email inválido"),
            ("user@domain", "Formato de email inválido"),
            (None, "Email não pode ser vazio"),
            ("a" * 256, "Email muito longo (máximo 255 caracteres)")  # Valor extremo
        ]
        
        for email, expected_error in invalid_emails:
            is_valid, message = UserValidator.validate_email(email)
            assert not is_valid, f"Email inválido {email} foi aceito"
            assert expected_error in message or "Email não pode ser vazio" in message
    

    def test_validate_password_valid(self):
        """Testa validação de senha com senhas válidas"""
        valid_passwords = [
            "senha123",
            "MinhaSenh@123",
            "abc123",
            "PASSWORD1",
            "123456a" 
        ]
        
        for password in valid_passwords:
            is_valid, message = UserValidator.validate_password(password)
            assert is_valid, f"Senha válida '{password}' foi rejeitada: {message}"
            assert message == "Senha válida"
    

    def test_validate_password_invalid(self):
        """Testa validação de senha com senhas inválidas"""
        invalid_passwords = [
            ("", "Senha não pode ser vazia"),
            ("12345", "Senha deve ter no mínimo 6 caracteres"),  
            ("abcdef", "Senha deve conter pelo menos um número"),  
            ("123456", "Senha deve conter pelo menos uma letra"),  
            ("a" * 51, "Senha muito longa (máximo 50 caracteres)"),  
            (None, "Senha não pode ser vazia")
        ]
        
        for password, expected_error in invalid_passwords:
            is_valid, message = UserValidator.validate_password(password)
            assert not is_valid, f"Senha inválida '{password}' foi aceita"
            assert expected_error in message or "Senha não pode ser vazia" in message
    

    def test_validate_name_valid(self):
        """Testa validação de nome com nomes válidos"""
        valid_names = [
            "João Silva",
            "Maria",
            "José da Silva",
            "Ana-Clara",
            "Pedro O'Brien",
            "A" * 2,  
            "A" * 100  
        ]
        
        for name in valid_names:
            is_valid, message = UserValidator.validate_name(name)
            assert is_valid, f"Nome válido '{name}' foi rejeitado: {message}"
            assert message == "Nome válido"
    

    def test_validate_name_invalid(self):
        """Testa validação de nome com nomes inválidos"""
        invalid_names = [
            ("", "Nome não pode ser vazio"),
            ("A", "Nome deve ter no mínimo 2 caracteres"), 
            ("A" * 101, "Nome muito longo (máximo 100 caracteres)"), 
            ("123", "Nome contém caracteres inválidos"),  
            ("João@Silva", "Nome contém caracteres inválidos"),  
            ("   ", "Nome deve ter no mínimo 2 caracteres"), 
            (None, "Nome não pode ser vazio")
        ]
        
        for name, expected_error in invalid_names:
            is_valid, message = UserValidator.validate_name(name)
            assert not is_valid, f"Nome inválido '{name}' foi aceito"
            assert expected_error in message or "Nome não pode ser vazio" in message
    
 
    def test_validate_user_data_valid(self):
        """Testa validação completa com dados válidos"""
        is_valid, errors = UserValidator.validate_user_data(
            email="usuario@example.com",
            password="senha123",
            name="João Silva"
        )
        
        assert is_valid, f"Dados válidos foram rejeitados: {errors}"
        assert len(errors) == 0
    

    def test_validate_user_data_multiple_errors(self):
        """Testa validação completa com múltiplos campos inválidos"""
        is_valid, errors = UserValidator.validate_user_data(
            email="email-invalido",
            password="123",
            name="A"
        )
        
        assert not is_valid
        assert len(errors) >= 3  
