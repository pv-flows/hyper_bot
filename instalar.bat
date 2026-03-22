@echo off
setlocal

:: -----------------------------------------------------------------------------
:: HYPER BOT - INSTALADOR BLINDADO
:: Este script usa uma logica linear para evitar erros de leitura do Windows CMD
:: em pastas com caracteres especiais ou espacos.
:: -----------------------------------------------------------------------------

:: 1. Garantir diretório de trabalho correto (Resolve erro de Run as Admin)
cd /d "%~dp0"

:: 2. Configurar Titulo e Codificacao
title Hyper Bot - Instalador
chcp 65001 >nul 2>&1

:: 3. Inicio do Log Visual
echo.
echo ==========================================
echo    HYPER BOT - INSTALACAO AUTOMATICA
echo ==========================================
echo.
echo [DEBUG] Iniciando processos...
echo [DEBUG] Local: %cd%
echo.

:: 4. Detectar o Comando do Python
set "PYTHON_CMD="

:: Tenta 'python'
python --version >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_CMD=python"
    goto :python_detected
)

:: Tenta 'py' (launcher padrao do Windows)
py --version >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_CMD=py"
    goto :python_detected
)

:: Se nenhum funcionar
echo [!] ERRO CRITICO: Python nao encontrado.
echo.
echo Por favor, instale o Python 3.12 (Stable) em: https://www.python.org/
echo IMPORTANTE: Na instalacao, marque a caixa "[x] Add Python to PATH".
echo.
pause
exit /b 1

:python_detected
echo [+] Python encontrado: %PYTHON_CMD%

:: 5. Capturar Versao para Logs
for /f "tokens=2" %%v in ('%PYTHON_CMD% --version 2^>^&1') do set "PYVER=%%v"
echo [+] Versao detectada: %PYVER%

:: 6. Alerta de Versao Experimental (3.14+)
echo %PYVER% | findstr /r "^3.14 ^3.15" >nul 2>&1
if errorlevel 1 goto :version_ok
echo.
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo ATENCAO: Voce esta usando o Python %PYVER% (versao de testes).
echo Isso PODE causar erros na instalacao das bibliotecas.
echo Recomendado: Python 3.12.
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo.
pause

:version_ok

:: 7. Pular instalacao pesada se ja estiver pronto (opcional, mas o script valida de qqq forma)
:: Se o venv existe, valida se o Python base dele ainda e valido
if exist "venv\Scripts\python.exe" (
    "venv\Scripts\python.exe" --version >nul 2>&1
    if errorlevel 1 (
        echo [!] Ambiente virtual detectado, mas o Python base foi desinstalado/movido.
        echo Removendo ambiente antigo para recriar com a nova versao do Python...
        rd /s /q "venv"
        goto :start_install
    )
)

if not exist "venv\Scripts\activate.bat" goto :start_install
if not exist "Rodar Bot.bat" goto :start_install
echo [INFO] O Hyper Bot ja parece configurado nesta pasta.
echo Verificando se ha alguma atualizacao necessaria...
echo.

:start_install

:: 8. Criar Ambiente Virtual (VENV)
if exist "venv\Scripts\activate.bat" (
    echo [1/5] Ambiente virtual detectado: OK.
    goto :venv_ready
)

echo [1/5] Criando ambiente virtual (venv)...
%PYTHON_CMD% -m venv venv
if errorlevel 1 goto :erro_venv

:venv_ready

:: 9. Instalar Dependencias
echo [2/5] Instalando dependencias (isso pode levar um minuto)...
call venv\Scripts\activate.bat
if errorlevel 1 goto :erro_activate

:: Garante Pip atualizado
python -m pip install --upgrade pip --quiet

:: Instala requirements
pip install -r requirements.txt --quiet
if errorlevel 1 goto :erro_deps
echo OK.

:: 10. (Pulado: Navegador Padraosera usado)
echo [3/5] Verificando arquivo de configuracao (.env)...
if exist ".env" (
    echo .env ja existe: OK.
    goto :env_ready
)

if not exist ".env.example" (
    echo [!] Aviso: .env.example nao encontrado. Configure manualmente.
    goto :env_ready
)

copy ".env.example" ".env" >nul
echo Arquivo .env criado com sucesso.

:env_ready

:: 11. Criar o Arquivo de Execucao (Rodar Bot.bat)
echo [4/5] Criando atalho "Rodar Bot.bat"...
(
echo @echo off
echo cd /d "%%~dp0"
echo chcp 65001 ^>nul
echo title Hyper Bot
echo echo Iniciando Hyper Bot...
echo call venv\Scripts\activate.bat
echo python -m bot.main
echo pause
) > "Rodar Bot.bat"
echo OK.

:: 13. Sucesso Final
echo.
echo ======================================================
echo           INSTALACAO FINALIZADA COM SUCESSO!
echo ======================================================
echo.
echo  - Planilha de alunos: data\filtro_alunos.xlsx
echo  - Para Iniciar o Bot: Use o arquivo "Rodar Bot.bat"
echo.
echo Pressione qualquer tecla para sair.
pause >nul
exit /b 0


:: -----------------------------------------------------------------------------
:: SECAO DE ERROS (Rotinas de Saida)
:: -----------------------------------------------------------------------------

:erro_venv
echo.
echo [!] ERRO: Falha ao criar a pasta "venv".
echo Verifique se voce tem permissao para escrever nesta pasta.
pause
exit /b 1

:erro_activate
echo.
echo [!] ERRO: O Windows nao permitiu ativar o venv.
pause
exit /b 1

:erro_deps
echo.
echo [!] ERRO: Falha ao instalar as bibliotecas (requirements.txt).
echo Verifique sua internet ou se o Python 3.12 esta instalado.
pause
exit /b 1

:: :erro_pw
:: echo.
:: echo [!] ERRO: Falha ao baixar o navegador do Playwright.
:: pause
:: exit /b 1
