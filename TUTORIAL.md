# 🤖 Hyper Bot — Tutorial Completo para o Usuário Final

> **Versão do documento:** 1.0 — Março 2026  
> **Plataforma alvo:** Hyperflow (conversas.hyperflow.global)  
> **Sistema operacional suportado:** Windows 10 / Windows 11

---

## 1. O que é o Hyper Bot?

O **Hyper Bot** é uma ferramenta de **automação RPA** (*Robotic Process Automation*) criada para automatizar a criação e ativação de conversas na plataforma **Hyperflow**. Ele elimina o trabalho manual repetitivo de abrir, preencher e ativar conversas para cada aluno individualmente.

### O que ele faz, na prática:

Para cada aluno listado em uma planilha Excel, o bot automaticamente:

1. Clica no botão **"+ Nova Conversa"** no Hyperflow
2. Seleciona o **Departamento** e o **Canal** configurados
3. Preenche o **telefone** e o **nome** do aluno
4. Confirma a criação da conversa
5. Clica em **"Ativar conversa"** e seleciona o template **"Início Atendimento Negociação"**
6. Preenche o parâmetro com `Nome Completo - Matrícula`
7. Clica em **"Reabrir conversa"** para finalizar

Tudo isso de forma sequencial e automática, repetindo o ciclo para todos os alunos da planilha.

---

## 2. Stack Técnica

O bot foi construído inteiramente em **Python**, utilizando as seguintes bibliotecas:

| Biblioteca | Versão | Função |
|---|---|---|
| **Playwright** | 1.44.0 | Automação do navegador (clicar, preencher, navegar) |
| **openpyxl** | 3.1.2 | Leitura da planilha Excel (`.xlsx`) |
| **python-dotenv** | 1.0.1 | Carregamento de configurações do arquivo `.env` |
| **loguru** | 0.7.2 | Sistema de logs coloridos e arquivos de log diários |

### Por que o Chrome real (e não o Playwright headless)?

> [!IMPORTANT]
> O Hyperflow utiliza **Cloudflare** como proteção anti-bot. Navegadores controlados pelo Playwright em modo "headless" (invisível) são detectados e bloqueados pelo Cloudflare. Por isso, o bot conecta ao seu **Google Chrome real** via protocolo **CDP (Chrome DevTools Protocol)**, contornando essa proteção de forma eficaz e segura.

A técnica usada é:
1. Fechar o Chrome existente (para liberar a porta de debug)
2. Reabrir o Chrome com a flag `--remote-debugging-port=9222`
3. O Playwright se conecta a esta porta via `connect_over_cdp()`
4. O Chrome usado é o **do próprio usuário**, com perfil isolado em `data/chrome_profile/`

---

## 3. Requisitos do Sistema

| Componente | Requisito |
|---|---|
| **Sistema Operacional** | Windows 10 ou Windows 11 (64-bit) |
| **Python** | Versão 3.10, 3.11 ou **3.12** (recomendado) |
| **Google Chrome** | Qualquer versão recente instalada |
| **Internet** | Conexão ativa e estável durante a execução |
| **Permissões** | Sem necessidade de administrador para executar |

> [!WARNING]
> **Evite Python 3.14 ou superior.** Essas versões são experimentais e podem exigir compilação de código C++, tornando a instalação demorada ou com falhas. Use sempre a versão **3.12 estável**.

---

## 4. Estrutura de Arquivos e Tamanhos

```
hyper_bot/
│
├── 📄 instalar.bat          (5,1 KB)  ← Instalador automático
├── 📄 Rodar Bot.bat         (148 B)   ← Atalho para executar o bot
├── 📄 requirements.txt      (70 B)    ← Lista de dependências Python
├── 📄 .env                  (1,5 KB)  ← Configurações do bot (NÃO compartilhar)
├── 📄 .env.example          (1,5 KB)  ← Modelo de configuração
├── 📄 README.md             (4,5 KB)  ← Resumo rápido
│
├── 📁 bot/                            ← Código-fonte principal
│   ├── main.py              (6,5 KB)  ← Ponto de entrada e orquestrador
│   ├── config.py            (1,7 KB)  ← Carrega configurações do .env
│   ├── login.py             (3,4 KB)  ← Lógica de detecção de login
│   ├── nova_conversa.py     (9,8 KB)  ← Automação principal (maior arquivo)
│   ├── planilha.py          (2,9 KB)  ← Leitura e normalização do Excel
│   └── utils.py             (2,0 KB)  ← Helpers: delay, screenshot, log
│
├── 📁 data/                           ← Dados do bot
│   ├── filtro_alunos.xlsx             ← Planilha de entrada (você fornece)
│   ├── processados.log                ← Controle de alunos já processados
│   └── chrome_profile/               ← Perfil isolado do Chrome (criado automaticamente)
│
├── 📁 logs/                           ← Logs diários (gerados automaticamente)
│   └── bot_2026-03-22.log
│
├── 📁 screenshots/
│   └── erros/                         ← Capturas de tela em caso de falha
│
├── 📁 venv/                           ← Ambiente virtual Python (criado pelo instalador)
└── 📁 tests/                          ← Testes automatizados (uso do desenvolvedor)
```

**Tamanho total aproximado da pasta** (sem o `venv`): ~35 KB de código  
**Tamanho total com `venv`**: ~200–400 MB (dependências Python + Playwright)

---

## 5. Ambientes em que Pode Ser Utilizado

O bot funciona em qualquer computador Windows que tenha o Chrome instalado. Abaixo estão os cenários suportados:

| Ambiente | Suportado? | Observação |
|---|---|---|
| **Windows 10 / 11 (desktop)** | ✅ Sim | Ambiente principal e recomendado |
| **Notebook corporativo** | ✅ Sim | Funciona normalmente |
| **Máquina virtual (VMware, Hyper-V)** | ⚠️ Parcial | Pode ter problemas de renderização do Chrome |
| **Windows Server** | ⚠️ Parcial | Requer Chrome instalado manualmente |
| **macOS / Linux** | ❌ Não | Os scripts `.bat` são exclusivos do Windows |
| **Chromebook / tablet** | ❌ Não | Sem suporte a Python/Chrome nativo |

> [!NOTE]
> O bot utiliza o protocolo **CDP (Chrome DevTools Protocol)** para controlar o navegador diretamente — **sem usar o mouse ou teclado do Windows**. Por isso, o Chrome pode ser **minimizado** durante a execução sem afetar o funcionamento do bot. A única exceção é o momento do **login**, quando o Chrome vem automaticamente para a frente para que você faça a autenticação.

---

## 6. Instalação Passo a Passo

### Passo 1 — Instalar o Python

1. Acesse [python.org/downloads](https://www.python.org/downloads/) e baixe o **Python 3.12**
2. Execute o instalador
3. **IMPORTANTE:** Marque a caixa `☑ Add Python to PATH` antes de clicar em "Install Now"

### Passo 2 — Copiar a pasta do bot

Copie a pasta `hyper_bot` para qualquer local do computador (Desktop, Documentos, etc.)

### Passo 3 — Executar o Instalador

Clique duas vezes no arquivo **`instalar.bat`**

O instalador irá realizar automaticamente:

| Etapa | O que faz |
|---|---|
| **[1/5]** Ambiente virtual | Cria uma pasta `venv` isolada para as dependências |
| **[2/5]** Dependências | Instala Playwright, openpyxl, loguru e python-dotenv |
| **[3/5]** Arquivo `.env` | Copia `.env.example` para `.env` (se ainda não existir) |
| **[4/5]** Atalho de execução | Cria o arquivo `Rodar Bot.bat` |

Ao final, você verá a mensagem:
```
══════════════════════════════════════════════════
          INSTALAÇÃO FINALIZADA COM SUCESSO!
══════════════════════════════════════════════════
```

> [!TIP]
> Se o instalador for executado novamente em um computador já configurado, ele detecta o ambiente existente e pula as etapas já concluídas. É seguro rodar novamente.

---

## 7. Configuração

### 7.1 — Preparar a Planilha

Coloque o arquivo **`filtro_alunos.xlsx`** dentro da pasta `data/`.

A planilha deve seguir este formato (os dados começam da **linha 2**; a linha 1 pode ser cabeçalho ou vazia):

| Coluna A | Coluna B | Coluna C |
|---|---|---|
| Telefone | Nome completo | Matrícula |
| +5581999991111 | João Silva Santos | 123456 |
| 81988882222 | Maria Oliveira | 654321 |

**Formatos de telefone aceitos:** O bot normaliza automaticamente:
- `81999991111` → vira `+5581999991111`
- `5581988882222` → vira `+5581988882222`
- `+5581977773333` → mantido como está

### 7.2 — Verificar o Arquivo `.env`

O arquivo `.env` fica na raiz da pasta `hyper_bot`. Abra-o com o Bloco de Notas e verifique:

```ini
# URL da plataforma (não alterar)
HYPER_URL=https://conversas.hyperflow.global/chats

# Departamento e Canal (devem ser exatamente como aparecem no Hyperflow)
DEPARTAMENTO=Negociação
CANAL=+55 81 9179-4459 - SER Educacional - Negociacao (Negociação)

# Caminho para a planilha
PLANILHA_PATH=data/filtro_alunos.xlsx

# Colunas da planilha
COLUNA_TELEFONE=A
COLUNA_NOME=B
COLUNA_MATRICULA=C
LINHA_INICIO=2

# Comportamento do bot
DELAY_MIN=0.8
DELAY_MAX=2.0
MAX_TENTATIVAS=3

# Porta de debug do Chrome (não alterar sem necessidade)
CHROME_DEBUG_PORT=9222
```

> [!CAUTION]
> **Nunca compartilhe** o arquivo `.env` por e-mail ou grupos. Ele contém as configurações específicas do seu ambiente. O arquivo `.env.example` é a versão segura para compartilhar.

---

## 8. Como Executar o Bot

### Execução normal

1. **Prepare a planilha** `filtro_alunos.xlsx` na pasta `data/`
2. **Clique duas vezes** em `Rodar Bot.bat`
3. O Chrome abrirá automaticamente na tela de login do Hyperflow
4. **Faça o login manualmente** no Chrome que acabou de abrir
5. Após o login, o bot detectará a interface e iniciará automaticamente

Você verá no terminal a mensagem:
```
══════════════════════════════════════════════
  🔐  FAÇA O LOGIN NO NAVEGADOR QUE ACABOU DE ABRIR
      O bot continuará automaticamente após o login.
      Você tem 120 segundos.
══════════════════════════════════════════════
```

### Durante a execução

O terminal exibirá o progresso em tempo real:
```
2026-03-22 10:30:15 | INFO    | Total de alunos na fila: 47
2026-03-22 10:30:18 | SUCCESS | Conectado ao Chrome (tentativa 1).
2026-03-22 10:30:45 | SUCCESS | Login e carregamento concluídos!
2026-03-22 10:30:46 | INFO    | Iniciando conversa para João Silva (5581999991111)
2026-03-22 10:31:02 | SUCCESS | Conversa criada: João Silva (+5581999991111)
2026-03-22 10:31:03 | SUCCESS | Conversa ativada: João Silva
```

### Ao final

```
══════════════════════════════════════════════════
RESUMO — Sucesso: 45 | Falha: 1 | Pulados: 1
══════════════════════════════════════════════════
```

- **Sucesso:** Alunos processados com êxito
- **Falha:** Alunos que não puderam ser processados (ver screenshots de erro)
- **Pulados:** Alunos já processados em execuções anteriores

---

## 9. Controle de Rexecução (Anti-Duplicatas)

O bot mantém um arquivo de controle em `data/processados.log`. Cada aluno processado com sucesso é registrado com timestamp e telefone:

```
2026-03-22 10:31:02 | +5581999991111 | João Silva Santos
2026-03-22 10:31:45 | +5581988882222 | Maria Oliveira
```

> Ao executar novamente, alunos já listados neste arquivo são automaticamente **pulados**, evitando duplicatas.

### Para reprocessar todos os alunos:

Apague o arquivo `data/processados.log` e execute o bot normalmente.

---

## 10. Como Lidar com Instabilidades

O bot possui mecanismos internos para lidar com falhas, mas algumas situações exigem intervenção manual.

### 10.1 — Contato já em atendimento

**O que acontece:** O Hyperflow exibe um conflito indicando que o contato já está sendo atendido por outro operador.

**Como o bot lida:** Detecta automaticamente o conflito (o botão "Confirmar" permanece visível após 5 segundos), fecha o modal com ESC e **pula para o próximo aluno**. O aluno conflitante é marcado como **falha** no resumo.

**O que fazer:** Processar esse aluno manualmente no Hyperflow.

---

### 10.2 — Timeout (página demorou demais)

**O que acontece:** O Hyperflow demorou mais de 15 segundos para responder a uma ação.

**Como o bot lida:** Tira um **screenshot automático** em `screenshots/erros/` com o nome do aluno e tenta fechar o modal com ESC.

**O que fazer:**
1. Verificar a conexão com a internet
2. Verificar o screenshot salvo para entender onde travou
3. Executar o bot novamente — o aluno não processado será retentado

---

### 10.3 — Chrome não conecta (porta CDP fechada)

**O que acontece:** O bot não consegue se conectar ao Chrome na porta 9222.

**Sintoma no terminal:**
```
[!] Não foi possível conectar ao Chrome após 15 tentativas.
```

**Causas e soluções:**

| Causa | Solução |
|---|---|
| Chrome já estava aberto antes de rodar o bot | Feche o Chrome manualmente e execute novamente |
| Outra aplicação usa a porta 9222 | Altere `CHROME_DEBUG_PORT=9223` no `.env` |
| Chrome não está instalado no caminho padrão | Defina `CHROME_PATH=C:\caminho\completo\chrome.exe` no `.env` |

---

### 10.4 — Login não detectado (timeout de 120s)

**O que acontece:** O bot aguarda o login por 120 segundos, mas não detectou que a interface do Hyperflow carregou.

**Causas e soluções:**

| Causa | Solução |
|---|---|
| Login demorou mais de 120s | Execute novamente e faça o login mais rapidamente |
| Internet lenta — página carregou mas o botão `+` não apareceu | Execute novamente; o bot aguarda 60s extras pelo botão `+` |
| Sessão já estava ativa mas a página travou | O bot detecta isso e força o recarregamento automaticamente |

---

### 10.5 — Modal residual da execução anterior

**O que acontece:** Se o bot foi interrompido (fechando o terminal ou com Ctrl+C) com um modal aberto no Hyperflow, ele ficará "preso".

**Como o bot lida:** Antes de processar cada aluno, o bot verifica se há modais abertos (`MuiDialog-root`) e tenta fechá-los com até **3 pressões de ESC** automaticamente.

**Se ainda persistir:** Feche o modal manualmente no Chrome antes de executar novamente.

---

### 10.6 — Erro na planilha

**Sintoma:**
```
[!] ERRO: Planilha não encontrada: data/filtro_alunos.xlsx
```
ou
```
IndexError na planilha
```

**Soluções:**

| Problema | Solução |
|---|---|
| Arquivo não está em `data/` | Mova o arquivo para `hyper_bot/data/filtro_alunos.xlsx` |
| Nome diferente de `filtro_alunos.xlsx` | Renomeie ou ajuste `PLANILHA_PATH` no `.env` |
| Planilha com menos de 3 colunas | Adicione a coluna de matrícula (pode ficar vazia, mas deve existir) |
| Arquivo aberto no Excel | Feche o Excel antes de executar o bot |

---

### 10.7 — ModuleNotFoundError

**Sintoma:**
```
ModuleNotFoundError: No module named 'playwright'
```

**Causa:** As dependências não foram instaladas (ou o `venv` está corrompido).

**Solução:** Execute o `instalar.bat` novamente.

---

## 11. Logs e Diagnóstico

### Logs diários

O bot cria um arquivo de log por dia em:
```
hyper_bot/logs/bot_2026-03-22.log
```

O log contém **todos os eventos**, incluindo mensagens de DEBUG que não aparecem no terminal:

```
2026-03-22 10:30:46 | DEBUG   | Clicando no botão '+'...
2026-03-22 10:30:47 | DEBUG   | Selecionando Departamento: Negociação
2026-03-22 10:30:48 | DEBUG   | Departamento selecionado.
2026-03-22 10:30:49 | DEBUG   | Preenchendo Telefone: +5581999991111
```

Os logs são mantidos por **30 dias** e depois apagados automaticamente.

### Screenshots de erro

Em qualquer falha, o bot salva um screenshot em:
```
hyper_bot/screenshots/erros/
```

O nome do arquivo inclui o timestamp e o telefone do aluno:
```
20260322_103102_timeout_5581999991111.png
20260322_103245_erro_ativar_5581988882222.png
```

Use essas imagens para identificar exatamente onde o bot travou.

---

## 12. Dicas de Boas Práticas

> [!TIP]
> **Antes de executar com muitos alunos**, faça um teste com 2-3 alunos para garantir que o `DEPARTAMENTO` e o `CANAL` no `.env` estão corretos.

> [!TIP]
> **O Chrome pode ser minimizado** durante a execução. O bot opera via protocolo CDP interno e não depende de foco ou visibilidade da janela. Você pode usar outros programas normalmente enquanto o bot processa.

> [!TIP]
> **Conexão instável?** Aumente os valores de delay no `.env`: `DELAY_MIN=1.5` e `DELAY_MAX=3.0`. Isso dá mais tempo para o Hyperflow responder.

> [!TIP]
> **Execute em horários de menor movimento** no Hyperflow para evitar conflitos de contatos sendo atendidos simultaneamente.

---

## 13. Perguntas Frequentes (FAQ)

**O bot salva minha senha?**  
Não. O login é inteiramente **manual**. O bot nunca armazena credenciais. Você faz o login no Chrome como faria normalmente.

**O Chrome fica aberto após o bot terminar?**  
Sim. O bot se desconecta do Chrome ao finalizar, mas **não fecha o navegador**. Você pode continuar usando o Hyperflow normalmente após a execução.

**Posso usar o computador enquanto o bot roda?**  
Sim. O bot **não usa o mouse nem o teclado do sistema operacional** — todas as ações (cliques, digitação, teclas) são enviadas diretamente ao Chrome via protocolo CDP. Você pode usar outros programas, navegar na internet e até minimizar o Chrome sem interferir na execução. O único momento em que o Chrome virá para frente automaticamente é durante o login inicial.

**O bot pode processar a mesma planilha duas vezes sem duplicar?**  
Sim. O controle de `processados.log` garante que alunos já processados sejam pulados automaticamente.

**E se eu quiser rodar para novos alunos no mesmo dia?**  
Atualize a planilha com os novos alunos (mantendo os antigos ou não) e execute novamente. Os alunos já processados serão ignorados.

**Posso mudar o template de ativação?**  
O template `"Início Atendimento Negociação"` está definido no código (`nova_conversa.py`, linha 173). Alterar requer modificação no código-fonte.

---

## 14. Resumo Visual do Fluxo

```
┌─────────────────────────────────────────────────────────┐
│                    INÍCIO DA EXECUÇÃO                   │
└───────────────────────┬─────────────────────────────────┘
                        │
              Valida planilha Excel
                        │
              Fecha Chrome existente
                        │
         Abre Chrome com --remote-debugging-port=9222
                        │
         Playwright conecta via CDP (localhost:9222)
                        │
         ┌──────────────┴──────────────┐
         │    Sessão já ativa?         │
         │  (URL contém /chats?)       │
         └──────┬──────────────────────┘
       Sim ─────┘      │ Não
    Verifica botão +   │ Navega para Hyperflow
         │             │ Aguarda login manual (120s)
         └─────────────┘
                        │
               Loop por cada aluno
                        │
           ┌────────────┴──────────────────┐
           │   Já processado? → Pula       │
           │   Não → processa              │
           └────────────────────────────────┘
                        │
           Abre modal Nova Conversa (+)
           Seleciona Departamento e Canal
           Preenche Telefone e Nome
           Confirma (aguarda 5s)
           Detecta conflito? → Pula aluno
                        │
           Clica em Ativar Conversa
           Seleciona template HSM
           Preenche Nome - Matrícula
           Clica em Reabrir conversa
                        │
           Registra em processados.log
                        │
               (próximo aluno)
                        │
┌─────────────────────────────────────────────────────────┐
│           RESUMO: Sucesso | Falha | Pulados             │
└─────────────────────────────────────────────────────────┘
```

---

*Documento gerado em 22 de março de 2026.*
