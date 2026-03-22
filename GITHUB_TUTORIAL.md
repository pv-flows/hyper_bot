# 🐙 Tutorial — Publicar o Hyper Bot no GitHub

> Guia passo a passo para subir o projeto do zero ao GitHub.

---

## Pré-requisitos

| Item | Verificação |
|---|---|
| **Conta no GitHub** | [github.com](https://github.com) — crie uma se não tiver |
| **Git instalado** | Execute `git --version` no terminal. Se não funcionar, instale em [git-scm.com](https://git-scm.com/download/win) |

---

## Passo 1 — Criar o repositório no GitHub

1. Acesse [github.com/new](https://github.com/new)
2. Preencha:
   - **Repository name:** `hyper_bot` (ou o nome que preferir)
   - **Description:** `Bot RPA para automação de conversas no Hyperflow`
   - **Visibility:** `Private` ← recomendado, pois o projeto é interno
   - **NÃO marque** "Add a README file" (já temos um)
3. Clique em **"Create repository"**
4. Copie a URL do repositório que o GitHub exibirá (ex: `https://github.com/seu-usuario/hyper_bot.git`)

---

## Passo 2 — Abrir o terminal na pasta do projeto

Abra o **PowerShell** ou **Prompt de Comando** e navegue até a pasta:

```powershell
cd "d:\Área de Trabalho\hyper_bot"
```

> **Dica:** No Windows Explorer, clique com o botão direito dentro da pasta `hyper_bot` e escolha **"Abrir no Terminal"** ou **"Git Bash Here"**.

---

## Passo 3 — Inicializar o Git

Execute os comandos um por vez:

```bash
# Inicializa o repositório Git local
git init

# Configura seu nome e e-mail (apenas na primeira vez no computador)
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

---

## Passo 4 — Adicionar e confirmar os arquivos

```bash
# Adiciona todos os arquivos (respeitando o .gitignore)
git add .

# Verifica o que será enviado
git status

# Cria o primeiro commit
git commit -m "feat: versão inicial do Hyper Bot"
```

> O `.gitignore` está configurado para **não enviar** automaticamente:
> - `venv/` (ambiente Python — muito pesado, recriado pelo `instalar.bat`)
> - `logs/` e `screenshots/`
> - `data/processados.log` (log interno de execução — gerado a cada uso)
> - `data/chrome_profile/` (perfil do Chrome — gerado automaticamente, pode chegar a centenas de MB)
> - `Rodar Bot.bat` (gerado automaticamente pelo `instalar.bat`)
>
> Como o repositório é **privado**, `.env` e `data/filtro_alunos.xlsx` serão incluídos normalmente.

---

## Passo 5 — Conectar ao GitHub e enviar

```bash
# Conecta o repositório local ao GitHub
# (substitua pela URL copiada no Passo 1)
git remote add origin https://github.com/seu-usuario/hyper_bot.git

# Renomeia a branch principal para 'main'
git branch -M main

# Envia o projeto para o GitHub
git push -u origin main
```

O GitHub abrirá uma janela para você **fazer login** (ou pedir um token). Siga as instruções na tela.

---

## Passo 6 — Verificar

Acesse `https://github.com/seu-usuario/hyper_bot` no navegador. O projeto deverá estar lá com todos os arquivos.

---

## Envios futuros (após alterações no código)

Sempre que fizer mudanças e quiser atualizar o GitHub:

```bash
git add .
git commit -m "fix: descrição do que foi alterado"
git push
```

---

## Clonar o projeto em outro computador

Para instalar o bot em uma nova máquina a partir do GitHub:

```bash
# Baixa o projeto
git clone https://github.com/seu-usuario/hyper_bot.git

# Entra na pasta
cd hyper_bot
```

Depois:
1. Crie o arquivo `.env` a partir do `.env.example` (o `.env` não é enviado ao GitHub por segurança)
2. Execute `instalar.bat` normalmente

---

## Arquivos que o GitHub NÃO receberá

| Arquivo / Pasta | Motivo |
|---|---|
| `venv/` | Ambiente Python muito pesado — recriado pelo `instalar.bat` |
| `data/processados.log` | Log local de execução — gerado a cada uso |
| `data/chrome_profile/` | Perfil isolado do Chrome — gerado automaticamente pelo bot no primeiro uso, pode ter centenas de MB e contém cookies de sessão |
| `logs/` | Logs de execução |
| `screenshots/` | Capturas de erro |
| `Rodar Bot.bat` | Gerado automaticamente pelo `instalar.bat` |

> **`.env` e `data/filtro_alunos.xlsx` são versionados** pois o repositório é privado.
