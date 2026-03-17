---
name: fix-issue
description: Fix a GitHub issue by analyzing, implementing, testing and creating a PR
disable-model-invocation: true
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
argument-hint: "[issue-number]"
---

Fix GitHub issue #$ARGUMENTS:

1. **Analyseer het issue**: Gebruik `gh issue view $ARGUMENTS` om de details op te halen
2. **Zoek relevante code**: Doorzoek de codebase voor gerelateerde bestanden
3. **Implementeer de fix**: Maak de benodigde wijzigingen
4. **Schrijf tests**: Voeg tests toe die de fix valideren
5. **Valideer**: Run `npm test` en `npm run lint`
6. **Commit**: Maak een descriptieve commit met `fix: <beschrijving> (closes #$ARGUMENTS)`
7. **Push**: Push naar de huidige branch
