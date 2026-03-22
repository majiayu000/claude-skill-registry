---
description: >
  Issue triage: audit open issues, categorize, detect duplicates, cross-ref PRs, risk assessment, post comments.
  Args: "all" for deep analysis of all, issue numbers to focus (e.g. "42 57"), "en"/"fr" for language, no arg = audit only in French.
---

# Issue Triage

## Quand utiliser

| Skill | Usage | Output |
|-------|-------|--------|
| `/issue-triage` | Trier, analyser, commenter les issues | Tableaux d'action + deep analysis + commentaires postés |

**Declencheurs** :
- Manuellement : `/issue-triage` ou `/issue-triage all` ou `/issue-triage 42 57`
- Proactivement : quand >10 issues ouvertes sans triage, ou issue stale >30j detectee

---

## Langue

- Verifier l'argument passe au skill
- Si `en` ou `english` -> tableaux et resume en anglais
- Si `fr`, `french`, ou pas d'argument -> francais (defaut)
- Note : les commentaires GitHub (Phase 3) restent TOUJOURS en anglais (audience internationale)

---

Workflow en 3 phases : audit automatique -> deep analysis opt-in -> commentaires avec validation obligatoire.

## Preconditions

```bash
git rev-parse --is-inside-work-tree
gh auth status
```

Si l'un echoue, stop et expliquer ce qui manque.

---

## Phase 1 -- Audit (toujours executee)

### Data Gathering (commandes en parallele)

```bash
# Identite du repo
gh repo view --json nameWithOwner -q .nameWithOwner

# Issues ouvertes avec metadonnees completes
gh issue list --state open --limit 100 \
  --json number,title,author,createdAt,updatedAt,labels,assignees,body,comments

# PRs ouvertes (pour cross-reference)
gh pr list --state open --limit 50 --json number,title,body

# Issues fermees recemment (pour detection doublons)
gh issue list --state closed --limit 20 \
  --json number,title,labels,closedAt

# Collaborateurs (pour proteger les issues des mainteneurs)
gh api "repos/{owner}/{repo}/collaborators" --jq '.[].login'
```

**Fallback collaborateurs** : si `gh api .../collaborators` echoue (403/404) :
```bash
gh pr list --state merged --limit 10 --json author --jq '.[].author.login' | sort -u
```
Si toujours ambigu, demander a l'utilisateur via `AskUserQuestion`.

**Note** : `author` est un objet `{login: "..."}` -- toujours extraire `.author.login`.

### Analyse -- 6 dimensions

**1. Categorisation** (labels existants > inference titre/body) :
- **Bug** : mots-cles `crash`, `error`, `fail`, `broken`, `regression`, `wrong`, `unexpected`, `panic`, `404`, `404`
- **Feature** : `add`, `implement`, `support`, `new`, `feat:`
- **Enhancement** : `improve`, `optimize`, `better`, `enhance`, `refactor`
- **Question/Support** : `how`, `why`, `help`, `unclear`, `docs`, `documentation`
- **Duplicate Candidate** : voir dimension 3 ci-dessous

**2. Cross-ref PRs** :
- Scanner `body` de chaque PR ouverte pour `fixes #N`, `closes #N`, `resolves #N` (case-insensitive, regex)
- Construire un map : `issue_number -> [PR numbers]`
- Une issue liee a une PR mergee -> recommander fermeture

**3. Detection doublons** :
- Normaliser les titres : lowercase, strip prefixes (`bug:`, `feat:`, `[bug]`, `[feature]`, etc.)
- **Jaccard sur mots des titres** : si score > 60% entre deux issues -> candidat doublon
- **Keywords body overlap** > 50% -> renforcement du signal
- Comparer aussi avec issues fermees recentes (20 dernieres)
- Un faux positif peut etre confirme/ecarte en Phase 2

**4. Classification risque** :
- **Rouge** : mots-cles `CVE`, `vulnerability`, `injection`, `auth bypass`, `security`, `exploit`, `unsafe`, `credentials`, `leak`, `RCE`, `XSS`, `panic`, `data loss`
- **Jaune** : `breaking change`, `migration`, `deprecation`, `remove API`, `breaking`, `incompatible`, `regression`
- **Vert** : tout le reste

**5. Staleness** :
- >30j sans activite (updatedAt) -> **Stale**
- >90j sans activite -> **Very Stale**
- Calculer depuis la date actuelle

**6. Recommandations d'action** :
- `Accept & Prioritize` : issue claire, reproducible, dans scope
- `Label needed` : issue sans label
- `Comment needed` : info manquante, body insuffisant
- `Linked to PR` : une PR ouverte reference cette issue
- `Duplicate candidate` : candidat doublon identifie (preciser avec `#N`)
- `Close candidate` : stale + aucune activite recente, ou hors scope (jamais si auteur est collaborateur)
- `PR merged -> close` : PR liee est mergee, issue encore ouverte

### Output -- 5 tableaux

```
## Issues ouvertes ({count})

### Critiques (risque rouge)
| # | Titre | Auteur | Age | Labels | Action |
| - | ----- | ------ | --- | ------ | ------ |

### Liees a une PR
| # | Titre | Auteur | PR(s) liee(s) | Status PR | Action |
| - | ----- | ------ | ------------- | --------- | ------ |

### Actives
| # | Titre | Auteur | Categorie | Age | Labels | Action |
| - | ----- | ------ | --------- | --- | ------ | ------ |

### Doublons candidats
| # | Titre | Doublon de | Similarite | Action |
| - | ----- | ---------- | ---------- | ------ |

### Stale
| # | Titre | Auteur | Derniere activite | Action |
| - | ----- | ------ | ----------------- | ------ |

### Resume
- Total : {N} issues ouvertes
- Critiques : {N} (risque securite ou breaking)
- Liees a PR : {N}
- Doublons candidats : {N}
- Stale (>30j) : {N} | Very Stale (>90j) : {N}
- Sans labels : {N}
- Quick wins (a fermer ou labeler rapidement) : {liste}
```

0 issues -> afficher `Aucune issue ouverte.` et terminer.

**Note** : `Age` = jours depuis `createdAt`, format `{N}j`. Si >30j, afficher en **gras**.

### Copie automatique

Apres affichage du tableau de triage, copier dans le presse-papier :
```bash
pbcopy <<'EOF'
{tableau de triage complet}
EOF
```
Confirmer : `Tableau copie dans le presse-papier.` (FR) / `Triage table copied to clipboard.` (EN)

---

## Phase 2 -- Deep Analysis (opt-in)

### Selection des issues

**Si argument passe** :
- `"all"` -> toutes les issues ouvertes
- Numeros (`"42 57"`) -> uniquement ces issues
- Pas d'argument -> proposer via `AskUserQuestion`

**Si pas d'argument**, afficher :

```
question: "Quelles issues voulez-vous analyser en profondeur ?"
header: "Deep Analysis"
multiSelect: true
options:
  - label: "Toutes ({N} issues)"
    description: "Analyse approfondie de toutes les issues avec agents en parallele"
  - label: "Critiques uniquement"
    description: "Focus sur les {M} issues a risque rouge/jaune"
  - label: "Doublons candidats"
    description: "Confirmer ou ecarter les {K} doublons detectes"
  - label: "Stale uniquement"
    description: "Decision close/keep sur les {J} issues stale"
  - label: "Passer"
    description: "Terminer ici -- juste l'audit"
```

Si "Passer" -> fin du workflow.

### Execution de l'analyse

Pour chaque issue selectionnee, lancer un agent via **Task tool en parallele** :

```
subagent_type: general-purpose
model: sonnet
prompt: |
  Analyze GitHub issue #{num}: "{title}" by @{author}

  **Metadata**: Created {createdAt}, last updated {updatedAt}, labels: {labels}

  **Body**:
  {body}

  **Existing comments** ({comments_count} total, showing last 5):
  {last_5_comments}

  **Context**:
  - Linked PRs: {linked_prs or "none"}
  - Duplicate candidate of: {duplicate_of or "none"}
  - Risk classification: {risk_color}

  Analyze this issue and return a structured report:
  ### Scope Assessment
  What is this issue actually asking for? Is it clearly defined?

  ### Missing Information
  What's needed to act on this? (reproduction steps, ccboard version, OS, install method used)

  ### Risk & Impact
  Security risk? Breaking change? Who's affected? Does it touch ~/.claude data?

  ### Effort Estimate
  XS (<1h) / S (1-4h) / M (1-2d) / L (3-5d) / XL (>1 week)

  ### Priority
  P0 (critical, act now) / P1 (high, this sprint) / P2 (medium, backlog) / P3 (low, someday)

  ### Recommended Action
  One of: Accept & Prioritize, Request More Info, Mark Duplicate (#N), Close (Stale), Close (Out of Scope), Link to Existing PR

  ### Draft Comment
  Draft a GitHub comment in English using the appropriate template from templates/issue-comment.md.
  Be specific, helpful, and constructive.
```

Si issue a >50 commentaires, resumer les 5 derniers uniquement.

Agreger tous les rapports. Afficher un resume apres toutes les analyses.

---

## Phase 3 -- Actions (validation obligatoire)

### Types d'actions possibles

- **Commenter** : `gh issue comment {num} --body-file -`
- **Labeler** : `gh issue edit {num} --add-label "{label}"` (skip si label deja present)
- **Fermer** : `gh issue close {num} --reason "not planned"` (jamais sans validation)

### Generation des drafts

Pour chaque issue analysee, generer les actions (commentaire + labels + fermeture si applicable) en utilisant `templates/issue-comment.md`.

**Regles** :
- Langue des commentaires : **anglais** (audience internationale)
- Ton : professionnel, constructif, factuel
- Ne jamais re-labeler une issue qui a deja ce label
- Ne jamais proposer "close" pour une issue d'un collaborateur
- Toujours afficher le draft AVANT tout `gh issue comment`

### Affichage et validation

**Afficher TOUS les drafts** au format :

```
---
### Draft -- Issue #{num}: {title}

**Actions proposees** : {Commentaire | Label: "bug" | Fermeture}

**Commentaire** :
{commentaire complet}

---
```

Puis demander validation via `AskUserQuestion` :

```
question: "Ces actions sont pretes. Lesquelles voulez-vous executer ?"
header: "Executer"
multiSelect: true
options:
  - label: "Toutes ({N} actions)"
    description: "Commenter + labeler + fermer selon les drafts"
  - label: "Issue #{x} -- {title_truncated}"
    description: "Executer uniquement les actions pour cette issue"
  - label: "Aucune"
    description: "Annuler -- ne rien faire"
```

(Generer une option par issue + "Toutes" + "Aucune")

### Execution

Pour chaque action validee, executer dans l'ordre : commenter -> labeler -> fermer.

```bash
# Commenter
gh issue comment {num} --body-file - <<'COMMENT_EOF'
{commentaire}
COMMENT_EOF

# Labeler (si applicable)
gh issue edit {num} --add-label "{label}"

# Fermer (si applicable)
gh issue close {num} --reason "not planned"
```

Confirmer chaque action : `Commentaire poste sur issue #{num}: {title}`

Si "Aucune" -> `Aucune action executee. Workflow termine.`

---

## Gestion des cas limites

| Situation | Comportement |
|-----------|--------------|
| 0 issues ouvertes | `Aucune issue ouverte.` + terminer |
| Issue sans body | Categoriser par titre, recommander `Comment needed` |
| >50 commentaires | Resumer les 5 derniers uniquement |
| Faux positif doublon | Phase 2 confirme/ecarte -- ne pas agir sur suspicion seule |
| Labels deja presents | Ne pas re-labeler, signaler "label deja applique" |
| Issue d'un collaborateur | Jamais `close candidate` automatique |
| Rate limit GitHub API | Reduire `--limit`, notifier l'utilisateur |
| PR mergee liee a issue ouverte | Recommander fermeture de l'issue |
| Issue sans activite >90j | Very Stale -- proposer fermeture avec message bienveillant |
| Duplicate confirmed in Phase 2 | Poster commentaire + fermer en faveur de l'issue originale |

---

## Notes

- Toujours deriver owner/repo via `gh repo view`, jamais hardcoder
- Utiliser `gh` CLI (pas `curl` GitHub API) sauf pour la liste des collaborateurs
- `updatedAt` peut etre null sur certaines issues -> traiter comme `createdAt`
- Ne jamais poster ou fermer sans validation explicite de l'utilisateur dans le chat
- Les commentaires draftes doivent etre visibles AVANT tout `gh issue comment`
- Similarite Jaccard = |intersection mots| / |union mots| (exclure stop words : a, the, is, in, of, for, to, with, on, at, by)
