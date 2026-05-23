---
name: somtech-pack-install
description: |
  Installer le somtech-pack dans le projet courant.
  TRIGGERS : installe le pack, install somtech, somtech-pack install, bootstrap somtech, init somtech, installe somtech-pack
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task
---

# Installer le somtech-pack dans le projet courant

Installe automatiquement le pack de configuration Somtech (skills, agents, rules, features, scripts) dans le projet courant via Claude Code.

## Prérequis

- Le projet courant doit être un repo git initialisé
- Accès réseau à GitHub (https://github.com/SomtechSolutionMAxime/somtech-pack.git)

## Phase 0 — Vérification

### 0.1 Vérifier si le pack est déjà installé

```bash
if [ -d ".claude/skills" ] && [ -f ".claude/CLAUDE.md" ]; then
  echo "⚠️  Le somtech-pack semble déjà installé (.claude/ existe)."
  echo "→ Utilise /somtech-pack-maj pour mettre à jour."
  exit 0
fi
```

Si le pack est déjà présent, **arrêter** et proposer `/somtech-pack-maj` à la place.

### 0.2 Vérifier que c'est un repo git

```bash
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
  echo "❌ Ce n'est pas un repo git. Initialise avec 'git init' d'abord."
  exit 1
fi
```

## Phase 1 — Cloner le pack

```bash
WORKDIR=$(mktemp -d)
echo "📦 Clonage du somtech-pack..."
git clone --depth 1 --branch main https://github.com/SomtechSolutionMAxime/somtech-pack.git "$WORKDIR/somtech-pack"
```

## Phase 2 — Dry-run et prévisualisation

```bash
"$WORKDIR/somtech-pack/scripts/install_somtech_pack.sh" --target "$(pwd)" --dry-run
```

**OBLIGATOIRE** : Afficher le résumé du dry-run à l'utilisateur et **attendre sa confirmation** avant de continuer.

Présenter :
1. Les dossiers qui seront créés/mis à jour
2. Les fichiers qui seront copiés
3. Si des fichiers existants seront écrasés (le script fait des backups `.bak`)

## Phase 3 — Installation

Après confirmation explicite de l'utilisateur :

```bash
"$WORKDIR/somtech-pack/scripts/install_somtech_pack.sh" --target "$(pwd)"
```

## Phase 4 — Nettoyage

```bash
rm -rf "$WORKDIR"
echo "🧹 Dossier temporaire nettoyé."
```

## Phase 5 — Post-installation

### 5.1 Personnalisation

Rappeler à l'utilisateur de personnaliser :

1. **`.claude/CLAUDE.md`** — Adapter les sections :
   - Sources de vérité (ontologie, constitution, sécurité)
   - Stack technique du projet
   - Ports de dev

2. **`.cursor/rules/`** — Remplacer les placeholders `{{...}}` si applicable

### 5.2 Proposer le commit

```bash
git add .claude/ .cursor/ features/ scripts/ docs/
git status
```

Montrer le `git status` et proposer :

```bash
git commit -m "chore: bootstrap somtech-pack"
```

**Attendre la confirmation** avant de commiter.

## Options

L'utilisateur peut demander une installation partielle. Passer les flags appropriés au script :

| Demande | Flags |
|---------|-------|
| "installe seulement les skills" | Copier uniquement `.claude/skills/` |
| "installe sans les docs" | `--no-docs` |
| "dry-run seulement" | `--dry-run` |

## Règles critiques

1. **Toujours** faire un dry-run et montrer le résumé avant d'installer
2. **Ne jamais** commiter sans confirmation explicite
3. **Ne jamais** écraser un `.claude/CLAUDE.md` personnalisé sans avertir (le script fait des `.bak`)
4. **Nettoyer** le dossier temporaire même en cas d'erreur
