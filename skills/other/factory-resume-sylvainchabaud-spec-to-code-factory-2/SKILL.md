---
name: factory-resume
description: "Reprend le pipeline depuis la dernière phase/task"
context: fork
allowed-tools: Read, Glob, Grep, Bash, Task, Skill
---

# Factory Resume - Reprise du Pipeline

Tu es l'orchestrateur de reprise du pipeline après une interruption.

## Workflow

### 0. Instrumentation (si activée)
```bash
node tools/instrumentation/collector.js skill "{\"skill\":\"factory-resume\"}"
```

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
- Informer l'utilisateur et suggérer `/factory-run`

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
Si une task est en cours (`tasks.current !== null`) :
1. Définir la task courante :
   ```bash
   node tools/set-current-task.js set docs/planning/tasks/[TASK-ID].md
   ```
2. Déléguer au developer :
   ```
   Task(
     subagent_type: "developer",
     prompt: "Continue la task docs/planning/tasks/[TASK-ID].md",
     description: "Developer - Resume TASK"
   )
   ```
3. Puis continuer avec les tasks suivantes via `/factory-build`

Sinon :
```
Skill(skill: "factory-build")
```

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
- Ou démarrer un nouveau pipeline avec `/factory-run`

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
