"""
tests/test_planilha.py — Testes de leitura da planilha
Execute com: python -m pytest tests/
"""
import os
import pytest
from unittest.mock import patch, MagicMock
from bot.planilha import _col_para_indice, Aluno


def test_col_para_indice_simples():
    assert _col_para_indice("A") == 1
    assert _col_para_indice("B") == 2
    assert _col_para_indice("Z") == 26


def test_col_para_indice_dupla():
    assert _col_para_indice("AA") == 27
    assert _col_para_indice("AB") == 28


def test_col_minuscula():
    assert _col_para_indice("a") == 1
    assert _col_para_indice("b") == 2


def test_aluno_dataclass():
    aluno = Aluno(telefone="+5581999999999", nome="João Silva", linha=2)
    assert aluno.telefone == "+5581999999999"
    assert aluno.nome == "João Silva"
    assert aluno.linha == 2
