"""
config.py — Carrega e valida todas as configurações do .env
"""
import os
from dotenv import load_dotenv

load_dotenv()


def _get(key: str, default=None, obrigatorio: bool = False) -> str:
    val = os.getenv(key, default)
    if obrigatorio and not val:
        raise EnvironmentError(
            f"[config] Variável obrigatória '{key}' não encontrada no .env"
        )
    return val


class Config:
    VERSAO: str = "2.2"
    
    # Login manual — sem necessidade de e-mail/senha
    HYPER_URL: str       = _get("HYPER_URL", "https://conversas.hyperflow.global/chats")
    TIMEOUT_LOGIN_MANUAL: int = int(_get("TIMEOUT_LOGIN_MANUAL", "120"))

    # Conversa
    DEPARTAMENTO: str    = _get("DEPARTAMENTO", "Negociação")
    CANAL: str           = _get("CANAL", "+55 81 9179-4459 - SER Educacional - Negociacao (Negociação)")
    TEMPLATE_NOME: str   = _get("TEMPLATE_NOME", "Início Atendimento Negociação")

    # Planilha
    PLANILHA_PATH: str   = _get("PLANILHA_PATH",    "data/filtro_alunos.xlsx")
    COLUNA_TELEFONE: str = _get("COLUNA_TELEFONE",  "A")
    COLUNA_NOME: str     = _get("COLUNA_NOME",      "B")
    COLUNA_MATRICULA: str = _get("COLUNA_MATRICULA", "C")
    LINHA_INICIO: int    = int(_get("LINHA_INICIO", "2"))

    # Navegador — Chrome real (anti-Cloudflare)
    CHROME_PATH: str       = _get("CHROME_PATH", "")
    CHROME_DEBUG_PORT: int = int(_get("CHROME_DEBUG_PORT", "9222"))

    # Comportamento
    DELAY_MIN: float    = float(_get("DELAY_MIN", "0.8"))
    DELAY_MAX: float    = float(_get("DELAY_MAX", "2.0"))
    DELAY_DIGITACAO: int = int(_get("DELAY_DIGITACAO", "80"))
    TIMEOUT_ACAO: int   = int(_get("TIMEOUT_ACAO", "15000"))
    MAX_TENTATIVAS: int = int(_get("MAX_TENTATIVAS", "3"))
    HEADLESS: bool      = _get("HEADLESS", "false").lower() == "true"

    # Pastas
    LOG_DIR: str         = "logs"
    SCREENSHOT_DIR: str  = "screenshots/erros"
    PROCESSADOS_LOG: str = "data/processados.log"
