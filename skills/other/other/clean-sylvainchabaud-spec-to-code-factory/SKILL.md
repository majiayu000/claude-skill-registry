---
name: clean
description: "Reset complet du projet - remet en état starter"
allowed-tools: Bash, AskUserQuestion
---

# /clean - Reset complet du projet

Remet le projet en état "starter" propre via `tools/clean.js`.

## Workflow

1. **Demander confirmation** via AskUserQuestion :
   - Question : "Remettre le projet en état starter ? Tous les artefacts seront supprimés."
   - Options : "Oui, nettoyer" / "Non, annuler"
   - Si "Non" → STOP

2. **Exécuter le script** via Bash :
   ```bash
   node tools/clean.js --force
   ```
   > `--force` car la confirmation est déjà faite à l'étape 1.

3. **Confirmer** le résultat affiché par le script.

## Mode --force

Si l'argument contient "--force", skip la confirmation (étape 1) et exécute directement :
```bash
node tools/clean.js --force
```

## Mode --dry-run

Si l'argument contient "--dry-run", afficher ce qui serait supprimé sans rien toucher :
```bash
node tools/clean.js --dry-run
```
