---
name: git-module
description: Gestion des modules Git (submodules). Ajouter, synchroniser et gérer les maquettes.
argument-hint: <command> [options]
disable-model-invocation: true
---

# Git-Module - Gestion des Submodules

Tu gères les modules Git (submodules) du projet. Les maquettes sont stockées comme submodules et doivent être synchronisées avant d'utiliser `/mockmig`.

## Commande reçue

L'utilisateur a exécuté: `/git-module $ARGUMENTS`

## Instructions par commande

| Argument | Fichier à lire | Description |
|----------|----------------|-------------|
| `add` | `.claude/skills/git-module/phases/add.md` | Ajouter un nouveau submodule |
| `sync` | `.claude/skills/git-module/phases/sync.md` | Synchroniser les submodules |
| `list` | `.claude/skills/git-module/phases/list.md` | Lister les submodules |
| `status` | `.claude/skills/git-module/phases/status.md` | État de synchronisation |
| `remove` | `.claude/skills/git-module/phases/remove.md` | Retirer un submodule |
| (vide) | - | Afficher l'aide ci-dessous |

## Si aucun argument ou argument invalide

Affiche:

```
📦 GIT-MODULE - Gestion des Submodules
======================================

Gérer les maquettes stockées comme git submodules.

Usage:
  /git-module <command> [options]

Commandes:
  add <url> [path]     Ajouter un nouveau submodule
  sync [--all]         Synchroniser les submodules
  list                 Lister les submodules existants
  status               Voir l'état de synchronisation
  remove <path>        Retirer un submodule

Exemples:
  /git-module add git@github.com:somtech/maquette-devis.git modules/maquette/devis/v1
  /git-module sync --all
  /git-module status

Workflow typique:
  1. /git-module add <url> <path>    # Ajouter la maquette
  2. /git-module sync                 # S'assurer qu'elle est à jour
  3. /mockmig init --module <x> --mockupPath <path>  # Migrer
```

## Conventions

- **Chemin des maquettes**: `modules/maquette/<module>/<version>`
- **Versions**: `v1`, `v2`, etc. (ou `main` pour la version courante)
- **Branches**: Chaque submodule suit sa propre branche (généralement `main`)

## Sortie

- Afficher les commandes git exécutées
- Utiliser des émojis pour le statut (✅ ⚠️ ❌)
- Montrer les différences de version si désync
