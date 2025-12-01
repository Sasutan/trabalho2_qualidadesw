# Trabalho de Testes Automatizados - Natan Barbosa Pederzolli

Projeto completo de testes automatizados em Python para a aplicação web BugBank (https://bugbank.netlify.app/).

## Status dos Testes

- **Testes Unitários**: **18/18 PASSANDO** (100%)
- **Testes Funcionais**: **11/11 PASSANDO** (100%) - Usando Firefox/GeckoDriver

## Estrutura do Projeto

```
TRAB2/
├── requirements.txt          # Dependências
├── pytest.ini              # Configuração do pytest
├── run_tests.py            # Script de execução
├── SOLUCAO_PROBLEMAS.md    # Guia de solução de problemas
│
├── src/                    # Código-fonte para testes unitários
│   ├── user_validator.py   # Validador de usuário
│   └── transaction.py      # Lógica de transações
│
└── tests/                  # Testes automatizados
    ├── functional/         # Testes funcionais (sistema)
    │   ├── test_login.py   # 5 casos de teste
    │   └── test_registration.py  # 6 casos de teste
    └── unit/               # Testes unitários
        ├── test_user_validator.py  # 8 casos de teste
        └── test_transaction.py     # 10 casos de teste
```

## Instalação

```bash
pip install -r requirements.txt
```

## Execução

### Todos os testes:

```bash
python run_tests.py
```

### Apenas testes unitários (recomendado se ChromeDriver não estiver configurado):

```bash
pytest tests/unit/ -v
```

### Apenas testes funcionais:

```bash
pytest tests/functional/ -v
```

## Requisitos Atendidos

### Testes Funcionais (Sistema) - 11 casos

- **Cenário 1: Login** (5 casos)
- **Cenário 2: Registro** (6 casos)

### Testes Unitários - 18 casos

- **Cenário 1: Validação de Usuário** (8 casos)
- **Cenário 2: Transações Financeiras** (10 casos)

## Navegador Utilizado

O projeto usa **Firefox com GeckoDriver** para os testes funcionais. O webdriver-manager baixa automaticamente o GeckoDriver compatível.

## Relatórios

Os relatórios HTML são gerados automaticamente em `reports/` após a execução.

## Estatísticas

- **Total de Testes**: 29 casos
- **Testes Unitários**: 18 casos (100% passando)
- **Testes Funcionais**: 11 casos (100% passando com Firefox)
