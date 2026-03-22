---
name: sprint-status
description: Dashboard synthetique de progression du sprint avec support multi-sprint
---

# Sprint Status

## Objectif

Afficher un dashboard synthetique de la progression du sprint en cours.

## Modes d'execution

| Mode | Declencheur | Description |
|------|------------|-------------|
| Normal | `--sprint <chemin>` | Dashboard general du sprint |
| Epics | `--epics` | Detail par epic |
| Issues | `--issues` | Stories bloquees et problemes |

## Fonctionnement

1. Lire `sprint-status.yaml` (source de verite)
2. Calculer les metriques :
   - Progression globale (done / total)
   - Progression par epic
   - Repartition par taille et statut
   - Temps total passe vs estimations
   - Difficultes rencontrees
3. Identifier la prochaine story disponible (todo + dependances resolues)
4. Lister les stories bloquees avec raisons

## Affichage : Mode normal

```
Sprint : {nom-feature}
Progress : [=========>         ] 45% (9/20)

Par statut : 9 done | 2 in_progress | 7 todo | 2 blocked
Par taille : S:5/8 | M:3/7 | L:1/4 | XL:0/1

Temps total : {N}h{M}min
Difficultes : {N} hard, {N} extreme

Prochaine story : {id} - {titre} ({taille})
```

## Affichage : Mode epics

```
Epics:
  [####----] Epic 1 : {nom}  (4/8)  ~{N}h
  [########] Epic 2 : {nom}  (5/5)  DONE ~{N}h
  [--------] Epic 3 : {nom}  (0/7)
```

## Affichage : Mode issues

```
Stories bloquees :
  - {id} : {titre} - Raison : {dependance non resolue / erreur / complexite}

Stories avec difficulte extreme :
  - {id} : {titre} - Lecon : {resume}
```

## Multi-sprint

Si plusieurs sprints existent (`sprint-1/`, `sprint-2/`...), afficher un resume global puis le detail du sprint en cours.

## Sortie attendue

Dashboard texte formate, directement lisible dans le terminal.
