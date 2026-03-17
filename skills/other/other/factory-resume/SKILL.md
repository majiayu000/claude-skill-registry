---
name: factory-resume
description: "Reprend le pipeline depuis la dernière phase/task"
context: fork
allowed-tools: Read, Glob, Grep, Bash, Task, Skill
---

# Factory Resume - Reprise du Pipeline

Tu es l'orchestrateur de reprise du pipeline après une interruption.

## Workflow

### 1. Charger l'état actuel

```bash
node tools/factory-state.js get
```

Analyser le JSON retourné pour déterminer :
- `pipeline.status` : État global (idle, running, paused, completed, failed)
- `pipeline.currentPhase` : Phase en cours
- `tasks.current` : Task en cours (si phase build)
- `gates` : État des gates

### 2. Déterminer le point de reprise

**Si `pipeline.status === 'idle'`** :
- Pas de pipeline en cours
- Informer l'utilisateur et suggérer `/factory`

**Si `pipeline.status === 'completed'`** :
- Pipeline déjà terminé
- Informer l'utilisateur et suggérer `/factory-qa` ou `/reset`

**Si `pipeline.status === 'failed'`** :
- Identifier la phase/gate qui a échoué
- Proposer les options de correction

**Si `pipeline.status === 'running'`** :
- Reprendre depuis `currentPhase`
- Si phase `build` avec `tasks.current` → reprendre cette task

### 3. Reprendre l'exécution

Selon la phase à reprendre :

**Phase BREAK** :
```
Skill(skill: "factory-intake")
```

**Phase MODEL** :
```
Skill(skill: "factory-spec")
```

**Phase PLAN** :
```
Skill(skill: "factory-plan")
```

**Phase BUILD** :
1. Lister toutes les tasks avec leur statut reel :
   ```bash
   node tools/factory-state.js tasks list
   # Retourne: { planningDir, current, total, completed, pending, tasks: { TASK-0001: { status, ... }, ... } }
   ```
2. Identifier les tasks pendantes (status != 'completed') :
   - Trier par numero (TASK-0001, TASK-0002, ...)
   - Si `current` est defini → reprendre cette task en premier
   - Sinon → prendre la premiere task pendante
3. Pour chaque task pendante, dans l'ordre :
   a. Definir la task courante :
      ```bash
      node tools/set-current-task.js set <tasksDir>/[TASK-ID].md
      ```
   b. Deleguer au developer :
      ```
      Task(
        subagent_type: "developer",
        prompt: "Implemente la task <tasksDir>/[TASK-ID].md",
        description: "Developer - Resume TASK"
      )
      ```
   c. Mettre a jour le statut :
      ```bash
      node tools/factory-state.js task [TASK-ID] completed
      node tools/set-current-task.js clear
      ```
4. Si toutes les tasks sont completes → continuer vers DEBRIEF

**Phase DEBRIEF** :
```
Skill(skill: "factory-qa")
```

### 4. Mettre à jour l'état

Après reprise réussie :
```bash
node tools/factory-state.js set pipeline.status "running"
```

### 5. Rapport de reprise

Retourner un résumé :
- Point de reprise (phase, task si applicable)
- Actions effectuées
- État actuel
- Prochaines étapes

## Cas d'erreur

**Si state.json n'existe pas** :
- Proposer d'initialiser avec `node tools/factory-state.js init`
- Ou démarrer un nouveau pipeline avec `/factory`

**Si incohérence détectée** :
- Vérifier les gates avec `node tools/gate-check.js [N]`
- Proposer de réinitialiser la phase problématique avec `/reset [phase]`

## Exemples d'utilisation

```
/factory-resume
```
→ Analyse l'état et reprend automatiquement

```
/factory-resume --force build
```
→ Force la reprise depuis la phase build (via argument)
