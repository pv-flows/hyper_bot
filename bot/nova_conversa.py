"""
nova_conversa.py — seletores validados via inspeção do HTML do Hyper
"""
from loguru import logger
from playwright.sync_api import Page, TimeoutError as PWTimeout

from bot.config import Config
from bot.planilha import Aluno
from bot.utils import delay_humano, tirar_screenshot

TIMEOUT = 15_000


def criar_conversa(page: Page, aluno: Aluno) -> bool:
    logger.info(f"Iniciando conversa para {aluno.nome} ({aluno.telefone})")
    try:
        _garantir_tela_limpa(page)
        _clicar_btn_nova_conversa(page)
        _selecionar_lista(page, 'input[name="department"]', Config.DEPARTAMENTO, "Departamento")
        _selecionar_lista(page, 'input[name="channel"]',    Config.CANAL,         "Canal")
        _preencher_campo(page, 'input[name="sender"]', aluno.telefone, "Telefone", tab_apos=True)
        _preencher_campo(page, 'input[name="name"]',   aluno.nome,     "Nome")
        _confirmar(page)
        # Segunda etapa: ativar conversa com template
        ativar_conversa(page, aluno)
        logger.success(f"Conversa criada: {aluno.nome} ({aluno.telefone})")
        return True
    except PWTimeout as e:
        logger.error(f"Timeout ao processar {aluno.nome}: {e}")
        tirar_screenshot(page, f"timeout_{aluno.telefone}")
        _fechar_modal(page)
        return False
    except Exception as e:
        logger.error(f"Erro ao processar {aluno.nome}: {e}")
        tirar_screenshot(page, f"erro_{aluno.telefone}")
        _fechar_modal(page)
        return False


def _clicar_btn_nova_conversa(page: Page):
    logger.debug("Clicando no botão '+'...")
    btn = page.locator("button.button-add-chat").first
    btn.wait_for(state="visible", timeout=TIMEOUT)
    delay_humano(0.5, 1.0)
    btn.click()
    # Aguarda o modal abrir confirmando que o campo department apareceu
    page.locator('input[name="department"]').wait_for(state="visible", timeout=TIMEOUT)
    delay_humano(0.8, 1.2)


def _selecionar_lista(page: Page, campo_seletor: str, valor: str, rotulo: str):
    """
    Clica no campo MUI Autocomplete, aguarda a lista abrir
    e clica na opção cujo texto contém o valor configurado.
    NÃO digita nada — a lista abre automaticamente ao clicar.
    """
    logger.debug(f"Selecionando {rotulo}: {valor}")

    campo = page.locator(campo_seletor).first
    campo.wait_for(state="visible", timeout=TIMEOUT)
    delay_humano(0.4, 0.8)
    campo.click()
    delay_humano(0.8, 1.5)

    # Aguarda qualquer opção aparecer na lista
    page.locator('li[role="option"]').first.wait_for(state="visible", timeout=TIMEOUT)
    delay_humano(0.3, 0.6)

    # Clica na opção que contém o texto correto
    opcao = page.locator(f'li[role="option"]:has-text("{valor[:20]}")').first
    opcao.wait_for(state="visible", timeout=TIMEOUT)
    opcao.click()
    delay_humano(0.5, 1.0)
    logger.debug(f"{rotulo} selecionado.")


def _preencher_campo(page: Page, seletor: str, valor: str, rotulo: str, tab_apos: bool = False):
    logger.debug(f"Preenchendo {rotulo}: {valor}")
    campo = page.locator(seletor).first
    campo.wait_for(state="visible", timeout=TIMEOUT)
    delay_humano(0.3, 0.6)
    campo.click()
    campo.fill("")
    delay_humano(0.2, 0.4)
    campo.type(valor, delay=80)
    if tab_apos:
        delay_humano(0.1, 0.2)
        campo.press("Tab")  # fecha popup de sugestão e vai para o próximo campo
    delay_humano(0.4, 0.8)


def _confirmar(page: Page):
    logger.debug("Clicando em Confirmar...")
    btn = page.locator("button#form-submit").first
    btn.wait_for(state="visible", timeout=TIMEOUT)
    delay_humano(0.5, 1.0)
    btn.click()
    
    # NOVO: Aguarda 5s para o processamento do Hyper e verificação de conflito
    # (Ex: contato já sendo atendido por outro operador)
    logger.debug("Aguardando 5s para confirmação do Hyper...")
    # Usamos delay_humano para garantir uma espera mínima exata de 5s
    delay_humano(5.0, 5.0)

    # Se o modal/botão de submit ainda estiver visível, houve erro ou conflito
    if btn.is_visible():
        logger.warning("CONFLITO DETECTADO: O contato já está sendo atendido por outro operador.")
        logger.warning("Fechando modal e pulando para o próximo aluno.")
        _fechar_modal(page)
        # Lançamos uma exceção para o criar_conversa interromper o fluxo deste aluno
        raise Exception("CONTATO_JA_EM_ATENDIMENTO")
    
    logger.debug("Confirmação realizada com sucesso.")
    delay_humano(1.0, 2.0)


def _fechar_modal(page: Page):
    try:
        page.keyboard.press("Escape")
        delay_humano(0.5, 1.0)
    except Exception:
        pass


def _garantir_tela_limpa(page: Page):
    """
    Verifica se há algum modal antigo aberto (ex: de uma execução anterior abortada)
    e pressiona ESC até fechá-lo, garantindo que a tela base (botão '+') esteja acessível.
    """
    try:
        dialogs = page.locator(".MuiDialog-root, .MuiModal-root, [role='dialog']")
        max_tentativas = 3
        
        while dialogs.first.is_visible() and max_tentativas > 0:
            logger.warning("Modal residual detectado na tela. Fechando (ESC)...")
            page.keyboard.press("Escape")
            delay_humano(0.5, 1.0)
            max_tentativas -= 1
            
        if dialogs.first.is_visible():
            logger.warning("Ainda há modais abertos após 3 tentativas de fechamento. O clique pode falhar.")
        else:
            logger.debug("Tela limpa de modais aparentes.")
            
    except Exception as e:
        logger.debug(f"Erro ignorado ao verificar modais residuais: {e}")


def ativar_conversa(page: Page, aluno: Aluno) -> bool:
    """
    Segunda etapa: clica em Ativar conversa, seleciona o template
    e preenche o nome do aluno no parâmetro {{1}}.
    """
    logger.info(f"Ativando conversa para {aluno.nome}...")
    try:
        # 1. Aguarda e clica no botão "Ativar conversa"
        btn_ativar = page.locator("button.button-send-hsm").first
        btn_ativar.wait_for(state="visible", timeout=TIMEOUT)
        delay_humano(0.8, 1.5)
        btn_ativar.click()
        delay_humano(0.8, 1.5)

        # 2. Aguarda o modal de template abrir
        page.locator('input[name="hsm"]').wait_for(state="visible", timeout=TIMEOUT)
        delay_humano(0.5, 1.0)

        # 3. Clica no campo de template para abrir a lista
        campo_hsm = page.locator('input[name="hsm"]').first
        campo_hsm.click()
        delay_humano(0.8, 1.5)

        # 4. Aguarda as opções e clica em "Início Atendimento Negociação"
        opcao = page.locator('li[role="option"]:has-text("Início Atendimento Negociação")').first
        opcao.wait_for(state="visible", timeout=TIMEOUT)
        delay_humano(0.3, 0.6)
        opcao.click()

        # 5. Rola o modal até o fim para revelar campos de parâmetro
        delay_humano(0.2, 0.4)
        page.evaluate("""
            const modal = document.querySelector('[role="dialog"]')
                       || document.querySelector('.MuiDialog-paper')
                       || document.querySelector('[class*="modal"]')
                       || document.body;
            modal.scrollTo(0, modal.scrollHeight);
        """)
        # Atraso reduzido: tempo suficiente para o renderizador do browser captar o scroll
        delay_humano(0.4, 0.7)

        # 6. Localiza e preenche o campo {{contact.name.split(' ')[0]}}
        #    Buscamos todos os possíveis seletores em um único passo via OR do Playwright
        dialog = page.locator('[role="dialog"]').first
        
        seletor_unificado = (
            'input[placeholder*="contact.name"], '
            'input[placeholder*="{{contact"], '
            'input[placeholder*="{{1}}"], '
            'input[data-index="0"], '
            'input[type="text"]:not([name="hsm"]):not([type="search"])'
        )
        
        campo_param = dialog.locator(seletor_unificado).first
        
        try:
            # Espera curta pois o modal já está aberto
            campo_param.wait_for(state="attached", timeout=2_000)
            logger.debug("Campo de parâmetro localizado com sucesso.")
        except Exception:
            raise Exception("Não foi possível localizar o campo de preenchimento do nome/matrícula.")

        campo_param.scroll_into_view_if_needed()
        delay_humano(0.1, 0.2)
        
        # force=True ignora elementos sobrepostos (prévia do template)
        campo_param.click(force=True)
        delay_humano(0.1, 0.2)
        
        # Ctrl+A seleciona o conteúdo padrão "{{contact.name.split(' ')[0]}}"
        campo_param.press("Control+a")
        
        # Valor a preencher: "Nome do Aluno - Matrícula"
        valor_param = f"{aluno.nome} - {aluno.matricula}" if aluno.matricula else aluno.nome
        logger.debug(f"Preenchendo parâmetro: '{valor_param}'")
        
        # Digitação rápida
        campo_param.type(valor_param, delay=40)
        delay_humano(0.3, 0.6)

        # 7. Clica em "Reabrir conversa"
        btn_reabrir = page.locator('button:has-text("Reabrir conversa")').first
        btn_reabrir.wait_for(state="visible", timeout=TIMEOUT)
        delay_humano(0.5, 1.0)
        btn_reabrir.click()
        page.locator('button:has-text("Reabrir conversa")').wait_for(state="hidden", timeout=TIMEOUT)
        delay_humano(1.0, 2.0)

        logger.success(f"Conversa ativada: {aluno.nome}")
        return True

    except PWTimeout as e:
        logger.error(f"Timeout ao ativar conversa para {aluno.nome}: {e}")
        tirar_screenshot(page, f"timeout_ativar_{aluno.telefone}")
        _fechar_modal(page)
        return False
    except Exception as e:
        logger.error(f"Erro ao ativar conversa para {aluno.nome}: {e}")
        tirar_screenshot(page, f"erro_ativar_{aluno.telefone}")
        _fechar_modal(page)
        return False
