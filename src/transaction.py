"""
Módulo de transações financeiras
Gerencia transferências e validações de saldo
"""


class TransactionError(Exception):
    """Exceção personalizada para erros de transação"""
    pass


class Account:
    """Classe que representa uma conta bancária"""
    
    def __init__(self, account_id, balance=0.0):
        """
        Inicializa uma conta
        
        Args:
            account_id (str): ID da conta
            balance (float): Saldo inicial
        """
        if balance < 0:
            raise ValueError("Saldo inicial não pode ser negativo")
        
        self.account_id = account_id
        self._balance = float(balance)
        self.transaction_history = []
    
    @property
    def balance(self):
        """Retorna o saldo atual"""
        return self._balance
    
    def deposit(self, amount):
        """
        Realiza um depósito
        
        Args:
            amount (float): Valor a ser depositado
            
        Returns:
            bool: True se sucesso
        """
        if amount <= 0:
            raise TransactionError("Valor do depósito deve ser maior que zero")
        
        if amount > 1000000:
            raise TransactionError("Valor do depósito excede o limite máximo")
        
        self._balance += amount
        self.transaction_history.append({
            'type': 'deposit',
            'amount': amount,
            'balance_after': self._balance
        })
        return True
    
    def withdraw(self, amount):
        """
        Realiza um saque
        
        Args:
            amount (float): Valor a ser sacado
            
        Returns:
            bool: True se sucesso
        """
        if amount <= 0:
            raise TransactionError("Valor do saque deve ser maior que zero")
        
        if amount > self._balance:
            raise TransactionError("Saldo insuficiente")
        
        if amount > 50000:
            raise TransactionError("Valor do saque excede o limite máximo por transação")
        
        self._balance -= amount
        self.transaction_history.append({
            'type': 'withdraw',
            'amount': amount,
            'balance_after': self._balance
        })
        return True
    
    def transfer(self, target_account, amount):
        """
        Realiza uma transferência para outra conta
        
        Args:
            target_account (Account): Conta de destino
            amount (float): Valor a ser transferido
            
        Returns:
            bool: True se sucesso
        """
        if not isinstance(target_account, Account):
            raise TransactionError("Conta de destino inválida")
        
        if amount <= 0:
            raise TransactionError("Valor da transferência deve ser maior que zero")
        
      
        if amount > 100000:
            raise TransactionError("Valor da transferência excede o limite máximo")
        
        if amount > self._balance:
            raise TransactionError("Saldo insuficiente para transferência")
     
        self._balance -= amount
        target_account._balance += amount

        self.transaction_history.append({
            'type': 'transfer_out',
            'amount': amount,
            'to': target_account.account_id,
            'balance_after': self._balance
        })
        
        target_account.transaction_history.append({
            'type': 'transfer_in',
            'amount': amount,
            'from': self.account_id,
            'balance_after': target_account._balance
        })
        
        return True
    
    def get_transaction_count(self):
        """Retorna o número de transações realizadas"""
        return len(self.transaction_history)


class TransactionManager:
    """Gerenciador de transações entre contas"""
    
    @staticmethod
    def validate_transaction_amount(amount):
        """
        Valida o valor de uma transação
        
        Args:
            amount: Valor a ser validado
            
        Returns:
            tuple: (bool, str) - (é_válido, mensagem_erro)
        """
        if not isinstance(amount, (int, float)):
            return False, "Valor deve ser numérico"
        
        if amount <= 0:
            return False, "Valor deve ser maior que zero"
        
        if amount > 100000:
            return False, "Valor excede o limite máximo de transação"
        
        return True, "Valor válido"
    
    @staticmethod
    def can_transfer(source_account, amount):
        """
        Verifica se uma transferência pode ser realizada
        
        Args:
            source_account (Account): Conta de origem
            amount (float): Valor a ser transferido
            
        Returns:
            tuple: (bool, str) - (pode_transferir, mensagem)
        """
        if not isinstance(source_account, Account):
            return False, "Conta inválida"
        
        amount_valid, msg = TransactionManager.validate_transaction_amount(amount)
        if not amount_valid:
            return False, msg
        
        if amount > source_account.balance:
            return False, "Saldo insuficiente"
        
        return True, "Transferência pode ser realizada"

