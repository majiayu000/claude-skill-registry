---
name: somtech-pack-maj
description: |
  Mettre à jour le projet courant depuis le somtech-pack (pull).
  TRIGGERS : somtech-pack-maj, mise à jour pack, update pack, sync pack, pull pack, maj somtech, mettre à jour le pack
  Détecte les changements disponibles, affiche un résumé, et applique la mise à jour.
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Somtech Pack — Mise à jour projet

Mettre à jour les fichiers de configuration, skills, rules et commandes du projet courant depuis la dernière version du somtech-pack.

## Phase 0 — Pré-vérifications

### 0.1 Vérifier qu'on est dans un projet client

```bash
# Vérifier qu'on est dans un repo git
git rev-parse --show-toplevel

# Vérifier qu'il y a déjà une config Somtech
ls .claude/ .cursor/ 2>/dev/null
```

Si `.claude/` ou `.cursor/` n'existent pas, avertir l'utilisateur qu'il s'agit peut-être d'une première installation (utiliser `install_somtech_pack.sh` plutôt).

### 0.2 Vérifier les prérequis

```bash
# Git dispo
git --version

# Réseau accessible (test rapide)
git ls-remote https://github.com/SomtechSolutionMAxime/somtech-pack.git HEAD 2>/dev/null | head -1
```

Si le réseau n'est pas accessible, proposer une mise à jour depuis un clone local si l'utilisateur en a un.

### 0.3 Vérifier l'état git du projet

```bash
# Vérifier s'il y a des changements non commités dans les dossiers pack
git status --short .claude/ .cursor/ docs/ scripts/
```

Si des fichiers modifiés sont détectés dans ces dossiers :
- **Avertir** l'utilisateur que la MAJ va écraser ses modifications locales
- **Lister** les fichiers en conflit potentiel
- **Demander confirmation** avant de continuer
- **Suggérer** de faire un `somtech_pack_push.sh` d'abord si les changements doivent être publiés vers le pack

## Phase 1 — Analyser les changements disponibles

### 1.1 Cloner le pack pour comparaison

```bash
WORKDIR=$(mktemp -d)
git clone --depth 1 --branch main https://github.com/SomtechSolutionMAxime/somtech-pack.git "$WORKDIR/somtech-pack" 2>/dev/null
```

### 1.2 Comparer les fichiers

Pour chaque dossier synchronisé, comparer le contenu local avec le pack :

```bash
# .claude/ — skills, agents, templates, settings
diff -rq .claude/ "$WORKDIR/somtech-pack/.claude/" 2>/dev/null | grep -v ".DS_Store"

# .cursor/ — commands, rules, skills
diff -rq .cursor/ "$WORKDIR/somtech-pack/.cursor/" 2>/dev/null | grep -v ".DS_Store"

# features/ — blueprints de features
diff -rq features/ "$WORKDIR/somtech-pack/features/" 2>/dev/null | grep -v ".DS_Store"

# scripts/
diff -rq scripts/ "$WORKDIR/somtech-pack/scripts/" 2>/dev/null | grep -v ".DS_Store"
```

### 1.3 Catégoriser les changements

Classer les fichiers en 3 catégories et présenter à l'utilisateur :

| Catégorie | Description | Action |
|-----------|-------------|--------|
| **Nouveaux** | Fichiers dans le pack mais pas dans le projet | Seront ajoutés |
| **Modifiés** | Fichiers différents entre pack et projet | Seront mis à jour |
| **Supprimés** | Fichiers dans le projet mais plus dans le pack | Seront signalés (pas supprimés automatiquement) |

### 1.4 Afficher le résumé

Présenter un résumé clair :

```
📦 SOMTECH-PACK — Changements disponibles
──────────────────────────────────────────

🆕 Nouveaux (X fichiers):
   .claude/skills/deploy-metering/SKILL.md
   features/metering-billing/overview.md
   ...

📝 Modifiés (Y fichiers):
   .claude/CLAUDE.md
   .cursor/rules/somtech.md
   ...

⚠️  Fichiers locaux uniquement (Z fichiers):
   .claude/skills/custom-local/SKILL.md  ← pas dans le pack
   ...

Appliquer la mise à jour ? (les fichiers locaux uniquement ne seront PAS supprimés)
```

**Attendre la confirmation de l'utilisateur avant de continuer.**

## Phase 2 — Appliquer la mise à jour

### 2.1 Option A — Via le script officiel (recommandé)

Si le script `somtech_pack_pull.sh` est accessible :

```bash
# Depuis le projet courant
./scripts/somtech_pack_pull.sh --target .
```

Ou si le script n'est pas encore dans le projet :

```bash
"$WORKDIR/somtech-pack/scripts/somtech_pack_pull.sh" --target .
```

### 2.2 Option B — Copie manuelle (fallback)

Si le script n'est pas disponible ou échoue, copier manuellement :

```bash
PROJECT_ROOT=$(git rev-parse --show-toplevel)

# .claude/
rsync -av --exclude='.DS_Store' "$WORKDIR/somtech-pack/.claude/" "$PROJECT_ROOT/.claude/"

# .cursor/
rsync -av --exclude='.DS_Store' "$WORKDIR/somtech-pack/.cursor/" "$PROJECT_ROOT/.cursor/"

# features/
rsync -av --exclude='.DS_Store' "$WORKDIR/somtech-pack/features/" "$PROJECT_ROOT/features/"

# scripts/
rsync -av --exclude='.DS_Store' "$WORKDIR/somtech-pack/scripts/" "$PROJECT_ROOT/scripts/"
```

### 2.3 Nettoyage

```bash
rm -rf "$WORKDIR"
```

## Phase 3 — Post-mise à jour

### 3.1 Vérifier l'installation

```bash
# Lister les skills disponibles
ls .claude/skills/

# Vérifier le CLAUDE.md
head -5 .claude/CLAUDE.md
```

### 3.2 Résumé final

```
✅ SOMTECH-PACK MIS À JOUR
──────────────────────────
Fichiers ajoutés  : X
Fichiers modifiés : Y
Version pack      : main@<commit-sha>

📋 Nouveaux skills disponibles :
   /deploy-metering — Déployer métriques et facturation
   ...

⚠️  Actions recommandées :
   - Vérifier que .claude/CLAUDE.md contient les bonnes sources de vérité pour ce projet
   - Commiter les changements : git add .claude/ .cursor/ features/ scripts/ && git commit -m "chore(pack): sync somtech-pack"
```

### 3.3 Proposer le commit

Proposer à l'utilisateur de commiter les changements avec un message conventionnel :

```bash
git add .claude/ .cursor/ features/ scripts/
git commit -m "chore(pack): sync somtech-pack $(date +%Y-%m-%d)"
```

**Ne PAS commiter sans confirmation explicite de l'utilisateur.**

## Options avancées

L'utilisateur peut demander une mise à jour partielle :

| Demande | Comportement |
|---------|-------------|
| "maj skills seulement" | Synchroniser uniquement `.claude/skills/` |
| "maj sans écraser mon CLAUDE.md" | Exclure `.claude/CLAUDE.md` de la sync |
| "maj depuis une branche" | Utiliser `--ref <branche>` pour le pull |
| "dry-run" | Ajouter `--dry-run` pour preview sans écriture |
| "maj + push mes changements" | Faire un push d'abord, puis un pull |

Pour les mises à jour partielles, utiliser les flags du script :

```bash
./scripts/somtech_pack_pull.sh --target . --no-rules    # Sans rules Cursor
./scripts/somtech_pack_pull.sh --target . --no-commands  # Sans commandes
./scripts/somtech_pack_pull.sh --target . --no-skills    # Sans skills
./scripts/somtech_pack_pull.sh --target . --no-docs      # Sans docs
./scripts/somtech_pack_pull.sh --target . --somtech-only  # Somtech config uniquement
```

## Règles critiques

1. **Ne JAMAIS écraser sans confirmation** — toujours montrer le diff d'abord
2. **Ne JAMAIS push sur main** — si un commit est nécessaire, le faire sur la branche courante
3. **Ne JAMAIS supprimer** des fichiers locaux qui ne sont pas dans le pack (l'utilisateur peut avoir des skills custom)
4. **Toujours nettoyer** le dossier temporaire de travail après l'opération
5. **Proposer le push** si des changements locaux pertinents sont détectés avant le pull
