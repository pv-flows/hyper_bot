"""
login.py — Login MANUAL no Hyper (Hyperflow)

O bot abre o navegador e aguarda silenciosamente o usuário
navegar para a URL correta e fazer o login. Quando detecta que a tela de chats
carregou e o botão de nova conversa está visível, continua automaticamente.
"""
import time
from loguru import logger
from playwright.sync_api import BrowserContext, Page

from bot.config import Config


def fazer_login(context: BrowserContext) -> Page | None:
    """
    Aguarda silenciosamente o usuário navegar para a URL correta em qualquer aba
    e o botão de nova conversa ficar visível. Retorna a Page correspondente.
    """
    print("\n" + "=" * 55)
    print("  🚀  AGUARDANDO O OPERADOR")
    print("      Navegue manualmente até o Hyperflow (https://conversas.hyperflow.global/chats)")
    print("      O bot iniciará automaticamente quando a tela estiver pronta.")
    print(f"      Tempo limite de espera: {Config.TIMEOUT_LOGIN_MANUAL} segundos.")
    print("=" * 55 + "\n")

    logger.info("Aguardando navegação manual ou login...")

    inicio = time.time()
    limite = inicio + Config.TIMEOUT_LOGIN_MANUAL

    while time.time() < limite:
        for page in context.pages:
            try:
                if "/chats" in page.url:
                    btn = page.locator("button.button-add-chat").first
                    if btn.is_visible():
                        try:
                            page.bring_to_front()
                        except Exception:
                            pass
                        print("\n✅  Interface carregada! O bot vai iniciar agora.\n")
                        logger.success(f"Página pronta e botão detectado! URL atual: {page.url}")
                        return page
            except Exception as e:
                logger.debug(f"Aguardando renderização da página (erro temporário no polling ignorado): {e}")
        
        time.sleep(1)

    logger.error(f"Timeout de {Config.TIMEOUT_LOGIN_MANUAL}s atingido aguardando o Hyperflow.")
    return None
