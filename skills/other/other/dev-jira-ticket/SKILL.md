---
name: dev-jira-ticket
description: Prendre un ticket Jira et l'implementer de bout en bout, de l'analyse a l'implementation en passant par la planification.
---

# Dev Jira Ticket

## Objectif

Prendre un ticket Jira brut et l'implementer de bout en bout : comprehension, planification, implementation, verification et commit. Contrairement a `/dev-story` qui travaille avec des stories pre-planifiees dans un sprint, ce skill part d'un ticket brut et gere tout le processus.

## Input

- **Fichier de ticket** : `/dev-jira-ticket path/to/ticket.md` (texte, markdown ou PDF exporte)
- **Description inline** : `/dev-jira-ticket "PROJ-123 : Ajouter le champ email au formulaire d'inscription"`
- **URL Jira** : `/dev-jira-ticket https://jira.example.com/browse/PROJ-123` (si accessible)

## Parametres

- `--analyze` : Mode B — analyser le ticket sans implementer
- `--auto-commit` : Mode C — implementer et committer automatiquement

Sans parametre, le mode par defaut est le Mode A (implementation complete avec validation user).

## Workflow

### Etape 1 — Analyse du ticket

Suivre le guide d'analyse dans `references/ticket-analysis.md`.

Lire et comprendre :
- **Titre** du ticket
- **Description** detaillee
- **Acceptance criteria** (criteres d'acceptation)
- **Liens** vers d'autres tickets ou documents
- **Type** : bug, feature, improvement, technical debt

Identifier le scope :
- Quels fichiers et domaines sont impactes
- Quels composants/modules sont concernes
- Y a-t-il des dependances avec d'autres tickets

Estimer la complexite :
- Si le ticket est trop gros (>8-10 fichiers, multiple domaines, architecture complexe) → suggerer `/feature-planner`
- Si le ticket est de taille raisonnable → continuer

### Etape 2 — Scan contextuel

- Identifier le(s) stack(s) concerne(s)
- Charger les docs evan-workflow pertinentes :
  1. Lire `~/evan-workflow/common/manifest.yaml` et charger les fichiers des scopes `always` + scopes pertinents au projet (frontend, backend)
  2. `~/evan-workflow/technos/{stack}/code-style.md`
  3. `~/evan-workflow/technos/{stack}/patterns/` (patterns pertinents)
- Lire le `CLAUDE.md` du projet si present
- Scanner les fichiers directement lies au ticket

### Etape 3 — Clarification

Si des zones d'ombre subsistent apres l'analyse :
- Poser **3 a 5 questions ciblees** maximum au user
- Ne poser que des questions dont la reponse impacte l'implementation
- Si le ticket est clair et complet → passer directement a l'etape 4

### Etape 4 — Mini-plan

Produire un plan d'implementation court et actionnable :
- Liste ordonnee des fichiers a modifier ou creer
- Pour chaque fichier : description courte du changement
- Dependances entre les modifications (ordre d'execution)

Ce n'est pas un plan complet comme `/feature-planner`. C'est un plan d'execution technique direct.

Presenter le plan au user pour validation (sauf en Mode C `--auto-commit`).

### Etape 5 — Implementation

Coder les changements en respectant :
- Les conventions evan-workflow chargees via le manifeste (scope `always` + scopes du projet)
- Les patterns definis dans `~/evan-workflow/technos/{stack}/patterns/`
- Le code style de `~/evan-workflow/technos/{stack}/code-style.md`

En Mode B (`--analyze`) : s'arreter ici et produire uniquement le rapport d'analyse + le mini-plan.

### Etape 6 — Verification

Apres implementation :
- Verifier la coherence des types
- Verifier les imports
- Verifier que les tests existants ne sont pas casses
- Evaluer l'impact cascade sur les autres fichiers du projet
- S'assurer que les acceptance criteria du ticket sont couverts

### Etape 7 — Commit

Creer un ou plusieurs commits avec reference au ticket Jira. Le format du message suit le scope `commit` du manifeste evan-workflow (`~/evan-workflow/common/git-conventions.md`).

Exemple : `Feature - #PROJ-123 - Add email field to registration form`

- Mode A : proposer le(s) commit(s) au user pour validation
- Mode B : pas de commit (analyse seule)
- Mode C : creer le(s) commit(s) automatiquement

## Difference avec les autres skills

| Skill | Input | Planification | Implementation |
|-------|-------|--------------|----------------|
| `/dev-jira-ticket` | Ticket Jira brut | Mini-plan interne | Oui |
| `/dev-story` | Story pre-planifiee dans un sprint | Deja faite | Oui |
| `/feature-planner` | Idee ou besoin | Plan complet avec stories | Non |
| `/quick-dev` | Description courte | Aucune | Oui |

## Modes

| Mode | Comportement | Plan | Implementation | Commit |
|------|-------------|------|----------------|--------|
| A (defaut) | Complet avec validation | Presente au user | Oui | Propose au user |
| B (`--analyze`) | Analyse seule | Presente au user | Non | Non |
| C (`--auto-commit`) | Complet automatique | Affiche sans attendre | Oui | Auto |
