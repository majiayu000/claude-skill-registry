---
name: code-review
description: Review code for quality, security and best practices
disable-model-invocation: true
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
argument-hint: "[file-or-directory]"
---

Review de code in `$ARGUMENTS`:

1. **Lees de code** en begrijp de functionaliteit
2. **Controleer op**:
   - Code clarity en leesbaarheid
   - Naamgeving van functies en variabelen
   - Gedupliceerde code
   - Foutafhandeling
   - Security issues (OWASP top 10)
   - Input validatie
   - Test coverage
   - Performance
3. **Run de linter**: `npm run lint`
4. **Run de tests**: `npm test`
5. **Rapporteer** bevindingen gegroepeerd op prioriteit:
   - **Kritiek**: Moet gefixt worden
   - **Waarschuwingen**: Zou gefixt moeten worden
   - **Suggesties**: Nice to have verbeteringen
