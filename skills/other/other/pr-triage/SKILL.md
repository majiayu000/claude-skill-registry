---
description: >
  PR triage: audit open PRs, deep review selected ones, draft and post review comments.
  Args: "all" to review all, PR numbers to focus (e.g. "42 57"), "en"/"fr" for language, no arg = audit only in French.
---

# PR Triage

## Quand utiliser

| Skill | Usage | Output |
|-------|-------|--------|
| `/pr-triage` | Trier, reviewer, commenter les PRs | Tableau d'action + reviews + commentaires postes |

**Declencheurs** :
- Manuellement : `/pr-triage` ou `/pr-triage all` ou `/pr-triage 42 57`
- Proactivement : quand >5 PRs ouvertes sans review, ou PR stale >14j detectee

---

## Langue

- Verifier l'argument passe au skill
- Si `en` ou `english` -> tableaux et resume en anglais
- Si `fr`, `french`, ou pas d'argument -> francais (defaut)
- Note : les commentaires GitHub (Phase 3) restent TOUJOURS en anglais (audience internationale)

---

Workflow en 3 phases : audit automatique -> deep review opt-in -> commentaires avec validation obligatoire.

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

# PRs ouvertes avec metadonnees completes
gh pr list --state open --limit 50 \
  --json number,title,author,createdAt,updatedAt,additions,deletions,changedFiles,isDraft,mergeable,reviewDecision,statusCheckRollup,body

# Collaborateurs (pour distinguer "nos PRs" des externes)
gh api "repos/{owner}/{repo}/collaborators" --jq '.[].login'
```

**Fallback collaborateurs** : si `gh api .../collaborators` echoue (403/404) :
```bash
gh pr list --state merged --limit 10 --json author --jq '.[].author.login' | sort -u
```
Si toujours ambigu, demander a l'utilisateur via `AskUserQuestion`.

Pour chaque PR, recuperer reviews existantes ET fichiers modifies :

```bash
gh api "repos/{owner}/{repo}/pulls/{num}/reviews" \
  --jq '[.[] | .user.login + ":" + .state] | join(", ")'

# Fichiers modifies (necessaire pour overlap detection)
gh pr view {num} --json files --jq '[.files[].path] | join(",")'
```

**Note rate-limiting** : la recuperation des fichiers est N appels API (1 par PR). Pour repos avec 20+ PRs, prioriser les PRs candidates a l'overlap (meme domaine fonctionnel, meme auteur).

**Note** : `author` est un objet `{login: "..."}` -- toujours extraire `.author.login`.

### Analyse

**Classification taille** :
| Label | Additions |
|-------|-----------|
| XS | < 50 |
| S | 50-200 |
| M | 200-500 |
| L | 500-1000 |
| XL | > 1000 |

Format taille : `+{additions}/-{deletions}, {files} files ({label})`

**Detections** :
- **Overlaps** : comparer les listes de fichiers entre PRs -- si >50% de fichiers en commun -> cross-reference
- **Clusters** : auteur avec 3+ PRs ouvertes -> suggerer ordre de review (plus petite en premier)
- **Staleness** : aucune activite depuis >14j -> flag "stale"
- **CI status** : via `statusCheckRollup` -> `clean` / `unstable` / `dirty`
- **Reviews** : approved / changes_requested / aucune

**Liens PR <-> Issues** :
- Scanner le `body` de chaque PR pour `fixes #N`, `closes #N`, `resolves #N` (case-insensitive)
- Si trouve, afficher dans le tableau : `Fixes #42` dans la colonne Action/Status

**Categorisation** :

_Nos PRs_ : auteur dans la liste des collaborateurs

_Externes -- Pretes_ : additions <= 1000 ET files <= 10 ET `mergeable` != `CONFLICTING` ET CI clean/unstable

_Externes -- Problematiques_ : un des criteres suivants :
- additions > 1000 OU files > 10
- OU `mergeable` == `CONFLICTING` (conflit de merge)
- OU CI dirty (statusCheckRollup contient des echecs)
- OU overlap avec une autre PR ouverte (>50% fichiers communs)

### Output -- Tableau de triage

```
## PRs ouvertes ({count})

### Nos PRs
| PR | Titre | Taille | CI | Status |
| -- | ----- | ------ | -- | ------ |

### Externes -- Pretes pour review
| PR | Auteur | Titre | Taille | CI | Reviews | Action |
| -- | ------ | ----- | ------ | -- | ------- | ------ |

### Externes -- Problematiques
| PR | Auteur | Titre | Taille | Probleme | Action recommandee |
| -- | ------ | ----- | ------ | -------- | ------------------ |

### Resume
- Quick wins : {PRs XS/S pretes a merger}
- Risques : {overlaps, tailles XL, CI dirty}
- Clusters : {auteurs avec 3+ PRs}
- Stale : {PRs sans activite >14j}
- Overlaps : {PRs qui touchent les memes fichiers}
```

0 PRs -> afficher `Aucune PR ouverte.` et terminer.

### Copie automatique

Apres affichage du tableau de triage, copier dans le presse-papier :
```bash
pbcopy <<'EOF'
{tableau de triage complet}
EOF
```
Confirmer : `Tableau copie dans le presse-papier.` (FR) / `Triage table copied to clipboard.` (EN)

---

## Phase 2 -- Deep Review (opt-in)

### Selection des PRs

**Si argument passe** :
- `"all"` -> toutes les PRs externes
- Numeros (`"42 57"`) -> uniquement ces PRs
- Pas d'argument -> proposer via `AskUserQuestion`

**Si pas d'argument**, afficher :

```
question: "Quelles PRs voulez-vous reviewer en profondeur ?"
header: "Deep Review"
multiSelect: true
options:
  - label: "Toutes les externes"
    description: "Review {N} PRs externes avec rust-ccboard en parallele"
  - label: "Problematiques uniquement"
    description: "Focus sur les {M} PRs a risque (CI dirty, trop large, overlaps)"
  - label: "Pretes uniquement"
    description: "Review {K} PRs pretes a merger"
  - label: "Passer"
    description: "Terminer ici -- juste l'audit"
```

**Note sur les drafts** :
- Les PRs en draft sont EXCLUES des options "Toutes les externes" et "Pretes uniquement"
- Les PRs en draft sont INCLUSES dans "Problematiques uniquement"
- Pour reviewer un draft : taper son numero explicitement (ex: `42`)

Si "Passer" -> fin du workflow.

### Execution des Reviews

Pour chaque PR selectionnee, lancer un agent `rust-ccboard` via **Task tool en parallele** :

```
subagent_type: rust-ccboard
model: sonnet
prompt: |
  Review PR #{num}: "{title}" by @{author}

  **Metadata**: +{additions}/-{deletions}, {changedFiles} files ({size_label})
  **CI**: {ci_status} | **Reviews**: {existing_reviews} | **Draft**: {isDraft}

  **PR Body**:
  {body}

  **Diff**:
  {gh pr diff {num} output}

  Apply your security-guardian and backend-architect skills for this review.
  Additionally, apply the ccboard Rust review checklist:

  CRITICAL (block merge if violated):
  - anyhow::Result + .context("msg") on every ? -- no bare ?, no .unwrap() in production code
  - parking_lot::RwLock (not std::sync::RwLock) for shared state
  - No blocking in async context (use tokio::time::sleep, tokio::task::spawn_blocking for I/O)
  - Graceful degradation: parsers must return Option<T> and populate LoadReport, never panic on malformed input
  - cargo fmt --all + cargo clippy --all-targets must pass (zero warnings)
  - Tests in #[cfg(test)] mod tests with real fixtures from tests/fixtures/ (not synthetic data)

  IMPORTANT (should fix before merge):
  - thiserror in ccboard-core (library crate), anyhow in ccboard-tui/ccboard-web/ccboard (binaries)
  - No full JSONL file loading at startup -- metadata-only via BufReader line-by-line
  - Arc<DataStore> for shared ownership (NOT DashMap -- removed in v0.4.0, 50x memory reduction)
  - parking_lot::RwLock for low-contention shared state (stats, config) -- not std::sync::RwLock
  - Startup performance target maintained: <2s for 1000+ sessions
  - Read-only constraint: no writes to ~/.claude/* (monitoring only)

  SUGGESTIONS (nice to have):
  - Arc<T> for shared ownership instead of cloning large structs
  - JoinSet for bounded parallel scanning
  - tokio::sync::broadcast for EventBus updates

  Return structured review:
  ### Critical Issues (block merge)
  ### Important Issues (should fix)
  ### Suggestions (nice to have)
  ### What's Good

  Be specific: cite file:line, explain the problem, suggest the fix.
```

Recuperer le diff via :
```bash
gh pr diff {num}
gh pr view {num} --json body,title,author -q '{body: .body, title: .title, author: .author.login}'
```

Agreger tous les rapports. Afficher un resume apres toutes les reviews.

---

## Phase 3 -- Commentaires (validation obligatoire)

### Generation des drafts

Pour chaque PR reviewee, generer un commentaire GitHub en utilisant le template `templates/review-comment.md`.

**Regles** :
- Langue : **anglais** (audience internationale)
- Ton : professionnel, constructif, factuel
- Toujours inclure au moins 1 point positif
- Citer les lignes de code quand pertinent (format `file.rs:42`)

### Affichage et validation

**Afficher TOUS les commentaires draftes** au format :

```
---
### Draft -- PR #{num}: {title}

{commentaire complet}

---
```

Puis demander validation via `AskUserQuestion` :

```
question: "Ces commentaires sont prets. Lesquels voulez-vous poster ?"
header: "Poster"
multiSelect: true
options:
  - label: "Tous ({N} commentaires)"
    description: "Poster sur toutes les PRs reviewees"
  - label: "PR #{x} -- {title_truncated}"
    description: "Poster uniquement sur cette PR"
  - label: "Aucun"
    description: "Annuler -- ne rien poster"
```

(Generer une option par PR + "Tous" + "Aucun")

### Posting

Pour chaque commentaire valide :

```bash
gh pr comment {num} --body-file - <<'REVIEW_EOF'
{commentaire}
REVIEW_EOF
```

Confirmer chaque post : `Commentaire poste sur PR #{num}: {title}`

Si "Aucun" -> `Aucun commentaire poste. Workflow termine.`

---

## Gestion des cas limites

| Situation | Comportement |
|-----------|--------------|
| 0 PRs ouvertes | `Aucune PR ouverte.` + terminer |
| PR en draft | Indiquer dans tableau, skip pour review sauf si selectionnee explicitement |
| CI inconnu | Afficher `?` dans colonne CI |
| Review agent timeout | Afficher erreur partielle, continuer avec les autres |
| `gh pr diff` vide | Skip cette PR, notifier l'utilisateur |
| PR tres large (>5000 additions) | Avertir : "Review partielle, diff tronque" |
| Collaborateurs API 403/404 | Fallback sur auteurs des 10 derniers PRs merges |

---

## Notes

- Toujours deriver owner/repo via `gh repo view`, jamais hardcoder
- Utiliser `gh` CLI (pas `curl` GitHub API) sauf pour la liste des collaborateurs
- `statusCheckRollup` peut etre null -> traiter comme `?`
- `mergeable` peut etre `MERGEABLE`, `CONFLICTING`, ou `UNKNOWN` -> traiter `UNKNOWN` comme `?`
- Ne jamais poster sans validation explicite de l'utilisateur dans le chat
- Les commentaires draftes doivent etre visibles AVANT tout `gh pr comment`
