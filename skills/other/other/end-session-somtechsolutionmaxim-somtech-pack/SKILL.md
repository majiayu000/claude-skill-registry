---
name: end-session
description: |
  Skill de fin de session Claude Code pour documenter automatiquement le travail accompli.
  DÉCLENCHEURS: /end-session, fin de session, clôturer session, terminer session, sync docs
  Met à jour CLAUDE.md (mémoire projet) et CHANGELOG.md avec:
  - Décisions techniques prises pendant la session
  - Problèmes résolus et solutions appliquées
  - Contexte important pour les futures sessions
  - Fichiers créés ou modifiés
---

# End Session - Documentation Automatique

Ce skill analyse la session Claude Code en cours et met à jour la documentation du projet.

## Workflow

### 1. Analyser la session

Parcourir l'historique de la conversation pour identifier:

- **Décisions techniques**: choix d'architecture, patterns utilisés, compromis faits
- **Problèmes résolus**: bugs fixés, défis surmontés, solutions trouvées
- **Fichiers modifiés**: liste des fichiers créés/modifiés avec résumé des changements
- **Contexte important**: informations utiles pour les futures sessions

### 2. Mettre à jour CLAUDE.md

CLAUDE.md est le fichier de mémoire projet. Ajouter ou mettre à jour les sections:

```markdown
## Décisions Techniques
<!-- Choix d'architecture et leurs justifications -->

## Patterns Utilisés
<!-- Patterns de code, conventions adoptées -->

## Notes de Session [DATE]
<!-- Contexte spécifique à cette session -->
```

**Règles importantes:**
- Ne pas dupliquer l'information existante
- Fusionner avec le contenu existant si pertinent
- Garder le fichier concis et organisé
- Utiliser des bullet points pour la lisibilité

### 3. Mettre à jour CHANGELOG.md

Format standard pour les entrées:

```markdown
## [Non-versionné] - YYYY-MM-DD

### Ajouté
- Nouvelles fonctionnalités

### Modifié
- Changements aux fonctionnalités existantes

### Corrigé
- Bugs résolus

### Technique
- Décisions techniques, refactoring, dette technique
```

**Règles:**
- Créer le fichier s'il n'existe pas
- Ajouter une nouvelle section datée en haut
- Catégoriser les changements (Ajouté/Modifié/Corrigé/Technique)
- Être spécifique mais concis

### 4. Résumé de fin de session

Afficher un résumé à l'utilisateur:

```
📋 Session terminée - Documentation mise à jour

📝 CLAUDE.md:
   - X décisions techniques ajoutées
   - X notes de contexte ajoutées

📜 CHANGELOG.md:
   - X entrées ajoutées pour [DATE]

🔍 Résumé des changements:
   - [Liste des points clés]
```

## Exemple d'utilisation

Utilisateur tape `/end-session` à la fin d'une session de travail.

Claude:
1. Analyse la conversation
2. Identifie les éléments à documenter
3. Met à jour CLAUDE.md et CHANGELOG.md à la racine du projet
4. Affiche le résumé

## Notes

- Si CLAUDE.md n'existe pas, le créer avec une structure de base
- Si CHANGELOG.md n'existe pas, le créer avec le format Keep a Changelog
- Toujours demander confirmation avant d'écrire si des changements majeurs sont détectés
- Adapter le niveau de détail selon l'ampleur de la session
