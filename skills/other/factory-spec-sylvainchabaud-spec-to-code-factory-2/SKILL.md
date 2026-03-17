---
name: factory-spec
description: "Phase MODEL - Génère specs + ADR + rules"
context: fork
allowed-tools: Read, Glob, Grep, Task, Bash
---

# Factory Spec - Phase MODEL

Tu es l'orchestrateur de la phase MODEL.

## Workflow

> ⚠️ **SYNCHRONISATION OBLIGATOIRE** : Chaque étape DOIT être terminée avant de passer à la suivante.
> Les agents ont des dépendances : architect dépend de pm, rules-memory dépend de architect.

0. **Instrumentation** (si activée) - Enregistrer le début de phase :
   ```bash
   node tools/instrumentation/collector.js phase-start "{\"phase\":\"MODEL\",\"skill\":\"factory-spec\"}"
   node tools/instrumentation/collector.js skill "{\"skill\":\"factory-spec\"}"
   ```

1. **Vérifier Gate 1** : `node tools/gate-check.js 1`
   - Si exit code ≠ 0 → STOP immédiat

2. **Déléguer à l'agent `pm`** via Task tool :
   ```bash
   # Instrumentation (si activée)
   node tools/instrumentation/collector.js agent "{\"agent\":\"pm\",\"source\":\"factory-spec\"}"
   ```
   ```
   Task(
     subagent_type: "pm",
     prompt: "Produis docs/specs/system.md et docs/specs/domain.md depuis docs/brief.md et docs/scope.md",
     description: "PM - Specs fonctionnelles"
   )
   ```
   **⏳ ATTENDRE que le Task soit terminé avant de continuer.**
   **✅ Vérifier** : `docs/specs/system.md` ET `docs/specs/domain.md` existent.

3. **Déléguer à l'agent `architect`** via Task tool :
   ```bash
   # Instrumentation (si activée)
   node tools/instrumentation/collector.js agent "{\"agent\":\"architect\",\"source\":\"factory-spec\"}"
   ```
   ```
   Task(
     subagent_type: "architect",
     prompt: "Produis docs/specs/api.md et docs/adr/ADR-0001-stack.md depuis docs/specs/system.md et docs/specs/domain.md",
     description: "Architect - Specs techniques"
   )
   ```
   **⏳ ATTENDRE que le Task soit terminé avant de continuer.**
   **✅ Vérifier** : `docs/specs/api.md` ET `docs/adr/ADR-0001-*.md` existent.

4. **Déléguer à l'agent `rules-memory`** via Task tool :
   ```bash
   # Instrumentation (si activée)
   node tools/instrumentation/collector.js agent "{\"agent\":\"rules-memory\",\"source\":\"factory-spec\"}"
   ```
   ```
   Task(
     subagent_type: "rules-memory",
     prompt: "Génère les rules dans .claude/rules/ et enrichis CLAUDE.md depuis docs/specs/* et docs/adr/*",
     description: "Rules-Memory - Rules et mémoire"
   )
   ```
   **⏳ ATTENDRE que le Task soit terminé avant de continuer.**

5. **Vérifier les outputs** :
   - `docs/specs/system.md` existe
   - `docs/specs/domain.md` existe
   - `docs/specs/api.md` existe
   - `docs/adr/ADR-0001-*.md` existe

6. **Exécuter Gate 2** : `node tools/gate-check.js 2`
   - Si exit code ≠ 0 → STOP immédiat avec rapport des erreurs

7. **Logger** via :
   ```bash
   node tools/factory-log.js "MODEL" "completed" "Phase MODEL terminée"
   ```

8. **Retourner** un résumé avec liste des specs générées

## En cas d'échec

Si Gate 2 échoue → STOP et rapport des fichiers manquants.
