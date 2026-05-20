---
name: auto-branch
description: |
  Automacao de criacao de branches baseado em tipo de trabalho.
  Integra com SpecKit para criar branches automaticamente ao iniciar features.
  Use quando: iniciar novo trabalho, criar feature, corrigir bug.
allowed-tools:
  - Bash
  - Read
  - Write
user-invocable: true
---

# Auto-Branch Skill

## Proposito

Esta skill automatiza a criacao de branches seguindo convencoes de nomenclatura.

## Padroes de Branch

| Tipo | Padrao | Exemplo |
|------|--------|---------|
| Bug Fix | `fix/{descricao}` | `fix/timeout-conexao-api` |
| Hotfix | `hotfix/{descricao}` | `hotfix/seguranca-sql-injection` |
| Feature | `feature/{nome}` | `feature/exportacao-pdf` |
| Release | `release/v{versao}` | `release/v1.2.0` |
| Chore | `chore/{descricao}` | `chore/atualizar-dependencias` |
| Refactor | `refactor/{descricao}` | `refactor/separar-camadas` |
| Docs | `docs/{descricao}` | `docs/api-reference` |

## Uso

### Via Hook

O hook `.claude/hooks/auto-branch.sh` e chamado automaticamente:

```bash
.claude/hooks/auto-branch.sh feature "exportacao de duplicatas"
# Cria: feature/exportacao-de-duplicatas
```

### Via Comando

```
/auto-branch feature "nome da feature"
/auto-branch fix "descricao do bug"
```

## Integracao com SDLC

### Level 0 (Quick Flow)

Quando detectado bug fix ou hotfix:

```yaml
trigger: "fix: " ou "hotfix: " no inicio da descricao
action: auto-branch.sh fix "{descricao}"
```

### Level 1 (Feature)

Quando detectada nova feature:

```yaml
trigger: "feat: " ou "feature: " no inicio da descricao
action: auto-branch.sh feature "{descricao}"
```

### Level 2+ (SDLC Completo)

Quando iniciado SDLC completo:

```yaml
trigger: /sdlc-start com nivel >= 2
action: auto-branch.sh feature "{project-id}"
```

## Integracao com SpecKit

Ao executar `/spec-create`, a branch e criada automaticamente:

```yaml
spec_create_flow:
  1. Detectar nome da spec
  2. Executar: auto-branch.sh feature "{spec-name}"
  3. Criar arquivo da spec
  4. Registrar no manifest do projeto
```

## Validacoes

- Nome normalizado (lowercase, sem espacos)
- Limite de 50 caracteres
- Sem caracteres especiais
- Branch nao existe (ou faz checkout se existir)

## Script

O script principal esta em `.claude/hooks/auto-branch.sh`.

### Exemplo de Uso

```bash
# Criar branch de feature
.claude/hooks/auto-branch.sh feature "Exportacao de Duplicatas em PDF"
# Resultado: feature/exportacao-de-duplicatas-em-pdf

# Criar branch de fix
.claude/hooks/auto-branch.sh fix "Timeout na conexao com CERC"
# Resultado: fix/timeout-na-conexao-com-cerc

# Criar branch de release
.claude/hooks/auto-branch.sh release "1.2.0"
# Resultado: release/v1.2.0
```

## Configuracao no settings.json

Para habilitar criacao automatica de branches, adicione ao settings.json:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write(*.spec.md)",
      "hooks": [{
        "type": "command",
        "command": ".claude/hooks/auto-branch.sh feature $(basename $TOOL_INPUT_FILE_PATH .spec.md)"
      }]
    }]
  }
}
```

## Troubleshooting

### Branch ja existe

Se a branch ja existir, o script faz checkout automaticamente.

### Mudancas nao commitadas

O script avisa se houver mudancas nao commitadas, mas nao bloqueia a operacao.

### Nome muito longo

Nomes sao truncados em 50 caracteres para evitar problemas.
