# Guia de comprovação prática com Git e GitHub

Repositório remoto real: https://github.com/wblackrt/gerenciador-os-scm

## 1. Obter artefatos do remoto

Abra o **Git Bash** (Git instalado) e execute:

```bash
git config --global user.name "SEU NOME"
git config --global user.email "SEU EMAIL"
git clone https://github.com/wblackrt/gerenciador-os-scm.git
cd gerenciador-os-scm
git status
git log --oneline -5
```

Capture a tela do comando `git clone`, e a pasta clonada.

## 2. Alterar e publicar um artefato

Acrescente no final de `docs/HISTORICO.md` uma linha descrevendo sua alteração e salve. Em seguida:

```bash
git status
git add .
git commit -m "docs: registrar pratica de sincronizacao pelo Git Bash"
git push origin main
git status
```

Capture a saída dos comandos e o commit no site GitHub. Caso peça autenticação, use o navegador/Git Credential Manager, nunca compartilhe token ou senha.

## 3. Evidências para o relatório acadêmico

- Repositório remoto criado e acessível, com sua URL;
- URL HTTPS no menu **Code**;
- `git clone` e arquivos realmente obtidos no computador;
- Arquivo alterado localmente e `git status`;
- `git add .`, `git commit -m` e `git push` no Git Bash;
- Arquivo atualizado e novo commit visíveis no GitHub.

**Transparência:** a inserção inicial do projeto no GitHub foi feita pela integração de API. Ela comprova publicação remota e histórico, mas não equivale ao `git push` local exigido pelo roteiro. Esse último passo deve ser realizado no computador e documentado com capturas verdadeiras.
