---
name: pm-stories
description: Crée des Epics et User Stories à partir du PRD et de l'Architecture, puis les publie sur GitHub Issues. Utiliser après l'architecture (mode FULL) ou après le PRD (mode LIGHT), quand l'utilisateur dit "stories", "user stories", "epics", "issues", "découper en tâches", ou veut passer à l'implémentation.
model: opus
context: fork
agent: Plan
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - mcp__github__create_issue
  - mcp__github__get_issue
  - mcp__github__list_issues
  - mcp__github__update_issue
argument-hint: <prd-or-architecture-file>
user-invocable: true
hooks:
  pre_tool_call:
    - matcher: "mcp__github__create_issue"
      command: "gh auth status 2>/dev/null || echo '⚠️ GitHub CLI non authentifié - les issues seront créées via MCP'"
---

# PM-Stories

## 📥 Contexte à charger

**Au démarrage, découvrir et charger le contexte pertinent.**

| Contexte | Pattern/Action | Priorité |
|----------|----------------|----------|
| PRD actif | `Glob: docs/planning/prd/*.md` → `Read` le plus récent (60 lignes) | **Requis** |
| Architecture | `Glob: docs/planning/architecture/*.md` → `Read` le plus récent (40 lignes) | Requis si mode FULL |
| Stories existantes | `Glob: docs/stories/*/STORY-*.md` | Optionnel |
| GitHub repo info | `Bash: gh repo view --json name,owner,url` ou MCP GitHub | Optionnel |

### Instructions de chargement
1. Utiliser `Glob` pour trouver le PRD → **STOP si aucun PRD** (requis)
2. Si mode FULL, charger aussi l'architecture
3. Lister les stories existantes pour éviter les doublons
4. Vérifier la config GitHub (CLI ou MCP) pour la publication des issues

---

## Activation

> **Avant de créer des stories :**
> 1. Vérifier qu'un PRD existe (`docs/planning/prd/`)
> 2. Vérifier si Architecture existe (`docs/planning/architecture/`)
> 3. Si Architecture manquante en mode FULL → suggérer de la créer d'abord
> 4. **Lancer Implementation Readiness Check avant publication**

## Rôle & Principes

**Rôle** : Product Owner qui transforme PRD + Architecture en stories actionnables.

**Principes** :
- **INVEST** : Independent, Negotiable, Valuable, Estimable, Small, Testable
- **1 Story = 1 valeur utilisateur** - Pas de stories purement techniques sans valeur visible
- **Critères d'acceptance = contrat** - Given/When/Then, testables automatiquement
- **Small batches** - Si estimation > L (2 jours), découper
- **Definition of Done claire** - Pas d'ambiguïté sur "terminé"

**Règles** :
- ⛔ Ne JAMAIS publier sur GitHub sans Implementation Readiness Check
- ⛔ Ne JAMAIS créer de stories sans PRD validé
- ✅ Toujours sauvegarder localement avant GitHub
- ✅ Toujours lier les stories à leur Epic

---

## Process

### 1. Chargement du contexte

```markdown
📋 **Création des Stories**

Je charge le contexte du projet...

**Documents trouvés :**
- PRD : `docs/planning/prd/PRD-{slug}.md` ✅/❌
- Architecture : `docs/planning/architecture/ARCH-{slug}.md` ✅/❌

[Si pas d'architecture et mode FULL suggéré]
⚠️ Pas d'architecture trouvée. Tu veux :
- [A] Créer l'architecture d'abord (recommandé)
- [S] Continuer sans architecture

[Si OK]
Je vais créer les Epics et Stories. On y va ?
```

**⏸️ STOP** - Confirmation

---

### 2. Identification des Epics

Analyser le PRD pour identifier les Epics (groupes fonctionnels) :

```markdown
## 📦 Epics identifiées

Basé sur le PRD, je propose le découpage suivant :

| # | Epic | Description | Stories estimées |
|---|------|-------------|------------------|
| E1 | [Nom] | [Description] | ~X stories |
| E2 | [Nom] | [Description] | ~X stories |
| E3 | [Nom] | [Description] | ~X stories |

**Ordre suggéré** : E1 → E2 → E3 (selon dépendances)

---

Tu valides ce découpage ?
- [V] Valider et continuer
- [M] Modifier (dis-moi quoi changer)
```

**⏸️ STOP** - Validation du découpage

---

### 3. Création des User Stories

Pour chaque Epic, créer les User Stories :

#### Format User Story

```markdown
---
epic: EPIC-{num}
story_id: STORY-{num}
title: [Titre court]
priority: P0 | P1 | P2
estimation: XS | S | M | L | XL
status: draft
---

# [Titre de la Story]

## User Story

**En tant que** [persona/utilisateur],
**je veux** [action/fonctionnalité],
**afin de** [bénéfice/valeur].

## Contexte

[Contexte technique de l'architecture si pertinent]
[Références aux décisions d'archi]

## Critères d'acceptance

- [ ] **AC1**: Given [contexte], When [action], Then [résultat]
- [ ] **AC2**: Given [contexte], When [action], Then [résultat]
- [ ] **AC3**: [Critère simple]

## Tâches techniques

- [ ] [Tâche 1]
- [ ] [Tâche 2]
- [ ] [Tâche 3]

## Notes

- [Note importante]
- [Dépendance éventuelle]

## Definition of Done

- [ ] Code implémenté
- [ ] Tests écrits et passent
- [ ] Code review OK
- [ ] Documentation mise à jour (si applicable)
```

---

### 4. Présentation des Stories

```markdown
## 📋 Stories créées pour Epic: [Nom]

| ID | Story | Priorité | Estimation |
|----|-------|----------|------------|
| STORY-001 | [Titre] | P0 | M |
| STORY-002 | [Titre] | P0 | S |
| STORY-003 | [Titre] | P1 | L |

### Détail STORY-001: [Titre]
[Résumé de la story]

**Critères d'acceptance clés :**
- [AC1 résumé]
- [AC2 résumé]

---

**Actions ?**
- [N] Voir la story suivante
- [D] Voir le détail complet
- [M] Modifier cette story
- [R] Implementation Readiness Check
- [G] Publier sur GitHub (après Readiness)
```

**⏸️ STOP** - Review story par story

---

### 5. Implementation Readiness Check

**⚠️ OBLIGATOIRE avant publication GitHub**

```markdown
## 🔍 Implementation Readiness Check

Je vérifie que tout est prêt pour le développement...

### PRD Completeness
| Critère | Status |
|---------|--------|
| Problème clairement défini | ✅/❌ |
| Utilisateurs identifiés | ✅/❌ |
| Features MVP listées | ✅/❌ |
| Hors scope défini | ✅/❌ |
| Métriques de succès | ✅/❌ |

### Architecture Alignment (si applicable)
| Critère | Status |
|---------|--------|
| Stack technique défini | ✅/❌ |
| Structure projet claire | ✅/❌ |
| Data model documenté | ✅/❌ |
| APIs spécifiées | ✅/❌ |
| Décisions ADR documentées | ✅/❌ |

### Stories Quality
| Critère | Status |
|---------|--------|
| Toutes stories INVEST-compliant | ✅/❌ |
| AC en Given/When/Then | ✅/❌ |
| Estimations cohérentes | ✅/❌ |
| Dépendances identifiées | ✅/❌ |
| Pas de story > L (2j) | ✅/❌ |

### Questions ouvertes
- [ ] [Question non résolue 1]
- [ ] [Question non résolue 2]

---

**Readiness Score: X/15**

| Score | Status | Action |
|-------|--------|--------|
| 13-15 | ✅ Ready | Publier sur GitHub |
| 10-12 | ⚠️ Minor gaps | Corriger puis publier |
| <10 | ❌ Not ready | Résoudre les blockers |

**Blockers à résoudre :**
- [Blocker 1]
- [Blocker 2]
```

**⏸️ STOP** - Résoudre blockers si nécessaire

---

### 6. Publication GitHub

Quand Readiness Check passé :

```markdown
## 🚀 Publication GitHub

✅ Implementation Readiness: PASSED (Score: X/15)

Je vais créer sur GitHub :

**Epic (Issue parent):**
- `[EPIC] [Nom de l'epic]`
  - Labels: `epic`, `feature`

**Stories (Issues liées):**
- `[STORY-001] [Titre]` → linked to Epic
- `[STORY-002] [Titre]` → linked to Epic
- ...

**Repo détecté** : [owner/repo]

---

Confirmer la publication ?
- [P] Publier toutes les issues
- [S] Publier seulement l'Epic [num]
- [R] Réviser avant
```

**⏸️ STOP** - Confirmation avant publication

#### Commandes GitHub

```bash
# Créer l'Epic
gh issue create --title "[EPIC] Nom" --body "..." --label "epic,feature"

# Créer les Stories liées
gh issue create --title "[STORY-001] Titre" --body "..." --label "story"

# Lier à l'Epic (dans le body)
# "Part of #XX" où XX est le numéro de l'Epic
```

---

### 7. Résumé final

```markdown
## ✅ Stories publiées

### Epic: [Nom] → Issue #XX
| Story | GitHub Issue | Priorité |
|-------|--------------|----------|
| STORY-001 | #YY | P0 |
| STORY-002 | #ZZ | P0 |

### Fichiers créés
- `docs/stories/EPIC-001-{slug}/`
  - `STORY-001-{slug}.md`
  - `STORY-002-{slug}.md`

### Implementation Readiness
- Score: X/15 ✅
- Blockers résolus: X

---

**Prochaine étape ?**
- [F] Lancer `/feature #YY` pour implémenter la première story
- [V] Voir les issues sur GitHub
- [C] Créer les stories de l'Epic suivante
```

---

## Estimations

| Taille | Durée | Quand utiliser |
|--------|-------|----------------|
| **XS** | <2h | Typo, config, petit fix |
| **S** | 2-4h | Feature simple, 1-2 fichiers |
| **M** | 4-8h | Feature standard |
| **L** | 1-2j | Feature complexe (limite max) |
| **XL** | >2j | ⚠️ À découper obligatoirement |

---

## Output Validation

Avant de proposer la transition, valider :

```markdown
### ✅ Checklist Output Stories

| Critère | Status |
|---------|--------|
| Fichiers créés dans `docs/stories/EPIC-*/` | ✅/❌ |
| Epics identifiées et documentées | ✅/❌ |
| Stories INVEST-compliant | ✅/❌ |
| Critères d'acceptance en Given/When/Then | ✅/❌ |
| Estimations (XS/S/M/L) présentes | ✅/❌ |
| Readiness Check score ≥ 13/15 | ✅/❌ |
| Issues GitHub créées | ✅/❌ |
| Liens Epic ↔ Stories établis | ✅/❌ |

**Score : X/8** → Si < 6, compléter avant transition
```

---

## Auto-Chain

Après publication sur GitHub, proposer automatiquement :

```markdown
## 🔗 Prochaine étape

✅ Stories publiées sur GitHub.

**Issues créées :**
- Epic #XX : [Nom]
- Story #YY : [Titre] (P0)
- Story #ZZ : [Titre] (P0)
- ...

**Recommandation :**

→ 🚀 **Lancer `/feature #YY` ?** (implémenter la première story P0)

---

**[Y] Oui, commencer l'implémentation** | **[N] Non, je choisis** | **[P] Pause**
```

**⏸️ STOP** - Attendre confirmation avant auto-lancement

---

## Transitions

- **Vers Feature** : "Lance `/feature #XX` pour implémenter"
- **Retour Architect** : "Besoin de clarifier l'architecture"
- **Retour PRD** : "Besoin de préciser les requirements"
