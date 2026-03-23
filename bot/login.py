"""
login.py — Login MANUAL no Hyper (Hyperflow)

O bot abre o navegador na página de login e aguarda o usuário
fazer o login manualmente. Quando detecta que a tela de chats
carregou, continua automaticamente.
"""
from loguru import logger
from playwright.sync_api import Page, TimeoutError as PWTimeout

from bot.config import Config


def fazer_login(page: Page) -> bool:
    """
    Abre o Hyper e aguarda o usuário fazer login manualmente.
    Retorna True quando a URL muda para /chats (prova de login).
    """
    try:
        page.bring_to_front()
    except Exception:
        pass
        
    logger.info("Abrindo o Hyper no navegador...")
    # Já estava logado e a página atual é válida?
    if "/chats" in page.url:
        logger.info("URL atual já é /chats. Verificando se a página está pronta...")
        try:
            # Tenta encontrar o botão com um timeout curto (aba pode estar morta ou recarregando)
            btn = page.locator("button.button-add-chat").first
            btn.wait_for(state="visible", timeout=5_000)
            logger.success("Sessão já ativa e página pronta. Continuando automaticamente.")
            return True
        except Exception:
            logger.warning("URL é /chats, mas a página não responde ou está vazia. Forçando recarregamento...")
            page.goto(Config.HYPER_URL, wait_until="domcontentloaded", timeout=30_000)
    else:
        # Se não estava em /chats, navega e aguarda
        page.goto(Config.HYPER_URL, wait_until="domcontentloaded", timeout=30_000)

    # Instrução clara no terminal para o operador
    print("\n" + "=" * 55)
    print("  🔐  FAÇA O LOGIN NO NAVEGADOR QUE ACABOU DE ABRIR")
    print("      O bot continuará automaticamente após o login.")
    print(f"      Você tem {Config.TIMEOUT_LOGIN_MANUAL} segundos.")
    print("=" * 55 + "\n")

    logger.info(f"Aguardando login manual (timeout: {Config.TIMEOUT_LOGIN_MANUAL}s)...")
    logger.info(f"URL atual (login): {page.url}")

    try:
        # 1. Aguarda a URL mudar para /chats (sinal inicial de login OK)
        page.wait_for_url(
            "**/chats**",
            timeout=Config.TIMEOUT_LOGIN_MANUAL * 1000
        )
        logger.info("URL /chats detectada. Aguardando interface carregar...")

        # 2. NOVO: Ponto de falha corrigido.
        # A nova interface do Hyper abre /chats mas demora para descarregar a tela branca.
        # Aguardamos até 60s para o botão "+" de Nova Conversa aparecer.
        btn_nova_conversa = page.locator("button.button-add-chat").first
        btn_nova_conversa.wait_for(state="visible", timeout=60_000)

        # Login concluído e interface totalmente carregada
        print("\n✅  Interface carregada! O bot vai iniciar agora.\n")
        logger.success(f"Login e carregamento concluídos! URL: {page.url}")
        return True

    except PWTimeout as e:
        logger.error(
            f"Timeout aguardando login ou carregamento da tela: {e}. "
            f"URL atual: {page.url} — Verifique se a página carregou corretamente."
        )
        return False
    except Exception as e:
        logger.error(f"Erro no processo de login/carregamento: {e}")
        return False


def _esta_logado(page: Page) -> bool:
    """Verifica se a sessão já está ativa pela URL."""
    return "/chats" in page.url
