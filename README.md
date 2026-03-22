# 🤖 Hyper Bot — Manual de Instalação e Uso

Bot RPA para automação de criação e ativação de conversas no Hyperflow.  
Conecta ao seu Google Chrome real (evita bloqueio do Cloudflare) e processa uma lista de alunos automaticamente.

---

## 📋 Pré-requisitos

| Requisito | Versão recomendada |
|---|---|
| Python | 3.11 ou **3.12** (Estável) |
| Google Chrome | Qualquer versão recente |
| Windows | 10 ou 11 |

> [!IMPORTANT]
> **Evite o Python 3.14 ou superior:** Estas são versões de teste/experimental que exigem ferramentas de compilação C++ pesadas. Use o **Python 3.12** para uma instalação rápida de um clique.

---

## 🚀 Instalação Rápida (Recomendado)

Se você está em um computador novo, siga estes passos:

1. Instale o **Python 3.10+** em [python.org](https://www.python.org/downloads/) (marque **"Add Python to PATH"**).
2. Copie a pasta do bot para o computador.
3. Clique duas vezes no arquivo **`instalar.bat`**.
4. Aguarde a conclusão. Ele criará o atalho **`Rodar Bot.bat`** automaticamente.

---

## ⚙️ Configuração

### 1. Preparar a planilha
Coloque o arquivo `filtro_alunos.xlsx` dentro da pasta `data/`.  
A planilha deve ter o seguinte formato (sem cabeçalho, dados a partir da linha 2):

| Coluna A | Coluna B | Coluna C |
|---|---|---|
| Telefone | Nome completo | Matrícula |

### 2. Verificar o arquivo `.env`
O instalador cria um arquivo `.env` para você. Abra-o com o Bloco de Notas e confirme se `DEPARTAMENTO` e `CANAL` coincidem com o que aparece no seu Hyperflow.

---

## ▶️ Como executar o bot

Basta clicar duas vezes no arquivo:
**`Rodar Bot.bat`**

### O que o bot faz:
1. Abre o Google Chrome.
2. Aguarda **você fazer login manualmente** (timeout de 120s).
3. Começa o processamento automático assim que detectar o login.
4. Ao final, mostra um resumo de Sucesso/Falha.

### O que acontece ao rodar:

1. O bot fecha qualquer Chrome aberto e abre um novo
2. Navega automaticamente para o Hyperflow
3. Exibe uma mensagem pedindo para **você fazer login manualmente**
4. Após o login, o bot detecta e começa a processar os alunos automaticamente:
   - Abre nova conversa (`+`)
   - Seleciona Departamento e Canal
   - Preenche telefone e nome
   - Confirma a criação
   - Clica em "Ativar conversa"
   - Seleciona o template "Início Atendimento Negociação"
   - Preenche o parâmetro com `Nome Completo - Matrícula`
   - Clica em "Reabrir conversa"
5. Repete para cada aluno da planilha
6. Exibe o resumo: `Sucesso: X | Falha: X | Pulados: X`

---

## 🔁 Execuções seguintes (mesmo dia)

Se o bot já foi executado hoje e você quer rodar novamente para novos alunos:

1. Atualize a planilha com os novos alunos
2. Execute normalmente: `python -m bot.main`

> Alunos já processados são automaticamente ignorados (controle interno).  
> Para reprocessar todos, apague o arquivo `data/processados.json` (se existir).

---

## 🖼️ Screenshots de erro

Em caso de falha em um aluno, o bot salva automaticamente uma captura de tela em:

```
hyper_bot/screenshots/erros/
```

Use essas imagens para identificar o que travou.

---

## ❓ Problemas comuns

| Problema | Solução |
|---|---|
| `Chrome não encontrado` | Verifique se o Chrome está instalado no local padrão |
| `Não foi possível conectar ao Chrome` | Feche manualmente qualquer Chrome aberto e tente novamente |
| `Login não detectado` | Faça o login rapidamente após a janela abrir (timeout: 120s) |
| `Timeout ao processar aluno` | A página demorou — verifique a internet e tente novamente |
| `IndexError na planilha` | Verifique se a planilha tem as 3 colunas (A, B, C) |
| `ModuleNotFoundError` | Execute `pip install -r requirements.txt` novamente |

---

## 📁 Estrutura do projeto

```
hyper_bot/
├── bot/
│   ├── main.py           ← ponto de entrada
│   ├── config.py         ← configurações via .env
│   ├── login.py          ← aguarda login manual
│   ├── nova_conversa.py  ← automação principal
│   ├── planilha.py       ← leitura da planilha Excel
│   └── utils.py          ← funções auxiliares
├── data/
│   └── filtro_alunos.xlsx   ← planilha de alunos
├── screenshots/
│   └── erros/               ← capturas em caso de falha
├── .env                     ← configurações (não compartilhar)
├── .env.example             ← modelo de configuração
└── requirements.txt         ← dependências Python
```
