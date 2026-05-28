---
name: factory-build
description: "Phase ACT (build) - Implémente task-by-task"
context: fork
allowed-tools: Read, Glob, Grep, Task, Bash
---

# Factory Build - Phase ACT (Build)

Tu es l'orchestrateur de la phase build.

## Workflow

1. **Vérifier Gate 3** : `node tools/gate-check.js 3`

2. **Lister les tasks** : Glob `docs/planning/tasks/TASK-*.md`
   - **OBLIGATOIRE** : Trier par numéro (TASK-0001 avant TASK-0002, etc.)
   - Utiliser tri numérique : extraire le numéro XXXX et trier par valeur entière
   - Exemple ordre correct : TASK-0001, TASK-0002, TASK-0010, TASK-0100
   - Exemple ordre INCORRECT : TASK-0001, TASK-0010, TASK-0002 (tri alphabétique)

3. **Pour chaque TASK** (dans l'ordre numérique strict) :

   a. **Définir la task courante** (pour anti-dérive automatique) :
      ```bash
      node tools/set-current-task.js set docs/planning/tasks/TASK-XXXX.md
      ```

   b. **Déléguer à l'agent `developer`** via Task tool :
      ```
      Task(
        subagent_type: "developer",
        prompt: "Implémente la task docs/planning/tasks/TASK-XXXX.md",
        description: "Developer - TASK-XXXX"
      )
      ```

   c. **Vérifier la DoD** de la task (lire le fichier task et vérifier chaque critère)

   d. **Effacer la task courante** :
      ```bash
      node tools/set-current-task.js clear
      ```

   e. **Logger** via :
      ```bash
      node tools/factory-log.js "ACT-BUILD" "task-done" "TASK-XXXX implémentée"
      ```

4. **Exécuter Gate 4** : `node tools/gate-check.js 4`

5. **Retourner** un résumé des tasks implémentées avec statuts

## Règle anti-dérive

Si l'agent `developer` tente de modifier des fichiers hors scope → STOP immédiat et rapport.

## En cas d'échec

Si Gate 4 échoue → STOP et rapport des tests/fichiers manquants.
