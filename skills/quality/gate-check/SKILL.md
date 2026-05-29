---
name: gate-check
description: "Vérifie un gate spécifique (1-5)"
context: fork
allowed-tools: Read, Glob, Bash
argument-hint: "[gate-number]"
---

# Gate Check

Vérifie le gate spécifié en argument.

## Usage
`/gate-check 1` → Vérifie Gate 1
`/gate-check 2` → Vérifie Gate 2
...

## Exécution
```bash
node tools/gate-check.js $ARGUMENTS
```

## Retour
- ✅ PASS : gate validé
- ❌ FAIL : liste des fichiers/sections manquants
