---
name: gate-check
description: "Vérifie un gate spécifique (0-5)"
context: fork
allowed-tools: Read, Glob, Bash
argument-hint: "[gate-number]"
---

# Gate Check

Vérifie le gate spécifié en argument.

## Usage
`/gate-check 0` → Vérifie Gate 0 (requirements.md)
`/gate-check 1` → Vérifie Gate 1 (BREAK → MODEL)
`/gate-check 2` → Vérifie Gate 2 (MODEL → ACT)
`/gate-check 3` → Vérifie Gate 3 (Planning → Build)
`/gate-check 4` → Vérifie Gate 4 (Build → QA)
`/gate-check 5` → Vérifie Gate 5 (QA → Release)

## Exécution
```bash
node tools/gate-check.js $ARGUMENTS
```

## Retour
- ✅ PASS : gate validé
- ❌ FAIL : liste des fichiers/sections manquants
