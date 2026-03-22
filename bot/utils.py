"""
utils.py — Helpers: delay humano, screenshot, retry, log
"""
import random
import time
from datetime import datetime
from pathlib import Path

from loguru import logger
from playwright.sync_api import Page

from bot.config import Config


def delay_humano(minimo: float = None, maximo: float = None):
    """Aguarda um tempo aleatório para simular comportamento humano."""
    mn = minimo or Config.DELAY_MIN
    mx = maximo or Config.DELAY_MAX
    tempo = random.uniform(mn, mx)
    time.sleep(tempo)


def tirar_screenshot(page: Page, nome: str):
    """Salva um screenshot na pasta de erros com timestamp."""
    Path(Config.SCREENSHOT_DIR).mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho = f"{Config.SCREENSHOT_DIR}/{ts}_{nome}.png"
    try:
        page.screenshot(path=caminho)
        logger.warning(f"Screenshot salvo: {caminho}")
    except Exception as e:
        logger.error(f"Não foi possível salvar screenshot: {e}")


def ja_processado(telefone: str) -> bool:
    """Verifica se o aluno já foi processado em execuções anteriores."""
    path = Path(Config.PROCESSADOS_LOG)
    if not path.exists():
        return False
    return telefone in path.read_text(encoding="utf-8")


def marcar_processado(telefone: str, nome: str):
    """Registra o aluno como processado."""
    Path(Config.PROCESSADOS_LOG).parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(Config.PROCESSADOS_LOG, "a", encoding="utf-8") as f:
        f.write(f"{ts} | {telefone} | {nome}\n")


def configurar_logger():
    """Configura o loguru para salvar logs em arquivo diário."""
    Path(Config.LOG_DIR).mkdir(parents=True, exist_ok=True)
    logger.add(
        f"{Config.LOG_DIR}/bot_{{time:YYYY-MM-DD}}.log",
        rotation="00:00",
        retention="30 days",
        encoding="utf-8",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    )
