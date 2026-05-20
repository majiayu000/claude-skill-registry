---
name: dev-story
description: Implementation de stories avec workflow en 10 etapes, modes batch/parallel/epic, tracking et retour d'experience
---

# Dev Story

## Objectif

Implementer une story selon un workflow rigoureux en 10 etapes, avec tracking du temps, retour d'experience et mise a jour du sprint-status.yaml.

## Modes d'execution

| Mode | Declencheur | Description |
|------|------------|-------------|
| Story specifique | `--story <id>` | Implementer une story par son ID |
| Prochaine auto | `--next` | Prendre la prochaine story disponible (todo, dependances resolues) |
| Batch | `--batch <id1,id2,...>` | Implementer plusieurs stories sequentiellement |
| Parallel | `--parallel <id1,id2,...>` | Lancer des agents workers en parallele |
| Epic filtre | `--epic <slug>` | Toutes les stories d'un epic, sequentiellement |
| All epic | `--all-epic <slug>` | Toutes les stories d'un epic, en parallele si possible |

## Pre-requis

- Un sprint genere par `sprint-planner` avec `sprint-status.yaml`
- La story cible doit avoir le statut `todo`
- Les dependances de la story doivent avoir le statut `done`

## Workflow en 10 etapes

### Etape 1 : Pre-flight

1. Lire `sprint-status.yaml`
2. Verifier que la story existe et est `todo`
3. Verifier que les dependances sont `done`
4. Mettre le statut a `in_progress` et enregistrer `started_at`
5. Lire le fichier story pour les specs detaillees

### Etape 2 : Scan contextuel et adaptive context loading

1. Lire les fichiers cibles listes dans la story
2. Scanner le code environnant pour comprendre le contexte
3. **Adaptive context loading** : Identifier le stack concerne par la story, puis charger UNIQUEMENT les docs evan-workflow pertinentes :
   - Lire `~/evan-workflow/common/manifest.yaml` et charger les fichiers des scopes `always` + scopes pertinents au projet (frontend, backend)
   - `~/evan-workflow/technos/{stack}/patterns/{pattern}.md` references dans la story
   - Ne PAS charger tout le dossier technos, seulement ce qui est necessaire
4. Identifier les impacts potentiels sur d'autres fichiers

### Etape 3 : Checkpoint git

1. **Creer un checkpoint git** avant toute modification :
   ```
   git stash   # si des changements en cours
   ```
2. S'assurer que le working tree est propre
3. Cela permet un rollback facile si l'implementation echoue

### Etape 4 : Implementation

1. Implementer selon les specs de la story
2. Respecter les patterns charges a l'etape 2
3. Suivre les conventions evan-workflow chargees via le manifeste (scope `always` + scopes du projet)
4. Suivre les regles de style de `~/evan-workflow/technos/{stack}/code-style.md`
5. Creer/modifier uniquement les fichiers listes dans la story (sauf si un impact cascade l'exige)

### Etape 5 : Verification impact cascade

1. Verifier que les modifications ne cassent pas d'autres parties du code
2. Chercher les references aux fichiers modifies
3. Verifier les imports, les types, les interfaces
4. Si un impact est detecte, corriger ou documenter

### Etape 6 : Tests

1. Ecrire les tests listes dans la story
2. Executer les tests unitaires concernes
3. Verifier que les tests existants passent encore
4. Si des tests echouent, corriger l'implementation

### Etape 7 : Documentation update

1. Si la story impacte une documentation existante, la mettre a jour
2. Appeler `feature-doc --update` si necessaire (mode depuis dev-story)
3. Mettre a jour les commentaires de code si pertinent

### Etape 8 : Retour d'experience

1. Enregistrer dans sprint-status.yaml pour cette story :
   - `difficulty` : easy | medium | hard | extreme
   - `lessons_learned` : Ce qui a ete appris, les pieges rencontres
   - `duration_minutes` : Temps reel d'implementation
2. Si la taille estimee etait incorrecte, le noter

### Etape 9 : Commit

1. Creer un commit atomique avec un message clair :
   ```
   feat({scope}): {description courte}

   Story {id}: {titre de la story}

   - {changement 1}
   - {changement 2}
   ```
2. Suivre les conventions du scope `commit` du manifeste evan-workflow (`~/evan-workflow/common/git-conventions.md`)
3. Un commit par story (sauf si la story est decoupee en sous-taches logiques)

### Etape 10 : Status update et proposition next

1. Mettre le statut a `done` dans `sprint-status.yaml`
2. Enregistrer `completed_at`
3. Recalculer les compteurs `summary`
4. Identifier la prochaine story disponible
5. Afficher un resume :

```
Story {id} terminee : {titre}
Duree : {N} minutes | Difficulte : {level}
Lecons : {resume}

Sprint progress : [========>          ] 40% (8/20)
Prochaine story : {id} - {titre} ({taille})
```

## Mode parallel

### Fonctionnement

1. Identifier les stories sans dependances mutuelles
2. Pour chaque story, creer une instruction worker avec :
   - Le contexte complet de la story
   - Les fichiers a modifier (SANS conflit avec les autres workers)
   - Les patterns evan-workflow a respecter
3. Chaque worker suit le workflow complet (etapes 1-10)
4. **Fresh context** : Chaque agent worker demarre avec un contexte propre, sans pollution des stories precedentes
5. Consolider les resultats dans sprint-status.yaml

### Regles du mode parallel

- Deux stories ne peuvent PAS modifier le meme fichier en parallele
- Si un conflit de fichier est detecte, la story est mise en attente
- Le sprint-status.yaml est mis a jour de maniere atomique apres chaque worker

## Mode batch

Execution sequentielle des stories listees :
1. Pour chaque story dans l'ordre donne
2. Executer le workflow complet
3. Si une story echoue, proposer : continuer | arreter | skip

## Mode epic

1. Lister toutes les stories de l'epic
2. Trier par dependances
3. Executer sequentiellement (--epic) ou en parallele quand possible (--all-epic)

## Gestion des erreurs

| Situation | Action |
|-----------|--------|
| Dependance non resolue | Bloquer la story, suggerer l'ordre correct |
| Test echoue | Tenter de corriger, sinon marquer `blocked` |
| Conflit de fichier (parallel) | Mettre en attente, traiter sequentiellement |
| Story trop complexe | Suggerer un redecoupe, marquer `blocked` |
| Implementation echouee | Rollback via checkpoint git, marquer `blocked` |

## Sortie attendue

Pour chaque story terminee :
- Resume de l'implementation
- Fichiers crees/modifies
- Tests passes
- Retour d'experience
- Proposition de prochaine story
