---
name: factory-plan
description: "Phase ACT (planning) - Génère epics/US/tasks"
context: fork
allowed-tools: Read, Glob, Grep, Task, Bash
---

# Factory Plan - Phase ACT (Planning)

Tu es l'orchestrateur de la phase planning.

## Workflow

0. **Instrumentation** (si activée) - Enregistrer le début de phase :
   ```bash
   node tools/instrumentation/collector.js phase-start "{\"phase\":\"ACT\",\"skill\":\"factory-plan\"}"
   node tools/instrumentation/collector.js skill "{\"skill\":\"factory-plan\"}"
   ```

1. **Vérifier Gate 2** : `node tools/gate-check.js 2`

2. **Déléguer à l'agent `scrum-master`** via Task tool :
   ```bash
   # Instrumentation (si activée)
   node tools/instrumentation/collector.js agent "{\"agent\":\"scrum-master\",\"source\":\"factory-plan\"}"
   ```
   ```
   Task(
     subagent_type: "scrum-master",
     prompt: "Décompose docs/specs/* et docs/adr/* en epics/US/tasks.

     IMPORTANT - Tasks auto-suffisantes (principe BMAD):
     Chaque TASK doit être 100% indépendante avec:
     - Template: templates/planning/task-template.md
     - Contexte complet: références specs avec résumés
     - Code existant pertinent: extraits avec lignes
     - Aucune dépendance à la task précédente

     Le développeur doit pouvoir implémenter la task
     SANS connaître les autres tasks.",
     description: "Scrum Master - Planning BMAD"
   )
   ```

3. **Vérifier les outputs** :
   - `docs/planning/epics.md` existe
   - Au moins 1 fichier `docs/planning/us/US-*.md`
   - Au moins 1 fichier `docs/planning/tasks/TASK-*.md`
   - Chaque TASK contient TOUTES ces sections (auto-suffisance BMAD):
     * Objectif technique
     * Contexte complet (specs référencées avec résumés)
     * Fichiers concernés (liste exhaustive)
     * Definition of Done
     * Tests attendus
     * Critères de validation automatique

4. **Exécuter Gate 3** : `node tools/gate-check.js 3`

5. **Logger** via :
   ```bash
   node tools/factory-log.js "ACT" "completed" "Phase planning terminee"
   ```

6. **Retourner** un résumé avec liste des tasks créées (numérotées)

## En cas d'échec

Si Gate 3 échoue → STOP et rapport des éléments manquants.
