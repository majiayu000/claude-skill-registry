---
name: sprint-planner
description: Transforme un plan de feature en arborescence sprint avec epics, stories et tracking via sprint-status.yaml
---

# Sprint Planner

## Objectif

Transformer un plan de feature finalise en arborescence de sprint exploitable par `dev-story`, avec fichiers de stories detailles et un fichier `sprint-status.yaml` comme source de verite.

## Modes d'execution

| Mode | Declencheur | Description |
|------|------------|-------------|
| Normal | `--plan <chemin>` | Generer le sprint depuis un plan finalise |
| Fix | `--fix` | Recalculer les compteurs et corriger sprint-status.yaml |
| Progress | `--progress` | Dashboard de progression du sprint |

## Structure generee

```
{docs-dir}/features/{nom}/sprint/
  sprint-status.yaml       # Source de verite du sprint
  epics/
    epic-01-{slug}/
      _epic.md              # Description de l'epic
      story-01-{slug}.md    # Story detaillee
      story-02-{slug}.md
    epic-02-{slug}/
      _epic.md
      story-01-{slug}.md
```

## Workflow : Mode normal

### Etape 1 : Lecture du plan

1. Lire le plan finalise (mode D du feature-planner)
2. Valider que le plan a ete revue (review-critique.md existe)
3. Extraire les epics, stories, dependances et estimations

### Etape 2 : Generation de l'arborescence

1. Creer le dossier `sprint/` et les sous-dossiers epics
2. Pour chaque epic, generer `_epic.md` avec :
   - Nom et description
   - Nombre de stories
   - Objectif de l'epic

3. Pour chaque story, generer un fichier avec les sections suivantes :

```markdown
---
id: {epic-num}.{story-num}
title: "{titre imperatif}"
status: todo
size: S | M | L | XL
depends_on: [] | ["{id}"]
epic: "{nom-epic}"
---

# {titre}

## Contexte
{Pourquoi cette story existe}

## Objectif
{Ce que la story doit accomplir}

## Criteres d'acceptation
- [ ] {critere 1}
- [ ] {critere 2}

## Fichiers cibles
- `{chemin/fichier}` - {creer | modifier} - {description}

## Patterns et references
- `~/evan-workflow/technos/{stack}/patterns/{pattern}.md`

## Notes d'implementation
{Indications techniques, pieges a eviter}

## Tests attendus
- [ ] {test 1}
- [ ] {test 2}
```

### Etape 3 : Generation du sprint-status.yaml

```yaml
feature: "{nom-feature}"
plan_version: "v{N}"
created_at: "{date}"
updated_at: "{date}"

summary:
  total_stories: {N}
  completed: 0
  in_progress: 0
  todo: {N}
  blocked: 0

epics:
  - name: "{nom-epic}"
    slug: "epic-01-{slug}"
    stories:
      - id: "1.1"
        title: "{titre}"
        status: "todo"        # todo | in_progress | done | blocked
        size: "M"
        depends_on: []
        started_at: null
        completed_at: null
        duration_minutes: null
        difficulty: null       # easy | medium | hard | extreme
        lessons_learned: null
      - id: "1.2"
        ...
```

### Etape 4 : Validation

1. **Coherence** : Chaque story du plan est presente dans l'arborescence
2. **Dependances** : Pas de dependances circulaires
3. **Compteurs** : sprint-status.yaml reflette le bon total
4. **Conventions** : Les patterns references existent dans `~/evan-workflow/technos/`
5. **Fichiers cibles** : Les chemins sont realistes par rapport a l'arborescence du projet

## Workflow : Mode fix

1. Scanner tous les fichiers story dans `sprint/epics/`
2. Lire le statut de chaque story
3. Recalculer les compteurs dans `sprint-status.yaml`
4. Corriger les incoherences (statuts, dependances)
5. Afficher un rapport des corrections

## Workflow : Mode progress

1. Lire `sprint-status.yaml`
2. Afficher un dashboard :

```
Sprint : {nom-feature}
Progress : [=========>         ] 45% (9/20)

Epics:
  [####----] Epic 1 : {nom}  (4/8)
  [########] Epic 2 : {nom}  (5/5) DONE
  [--------] Epic 3 : {nom}  (0/7)

Par taille:
  S: 5/8 done | M: 3/7 done | L: 1/4 done | XL: 0/1 done

Prochaine story disponible : Story {X.Y} - {titre} ({taille})
Bloquees : {N} stories ({raisons})
```

## Regles de qualite

- Chaque story doit etre auto-suffisante : un developpeur doit pouvoir l'implementer sans contexte supplementaire
- Les fichiers cibles doivent etre precis (pas de "modifier le backend")
- Les criteres d'acceptation doivent etre testables
- Les dependances doivent etre minimales et explicites
- Les tailles XL doivent etre signalees avec un warning

## Multi-sprint

Si le plan contient plus de stories qu'un sprint ne peut absorber :
- Decouper en sprints successifs : `sprint-1/`, `sprint-2/`
- Chaque sprint a son propre `sprint-status.yaml`
- Les dependances inter-sprints sont documentees

## Sortie attendue

A la fin de l'execution, afficher :
- Nombre d'epics et stories generees
- Repartition par taille
- Dependances detectees
- Prochaine action : "Lancer `/dev-story --next` pour commencer l'implementation"
