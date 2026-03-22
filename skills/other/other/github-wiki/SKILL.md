---
name: github-wiki
description: |
  Sincroniza documentacao com GitHub Wiki via Git.
  Publica ADRs, docs de arquitetura e API automaticamente.
  Use quando: publicar ADR, sincronizar docs apos release.
allowed-tools:
  - Read
  - Write
  - Bash
user-invocable: false
version: "1.0.0"
---

# GitHub Wiki Skill

Skill para sincronizacao de documentacao com GitHub Wiki.

## Objetivo

Automatizar publicacao de documentacao do projeto na GitHub Wiki,
incluindo ADRs, documentos de arquitetura e API.

## Realidade Tecnica

GitHub Wiki nao tem API REST/GraphQL. Funciona como repositorio Git separado:
- URL: `https://github.com/{owner}/{repo}.wiki.git`
- Arquivos Markdown sao convertidos em paginas
- Estrutura de diretorios cria hierarquia

## Pre-requisitos

- GitHub CLI (`gh`) instalado e autenticado
- Permissao de escrita no repositorio
- Wiki habilitada no repositorio (Settings > Features > Wikis)
- **IMPORTANTE**: Wiki deve ter pelo menos uma pagina criada manualmente (Home)

## Scripts Disponiveis

### wiki_sync.sh

Sincroniza documentacao completa com a Wiki.

```bash
# Sincronizacao completa
.claude/skills/github-wiki/scripts/wiki_sync.sh

# Sincronizacao com verbose
.claude/skills/github-wiki/scripts/wiki_sync.sh --verbose

# Dry run (mostra o que seria feito)
.claude/skills/github-wiki/scripts/wiki_sync.sh --dry-run
```

### publish_adr.sh

Publica um ADR especifico na Wiki.

```bash
# Publicar ADR especifico
.claude/skills/github-wiki/scripts/publish_adr.sh .agentic_sdlc/corpus/nodes/decisions/adr-001.yml

# Publicar todos os ADRs
.claude/skills/github-wiki/scripts/publish_adr.sh --all
```

## Documentos Publicados

| Documento | Fonte | Destino Wiki | Trigger |
|-----------|-------|--------------|---------|
| Home | Auto-gerado | Home.md | Cada sync |
| ADRs | `.agentic_sdlc/corpus/nodes/decisions/*.yml` | ADRs/ADR-NNN.md | `/adr-create`, Phase 7 |
| Arquitetura | `.agentic_sdlc/projects/*/docs/ARCHITECTURE.md` | Architecture.md | Phase 3, Phase 7 |
| API Docs | `.agentic_sdlc/projects/*/docs/API.md` | API-Reference.md | Phase 7 |
| README | `.agentic_sdlc/projects/*/docs/README.md` | Getting-Started.md | Phase 7 |

## Estrutura da Wiki

```
wiki/
├── Home.md                    # Pagina inicial com indice
├── Getting-Started.md         # README do projeto
├── Architecture.md            # Visao geral da arquitetura
├── API-Reference.md           # Documentacao da API
├── ADRs/
│   ├── _Sidebar.md           # Sidebar com lista de ADRs
│   ├── ADR-001.md            # ADR individual
│   ├── ADR-002.md
│   └── ...
└── _Sidebar.md               # Sidebar global
```

## Template Home.md

```markdown
# {Project Name}

Documentacao do projeto gerada automaticamente pelo SDLC Agentico.

## Navegacao

- [Getting Started](Getting-Started)
- [Architecture](Architecture)
- [API Reference](API-Reference)
- [ADRs](ADRs)

## Projeto

- **Status**: {status}
- **Fase Atual**: {phase}
- **Ultima Atualizacao**: {timestamp}

---
*Sincronizado automaticamente pelo SDLC Agentico*
```

## Workflow de Sincronizacao

```
1. Clone wiki repo para /tmp/wiki-$$
2. Limpa arquivos gerenciados pelo SDLC
3. Copia documentos de .agentic_sdlc/
4. Converte ADRs YAML para Markdown
5. Gera Home.md com indice
6. Gera _Sidebar.md
7. Commit e push
8. Cleanup diretorio temporario
```

## Integracao SDLC

### Ao criar ADR (qualquer fase)
```bash
# Hook PostToolUse para adr-create
.claude/skills/github-wiki/scripts/publish_adr.sh $ADR_PATH
```

### Ao aprovar gate de release (Phase 7)
```bash
# Sincronizacao completa
.claude/skills/github-wiki/scripts/wiki_sync.sh
```

## Inicializacao Manual

Antes de usar a Wiki, ela precisa ser inicializada:

1. Acesse: `https://github.com/{owner}/{repo}/wiki`
2. Clique em "Create the first page"
3. Crie uma pagina Home simples
4. Salve

Apos isso, os scripts podem gerenciar automaticamente.

## Verificar se Wiki esta habilitada

```bash
# Tentar clonar wiki
git clone https://github.com/owner/repo.wiki.git /tmp/test-wiki

# Se falhar com "repository not found":
# - Wiki nao esta habilitada, ou
# - Wiki nao foi inicializada (sem paginas)
```

## Comandos Relacionados

- `/wiki-sync` - Comando para sincronizar manualmente
- `/adr-create` - Cria ADR e opcionalmente publica

## Limitacoes

- Wiki deve ser inicializada manualmente (pelo menos Home)
- Sem API, apenas operacoes Git
- Conflitos podem ocorrer se wiki for editada manualmente
- Historico de versoes via Git, nao via UI
