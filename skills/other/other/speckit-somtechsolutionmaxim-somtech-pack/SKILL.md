---
name: speckit
description: |
  Workflow Speckit : specify, plan, tasks, implement.
  TRIGGERS : speckit, spec, spécification, plan technique, créer spec, feature
disable-model-invocation: true
argument-hint: <init|plan|tasks|implement> [feature-name]
---

# Workflow Speckit

L'utilisateur a exécuté : `/speckit $ARGUMENTS`

## Commandes

| Argument | Action |
|----------|--------|
| `init <nom>` | Créer une nouvelle spécification |
| `plan <feature>` | Générer le plan technique |
| `tasks <feature>` | Générer les tâches ordonnées |
| `implement <feature>` | Implémenter selon les tâches |
| (vide) | Afficher l'aide |

---

## `/speckit init <nom>`

Créer `specs/{numero}-{nom}/spec.md` :

```markdown
# Spécification : {nom}

## Contexte
[Description du besoin métier]

## User Stories

### US-1 : [Titre]
**En tant que** [persona]
**Je veux** [action]
**Afin de** [bénéfice]

#### Critères d'acceptation
- [ ] **Given** [contexte] **When** [action] **Then** [résultat]
- [ ] **Given** [contexte] **When** [action] **Then** [résultat]

## Contraintes
- [Contraintes techniques/métier]

## Dépendances
- [Modules/features liés]

## Out of scope
- [Ce qui n'est PAS inclus]
```

---

## `/speckit plan <feature>`

Créer `specs/{feature}/plan.md` :

```markdown
# Plan Technique : {feature}

## Architecture

### Composants impactés
- [ ] Frontend : [composants]
- [ ] Backend : [endpoints/functions]
- [ ] Database : [tables/migrations]

### Flux de données
[Diagramme ou description]

## API (si applicable)

Créer `specs/{feature}/contracts/api-spec.json`

## Modèle de données (si applicable)

Créer `specs/{feature}/data-model.md`

## Risques et mitigations
- Risque 1 : [description] → Mitigation : [action]
```

---

## `/speckit tasks <feature>`

Créer `specs/{feature}/tasks.md` :

```markdown
# Tâches : {feature}

## Ordre d'exécution

### Phase 1 : Setup
- [ ] **T1** [S] : [description]
- [ ] **T2** [M] : [description]

### Phase 2 : Implementation
- [ ] **T3** [L] : [description]
- [ ] **T4** [M] : [description]

### Phase 3 : Tests & Validation
- [ ] **T5** [S] : Tests unitaires
- [ ] **T6** [M] : Tests e2e
- [ ] **T7** [S] : Validation UI (0 erreur console)

## Légende
- [S] = Small (< 1h)
- [M] = Medium (1-4h)
- [L] = Large (> 4h)
```

---

## `/speckit implement <feature>`

1. Lire `specs/{feature}/spec.md`
2. Lire `specs/{feature}/plan.md`
3. Lire `specs/{feature}/tasks.md`
4. Exécuter les tâches **dans l'ordre**
5. Cocher chaque tâche terminée
6. Valider avec `/validate-ui` à la fin

---

## Aide (si aucun argument)

```
📋 SPECKIT - Workflow de Spécification
======================================

Usage:
  /speckit <command> [feature-name]

Commandes:
  init <nom>        Créer une nouvelle spécification
  plan <feature>    Générer le plan technique
  tasks <feature>   Générer les tâches ordonnées
  implement <feat>  Implémenter selon les tâches

Workflow typique:
  1. /speckit init ma-feature
  2. /speckit plan ma-feature
  3. /speckit tasks ma-feature
  4. /speckit implement ma-feature

Structure générée:
  specs/{numero}-{nom}/
    spec.md           ← Spécification fonctionnelle
    plan.md           ← Plan technique
    tasks.md          ← Tâches ordonnées
    contracts/        ← Contrats API (si applicable)
    data-model.md     ← Modèle de données (si applicable)
```
