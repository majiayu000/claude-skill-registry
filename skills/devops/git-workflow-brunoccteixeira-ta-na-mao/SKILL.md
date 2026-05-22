---
name: git-workflow
description: Automacao de operacoes git
---

## Criar Nova Branch
```bash
# Feature
git checkout -b feat/nome-da-feature

# Bug fix
git checkout -b fix/descricao-do-bug

# Documentacao
git checkout -b docs/o-que-documenta
```

## Commit Atomico
```bash
# Adicionar arquivos especificos (preferivel)
git add backend/app/services/novo_servico.py
git add backend/tests/test_novo_servico.py

# Commit com mensagem descritiva
git commit -m "feat: Adiciona servico de consulta de BPC

- Implementa consulta por CPF
- Adiciona cache Redis
- Inclui testes unitarios"
```

## Padroes de Mensagem

| Prefixo | Uso |
|---------|-----|
| `feat:` | Nova funcionalidade |
| `fix:` | Correcao de bug |
| `docs:` | Documentacao |
| `refactor:` | Refatoracao sem mudar comportamento |
| `test:` | Adicao/correcao de testes |
| `chore:` | Manutencao (deps, configs) |

## Sincronizar com Main
```bash
# Fetch das mudancas remotas
git fetch origin

# Rebase na main (preferivel a merge)
git rebase origin/main

# Se houver conflitos
git status                    # Ver arquivos em conflito
# Resolver manualmente
git add <arquivos>
git rebase --continue
```

## Push e PR
```bash
# Push da branch
git push -u origin feat/nome-da-feature

# Criar PR
gh pr create --title "feat: Titulo" --body "Descricao"

# Ver status do PR
gh pr status
```

## Desfazer Mudancas

### Ultimo commit (nao pushado)
```bash
git reset --soft HEAD~1  # Mantem mudancas staged
git reset --hard HEAD~1  # Descarta mudancas (cuidado!)
```

### Arquivo especifico
```bash
git checkout -- caminho/arquivo.py
```

### Mudancas staged
```bash
git reset HEAD caminho/arquivo.py
```

## Stash (guardar temporariamente)
```bash
# Guardar
git stash push -m "WIP: descricao"

# Listar
git stash list

# Recuperar
git stash pop
```

## Ver Historico
```bash
# Commits recentes
git log --oneline -10

# Commits da branch atual vs main
git log origin/main..HEAD --oneline

# Mudancas de um arquivo
git log --follow -p -- caminho/arquivo.py
```

## Aliases Uteis
```bash
# Adicionar no ~/.gitconfig
[alias]
    st = status
    co = checkout
    br = branch
    cm = commit -m
    lg = log --oneline -10
```
