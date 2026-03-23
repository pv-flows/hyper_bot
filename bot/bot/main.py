"""
main.py — Ponto de entrada do bot Hyper
Uso: python -m bot.main
"""
import sys
import os
import time
import subprocess
import urllib.request
from pathlib import Path
from loguru import logger
from playwright.sync_api import sync_playwright

from bot.config import Config
from bot.login import fazer_login
from bot.nova_conversa import criar_conversa
from bot.planilha import carregar_alunos
from bot.utils import (
    configurar_logger,
    delay_humano,
    ja_processado,
    marcar_processado,
)


def get_chrome_path() -> str:
    """Localiza o executável do Chrome. Prioriza CHROME_PATH do .env."""
    if Config.CHROME_PATH and os.path.exists(Config.CHROME_PATH):
        return Config.CHROME_PATH

    paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    ]
    for p in paths:
        if os.path.exists(p):
            return p

    logger.error(
        "Google Chrome não encontrado nos caminhos padrão.\n"
        "Informe o caminho completo no .env: CHROME_PATH=C:\\...\\chrome.exe"
    )
    sys.exit(1)


def fechar_chrome_existente():
    """
    Encerra qualquer instância do Chrome antes de abrir com debug remoto.
    Necessário para liberar a porta 9222 — o Chrome normal não expõe CDP.
    """
    try:
        subprocess.run(
            ["taskkill", "/f", "/im", "chrome.exe"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        for _ in range(10):
            filtro = subprocess.run(["tasklist", "/fi", "imagename eq chrome.exe"], capture_output=True, text=True)
            if "chrome.exe" not in filtro.stdout.lower():
                break
            time.sleep(0.5)
        logger.info("Instâncias anteriores do Chrome encerradas.")
    except Exception as e:
        logger.warning(f"Erro ao tentar fechar o Chrome: {e}")


def main():
    configurar_logger()
    logger.info("=" * 50)
    logger.info("BOT HYPER — Iniciando")
    logger.info("=" * 50)

    # Valida planilha antes de abrir o navegador
    try:
        alunos = list(carregar_alunos())
    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)

    if not alunos:
        logger.warning("Nenhum aluno encontrado na planilha. Encerrando.")
        sys.exit(0)

    logger.info(f"Total de alunos na fila: {len(alunos)}")

    # Localiza e abre o Chrome com debug remoto
    logger.info("Localizando Google Chrome...")
    chrome_path = get_chrome_path()
    logger.info(f"Chrome encontrado: {chrome_path}")

    fechar_chrome_existente()

    # Perfil isolado do bot — garante instância independente no Windows
    chrome_user_data = Path("data") / "chrome_profile"
    chrome_user_data.mkdir(parents=True, exist_ok=True)

    logger.info(f"Abrindo Chrome com debug remoto na porta {Config.CHROME_DEBUG_PORT}...")
    subprocess.Popen(
        [
            chrome_path,
            f"--remote-debugging-port={Config.CHROME_DEBUG_PORT}",
            f"--user-data-dir={chrome_user_data.resolve()}",
            "--no-first-run",
            "--no-default-browser-check",
            "--start-maximized",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    logger.info("Aguardando Chrome inicializar...")

    sucesso = 0
    falha   = 0
    pulados = 0

    with sync_playwright() as pw:
        logger.info("Conectando Playwright ao Chrome...")
        browser = None
        cdp_url = f"http://localhost:{Config.CHROME_DEBUG_PORT}"
        for tentativa in range(1, 16):
            try:
                # Diagnóstico rápido antes de tentar o CDP
                urllib.request.urlopen(f"{cdp_url}/json/version", timeout=2)
            except Exception as e:
                logger.debug(f"Tentativa {tentativa}/15 — porta CDP ainda fechada: {e}")
                time.sleep(1.5)
                continue

            try:
                browser = pw.chromium.connect_over_cdp(cdp_url)
                logger.success(f"Conectado ao Chrome (tentativa {tentativa}).")
                break
            except Exception as e:
                logger.debug(f"Tentativa {tentativa}/15 — erro CDP: {e}")
                time.sleep(1.5)

        if not browser:
            logger.error(
                f"Não foi possível conectar ao Chrome após 15 tentativas.\n"
                f"Teste manualmente: curl {cdp_url}/json/version\n"
                "Se não retornar JSON, o Chrome não foi aberto com debug remoto."
            )
            sys.exit(1)

        context = browser.contexts[0] if browser.contexts else browser.new_context()
        
        # Procura se já existe uma aba do Hyper aberta para reaproveitar
        page = None
        for p in context.pages:
            if "hyperflow" in p.url:
                page = p
                break
                
        if not page:
            page = context.pages[0] if context.pages else context.new_page()
            
        # Garante que a página sendo controlada venha para a frente (foco visual do usuário)
        try:
            page.bring_to_front()
        except Exception:
            pass

        # Login manual — bot aguarda o usuário logar no Chrome
        if not fazer_login(page):
            logger.critical("Falha no login. Encerrando.")
            sys.exit(1)

        # Loop principal
        for aluno in alunos:
            if ja_processado(aluno.telefone):
                logger.info(f"Pulando (já processado): {aluno.nome}")
                pulados += 1
                continue

            tentativa = 0
            ok = False

            while tentativa < Config.MAX_TENTATIVAS and not ok:
                tentativa += 1
                if tentativa > 1:
                    logger.warning(f"Tentativa {tentativa}/{Config.MAX_TENTATIVAS} para {aluno.nome}")
                    delay_humano(2.0, 4.0)

                ok = criar_conversa(page, aluno)

            if ok:
                marcar_processado(aluno.telefone, aluno.nome)
                sucesso += 1
            else:
                logger.error(f"Falhou após {Config.MAX_TENTATIVAS} tentativas: {aluno.nome}")
                falha += 1

            delay_humano(Config.DELAY_MIN, Config.DELAY_MAX)

        # Desconecta sem fechar o Chrome — usuário pode continuar usando
        try:
            browser.close()
        except Exception:
            pass

    logger.info("=" * 50)
    logger.info(f"RESUMO — Sucesso: {sucesso} | Falha: {falha} | Pulados: {pulados}")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()
