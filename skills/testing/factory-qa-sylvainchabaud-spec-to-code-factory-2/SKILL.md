---
name: factory-qa
description: "Phase DEBRIEF - Tests + QA + Release"
context: fork
allowed-tools: Read, Glob, Grep, Task, Bash
---

# Factory QA - Phase DEBRIEF

Tu es l'orchestrateur de la phase DEBRIEF.

## Workflow

0. **Instrumentation** (si activée) - Enregistrer le début de phase :
   ```bash
   node tools/instrumentation/collector.js phase-start "{\"phase\":\"DEBRIEF\",\"skill\":\"factory-qa\"}"
   node tools/instrumentation/collector.js skill "{\"skill\":\"factory-qa\"}"
   ```

1. **Vérifier Gate 4** : `node tools/gate-check.js 4`

2. **Déléguer à l'agent `qa`** via Task tool :
   ```bash
   # Instrumentation (si activée)
   node tools/instrumentation/collector.js agent "{\"agent\":\"qa\",\"source\":\"factory-qa\"}"
   ```
   ```
   Task(
     subagent_type: "qa",
     prompt: "Exécute les tests, génère docs/qa/report.md, docs/release/checklist.md et CHANGELOG.md",
     description: "QA - Phase DEBRIEF"
   )
   ```

3. **Vérifier les outputs QA** :
   - `docs/qa/report.md` existe
   - `docs/release/checklist.md` existe
   - `CHANGELOG.md` existe et est à jour

4. **Exporter le projet livrable** :
   ```bash
   node tools/export-release.js
   ```
   Cette commande:
   - Copie les fichiers du projet (hors infrastructure factory) vers `release/`
   - Genere un README.md enrichi depuis les specs
   - Cree un manifest de traçabilite (`docs/factory/release-manifest.json`)

5. **Exécuter Gate 5** : `node tools/gate-check.js 5`

6. **Logger** via :
   ```bash
   node tools/factory-log.js "DEBRIEF" "completed" "Phase QA terminée"
   ```

7. **Retourner** le rapport final de release avec :
   - Résultat des tests
   - Couverture
   - Issues détectées
   - Checklist release validée

## Anti-dérive

Si des bugs critiques sont détectés → les documenter dans le rapport, NE PAS les corriger (sauf bloquants).

## En cas d'échec

Si Gate 5 échoue → STOP et rapport des éléments manquants.
