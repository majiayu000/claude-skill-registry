---
name: update-docs
version: 1.0.0
description: Atualiza contadores de componentes em README.md e CLAUDE.md
tags: [documentation, maintenance, automation]
---

# Update Documentation Counts

Executa o script de atualização de contadores de componentes.

## Instructions

Quando o usuário executar `/update-docs`:

1. Execute o script de atualização:
   ```bash
   ./.claude/scripts/update-component-counts.sh
   ```

2. Aguarde a conclusão do script

3. Analise o output:
   - Se houver atualizações, mostre um resumo das mudanças
   - Se não houver mudanças, informe que está tudo correto

4. Se houver mudanças:
   - Mostre o diff: `git diff README.md CLAUDE.md`
   - Pergunte se o usuário quer commitar automaticamente
   - Se sim, execute:
     ```bash
     git add README.md CLAUDE.md
     git commit -m "docs: update component counts (auto-generated)

     - Agents: X
     - Skills: Y
     - Commands: Z
     - Hooks: W

     Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
     ```

## Example Interaction

**User**: `/update-docs`

**Assistant**:
```
Executando atualização de contadores...

📊 Contadores detectados:
   Agents:   39 (+1)
   Skills:   29
   Commands: 25 (+1)
   Hooks:    21 (+1)

✅ Documentos atualizados:
   - README.md
   - CLAUDE.md

Mudanças detectadas:

diff --git a/README.md b/README.md
@@ -37 +37 @@
-O SDLC Agêntico é um framework que usa **38 agentes especializados**
+O SDLC Agêntico é um framework que usa **39 agentes especializados**

Deseja commitar essas mudanças automaticamente? (sim/não)
```

**User**: sim

**Assistant**:
```bash
git add README.md CLAUDE.md
git commit -m "docs: update component counts (auto-generated)

- Agents: 39
- Skills: 29
- Commands: 25
- Hooks: 21

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

✅ Commit criado com sucesso!

## Implementation

O skill usa o script `.claude/scripts/update-component-counts.sh` que:
- Conta componentes automaticamente
- Atualiza padrões conhecidos em README.md e CLAUDE.md
- Preserva formatação e estrutura dos documentos

## Related

- `/doc-generate` - Gera documentação completa do zero
- Hook `auto-update-component-counts.sh` - Atualização automática via PostToolUse
