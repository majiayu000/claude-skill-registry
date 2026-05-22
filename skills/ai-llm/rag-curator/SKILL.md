---
name: rag-curator
description: Curador do corpus RAG. Gerencia adição, organização e manutenção do conhecimento do projeto. Garante qualidade e acessibilidade.
---

# RAG Curator

Skill responsável por curar e manter o corpus RAG do projeto.

## Capabilities

- **Index ADRs**: Copia ADRs de `.agentic_sdlc/projects/{id}/decisions/` para `corpus/nodes/decisions/`
- **Index Learnings**: Copia learnings extraídos para `corpus/nodes/learnings/`
- **Validate Quality**: Verifica qualidade e completude dos nodes
- **Clean Obsolete**: Remove conhecimento obsoleto

## Usage

```bash
# Index ADRs from project to corpus
python3 .claude/skills/rag-curator/scripts/index_adrs.py --project-id PROJECT_ID

# Index all projects
python3 .claude/skills/rag-curator/scripts/index_adrs.py --all

# Validate corpus quality
python3 .claude/skills/rag-curator/scripts/validate_corpus.py
```

## Integration

- **Phase 1 (Discovery)**: domain-researcher → rag-curator (index research)
- **Phase 3 (Architecture)**: adr-author → rag-curator (index ADRs)
- **Gate Evaluation**: gate-evaluator → rag-curator (auto-index on gate pass)

## Files

- `scripts/index_adrs.py`: Index ADRs to corpus
- `scripts/index_learnings.py`: Index learnings to corpus
- `scripts/validate_corpus.py`: Validate corpus quality
