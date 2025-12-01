"""
Script para executar todos os testes e gerar relatórios
"""

import subprocess
import sys
import os
from datetime import datetime


def create_reports_dir():
    """Cria o diretório de relatórios se não existir"""
    if not os.path.exists('reports'):
        os.makedirs('reports')


def run_tests():
    """Executa todos os testes"""
    create_reports_dir()
    
    print("=" * 60)
    print("Executando Testes Automatizados - BugBank")
    print("=" * 60)
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    # Executa testes unitários
    print("1. Executando Testes Unitários...")
    print("-" * 60)
    result_unit = subprocess.run(
        ["pytest", "tests/unit/", "-v", "--tb=short", "--html=reports/unit_report.html", "--self-contained-html"],
        capture_output=True,
        text=True
    )
    print(result_unit.stdout)
    if result_unit.stderr:
        print("Erros:", result_unit.stderr)
    print()
    
    # Executa testes funcionais
    print("2. Executando Testes Funcionais (Sistema)...")
    print("-" * 60)
    result_functional = subprocess.run(
        ["pytest", "tests/functional/", "-v", "--tb=short", "--html=reports/functional_report.html", "--self-contained-html"],
        capture_output=True,
        text=True
    )
    print(result_functional.stdout)
    if result_functional.stderr:
        print("Erros:", result_functional.stderr)
    print()
    
    # Executa todos os testes e gera relatório geral
    print("3. Executando Todos os Testes e Gerando Relatório Geral...")
    print("-" * 60)
    result_all = subprocess.run(
        ["pytest", "tests/", "-v", "--tb=short", "--html=reports/report.html", "--self-contained-html"],
        capture_output=True,
        text=True
    )
    print(result_all.stdout)
    if result_all.stderr:
        print("Erros:", result_all.stderr)
    print()
    
    # Resumo
    print("=" * 60)
    print("RESUMO DA EXECUÇÃO")
    print("=" * 60)
    print(f"Testes Unitários: {'✓ PASSOU' if result_unit.returncode == 0 else '✗ FALHOU'}")
    print(f"Testes Funcionais: {'✓ PASSOU' if result_functional.returncode == 0 else '✗ FALHOU'}")
    print(f"Todos os Testes: {'✓ PASSOU' if result_all.returncode == 0 else '✗ FALHOU'}")
    print()
    print("Relatórios gerados em:")
    print("  - reports/report.html (relatório geral)")
    print("  - reports/unit_report.html (testes unitários)")
    print("  - reports/functional_report.html (testes funcionais)")
    print("=" * 60)
    
    return result_all.returncode == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)

