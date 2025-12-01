"""
Testes unitários para o módulo de transações financeiras
Cenário 2: Testes de transações bancárias
"""

import pytest
import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from transaction import Account, TransactionManager, TransactionError


@pytest.mark.unit
class TestTransaction:
    """Cenário 2: Testes de transações financeiras"""
    
    def test_transfer_with_sufficient_balance(self):
        """Testa transferência quando há saldo suficiente"""
        account1 = Account("ACC001", balance=1000.0)
        account2 = Account("ACC002", balance=500.0)
        
        result = account1.transfer(account2, 300.0)
        
        assert result is True
        assert account1.balance == 700.0
        assert account2.balance == 800.0
        assert len(account1.transaction_history) == 1
        assert len(account2.transaction_history) == 1
    
    def test_transfer_insufficient_balance(self):
        """Testa transferência quando não há saldo suficiente"""
        account1 = Account("ACC001", balance=100.0)
        account2 = Account("ACC002", balance=50.0)
        
        with pytest.raises(TransactionError) as exc_info:
            account1.transfer(account2, 200.0)
        
        assert "Saldo insuficiente" in str(exc_info.value)
        assert account1.balance == 100.0  
        assert account2.balance == 50.0
    
    def test_transfer_invalid_amount(self):
        """Testa transferência com valores inválidos"""
        account1 = Account("ACC001", balance=1000.0)
        account2 = Account("ACC002", balance=500.0)
        

        with pytest.raises(TransactionError) as exc_info:
            account1.transfer(account2, 0.0)
        assert "deve ser maior que zero" in str(exc_info.value)
        

        with pytest.raises(TransactionError) as exc_info:
            account1.transfer(account2, -100.0)
        assert "deve ser maior que zero" in str(exc_info.value)
        

        assert account1.balance == 1000.0
        assert account2.balance == 500.0
    

    def test_deposit_valid_amount(self):
        """Testa depósito com valores válidos"""
        account = Account("ACC001", balance=100.0)
        
        result = account.deposit(50.0)
        
        assert result is True
        assert account.balance == 150.0
        assert len(account.transaction_history) == 1
    

    def test_deposit_invalid_amount(self):
        """Testa depósito com valores inválidos"""
        account = Account("ACC001", balance=100.0)
        

        with pytest.raises(TransactionError) as exc_info:
            account.deposit(0.0)
        assert "deve ser maior que zero" in str(exc_info.value)
        

        with pytest.raises(TransactionError) as exc_info:
            account.deposit(-50.0)
        assert "deve ser maior que zero" in str(exc_info.value)
        

        with pytest.raises(TransactionError) as exc_info:
            account.deposit(1000001.0)
        assert "excede o limite máximo" in str(exc_info.value)
        
        assert account.balance == 100.0  

    def test_withdraw_sufficient_balance(self):
        """Testa saque quando há saldo suficiente"""
        account = Account("ACC001", balance=1000.0)
        
        result = account.withdraw(300.0)
        
        assert result is True
        assert account.balance == 700.0
        assert len(account.transaction_history) == 1
    
  
    def test_withdraw_insufficient_balance(self):
        """Testa saque quando não há saldo suficiente"""
        account = Account("ACC001", balance=100.0)
        
        with pytest.raises(TransactionError) as exc_info:
            account.withdraw(200.0)
        
        assert "Saldo insuficiente" in str(exc_info.value)
        assert account.balance == 100.0 
    

    def test_transaction_extreme_values(self):
        """Testa transações com valores extremos"""
        account1 = Account("ACC001", balance=200000.0)
        account2 = Account("ACC002", balance=0.0)
        
      
        account1.transfer(account2, 100000.0)
        assert account1.balance == 100000.0
        

        account3 = Account("ACC003", balance=200000.0)
        with pytest.raises(TransactionError) as exc_info:
            account3.transfer(account2, 100001.0)
        assert "excede o limite máximo" in str(exc_info.value)
        

        account1.withdraw(50000.0)
        assert account1.balance == 50000.0
        

        account4 = Account("ACC004", balance=100000.0)
        with pytest.raises(TransactionError) as exc_info:
            account4.withdraw(50001.0)
        assert "excede o limite máximo" in str(exc_info.value)
    

    def test_validate_transaction_amount(self):
        """Testa validação de valores de transação"""

        is_valid, msg = TransactionManager.validate_transaction_amount(100.0)
        assert is_valid
        assert "válido" in msg
        
        is_valid, msg = TransactionManager.validate_transaction_amount(0.01)
        assert is_valid
        

        is_valid, msg = TransactionManager.validate_transaction_amount(0)
        assert not is_valid
        assert "maior que zero" in msg
        
        is_valid, msg = TransactionManager.validate_transaction_amount(-100)
        assert not is_valid
        
        is_valid, msg = TransactionManager.validate_transaction_amount(100001)
        assert not is_valid
        assert "excede o limite" in msg
        
        is_valid, msg = TransactionManager.validate_transaction_amount("100")
        assert not is_valid
        assert "numérico" in msg
    

    def test_can_transfer(self):
        """Testa verificação de possibilidade de transferência"""
        account = Account("ACC001", balance=500.0)
        

        can_transfer, msg = TransactionManager.can_transfer(account, 300.0)
        assert can_transfer is True
        assert "pode ser realizada" in msg
        

        can_transfer, msg = TransactionManager.can_transfer(account, 600.0)
        assert can_transfer is False
        assert "Saldo insuficiente" in msg
        

        can_transfer, msg = TransactionManager.can_transfer(account, 0)
        assert can_transfer is False
        

        can_transfer, msg = TransactionManager.can_transfer(None, 100.0)
        assert can_transfer is False
        assert "Conta inválida" in msg

