---
name: code-review
description: Analyser du code modifie et lister les problemes en se basant sur les regles et conventions evan-workflow.
---

# Code Review

## Objectif

Analyser du code modifie (commit, branche, fichiers, diff non-committe) et produire un rapport structure des problemes detectes en se basant sur les regles evan-workflow.

## Input parametrable

- **Commit specifique** : `/code-review --commit abc123`
- **Plage de commits** : `/code-review --commits abc123..def456`
- **Branche entiere** (diff vs main) : `/code-review --branch feature/xxx`
- **Fichiers specifiques** : `/code-review src/components/MyComponent.tsx`
- **Sans parametre** : analyse le diff non-committe (staged + unstaged)

## Workflow

### Etape 1 — Recuperer le diff

Selon le mode choisi, executer la commande git appropriee :
- Sans parametre : `git diff` (unstaged) + `git diff --staged` (staged)
- `--commit abc123` : `git show abc123`
- `--commits abc123..def456` : `git log -p abc123..def456`
- `--branch feature/xxx` : `git diff main...feature/xxx`
- Fichiers specifiques : `git diff -- <fichiers>` ou lire directement les fichiers

### Etape 2 — Lister les fichiers modifies

Produire un resume des fichiers modifies avec :
- Nom du fichier
- Type de modification (ajout, modification, suppression)
- Resume court du changement

### Etape 3 — Charger les regles evan-workflow

Identifier le(s) stack(s) concerne(s) a partir des extensions de fichiers et de la structure du projet, puis charger :
1. Lire `~/evan-workflow/common/manifest.yaml` et charger les fichiers des scopes `always` + scopes pertinents au projet (frontend, backend)
2. `~/evan-workflow/technos/{stack}/code-style.md`
3. `~/evan-workflow/technos/{stack}/patterns/*.md` (seulement les patterns pertinents)

### Etape 4 — Analyser chaque modification

Pour chaque fichier modifie, verifier :
- Respect des conventions de nommage
- Respect du code style du stack
- Respect des patterns evan-workflow (structure, organisation, types)
- Absence de bugs evidents, failles de securite, regressions
- Coherence des types et des imports
- Qualite generale du code

Classer chaque probleme selon les niveaux de severite definis dans `references/severity-levels.md`.

### Etape 5 — Produire le rapport

Generer le rapport au format defini dans `references/report-template.md`. Le rapport inclut :
- Resume global
- Problemes classes par severite (CRITIQUE, HAUTE, MOYENNE, BASSE)
- Points positifs
- Actions recommandees

### Etape 6 — Proposer la correction

A la fin du rapport, proposer au user d'utiliser `/fix-review-code` pour corriger automatiquement les problemes detectes.

## Principes

- **Exhaustivite** : ne pas ignorer de fichier modifie.
- **Precision** : chaque probleme doit citer le fichier, la ligne et la regle violee.
- **Equilibre** : mentionner aussi ce qui est bien fait (points positifs).
- **Actionnable** : chaque probleme doit avoir une suggestion de correction.
- **Non-bloquant** : les problemes de severite BASSE sont des suggestions, pas des blockers.
