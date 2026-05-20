---
name: mockmig
description: Workflow de migration de maquettes Git vers production. Phases - init, discover, analyze, plan, execute, status.
argument-hint: <phase> [options]
disable-model-invocation: true
---

# Mockmig - Migration de Maquettes

Tu es l'assistant de migration mockmig. Tu transformes des maquettes UI (code statique dans un repo Git) en applications de production avec Supabase.

## Commande reçue

L'utilisateur a exécuté: `/mockmig $ARGUMENTS`

## Instructions par phase

Lis le fichier de phase correspondant et exécute les instructions:

| Argument | Fichier à lire | Description |
|----------|----------------|-------------|
| `init` | `.claude/skills/mockmig/phases/init.md` | Preflight MCPs + Bootstrap sources de vérité |
| `discover` | `.claude/skills/mockmig/phases/discover.md` | Phase 1: Inventaire règles métier |
| `analyze` | `.claude/skills/mockmig/phases/analyze.md` | Phase 2: Audit DB + Gap analysis |
| `plan` | `.claude/skills/mockmig/phases/plan.md` | Phase 3: Tâches backend/UI + Runbook |
| `execute` | `.claude/skills/mockmig/phases/execute.md` | Phase 4: Implémentation |
| `status` | `.claude/skills/mockmig/phases/status.md` | Vue d'ensemble session |
| (vide) | - | Afficher l'aide ci-dessous |

## Si aucun argument ou argument invalide

Affiche:

```
📦 MOCKMIG - Migration de Maquettes
===================================

Workflow de transformation de maquettes Git vers production Supabase.

Usage:
  /mockmig <phase> [options]

Phases:
  init                 Initialiser la migration (preflight + bootstrap)
  discover             Phase 1: Extraire les règles métier
  analyze              Phase 2: Auditer la DB et identifier les gaps
  plan                 Phase 3: Générer les tâches et le runbook
  execute [--confirm]  Phase 4: Implémenter les tâches
  status [--verbose]   Afficher l'état de la migration

Exemples:
  /mockmig init --module devis --mockupPath modules/maquette/devis/v1
  /mockmig discover
  /mockmig status --verbose
  /mockmig execute --confirm

Documentation:
  Voir .claude/MOCKMIG_ANALYSIS.md pour le détail du workflow.
```

## Contexte à charger

Avant d'exécuter une phase, charge toujours:

1. **CLAUDE.md** - Contexte projet (`.claude/CLAUDE.md`)
2. **Session** - État actuel si existe (`.mockmig/session.json`)
3. **Sources de vérité** - Si elles existent:
   - `memory/constitution.md`
   - `ontologie/01_ontologie.md` + `02_ontologie.yaml`
   - `ARCHITECTURE_DE_SECURITÉ.md`

## MCPs requis

Vérifie la disponibilité des MCPs avant les phases qui les utilisent:

| MCP | Requis pour |
|-----|-------------|
| Supabase | analyze, execute |
| GitHub | execute (optionnel) |
| Netlify | execute (optionnel) |

## Sortie

- Toujours afficher la progression clairement avec des émojis
- Utiliser des blocs de code pour le SQL et les commandes
- Créer les fichiers dans les bons répertoires:
  - Artefacts → `migration/<module>/`
  - Sources de vérité → `memory/`, `ontologie/`, racine
  - Session → `.mockmig/session.json`
