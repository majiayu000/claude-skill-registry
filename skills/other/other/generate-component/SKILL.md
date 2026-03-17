---
name: generate-component
description: Generate a new component with test file following project conventions
disable-model-invocation: true
user-invocable: true
allowed-tools: Read, Write, Bash
argument-hint: "[component-name]"
---

Genereer een nieuw component `$ARGUMENTS`:

1. **Maak het bronbestand**: `src/$ARGUMENTS.js` met een duidelijke, geexporteerde module
2. **Maak het testbestand**: `tests/$ARGUMENTS.test.js` met minimaal:
   - Een test dat het component correct initialiseert
   - Een test voor de belangrijkste functionaliteit
   - Een edge case test
3. **Valideer**: Run `npm test` om te bevestigen dat de tests slagen
4. **Lint**: Run `npm run lint` om code style te checken

Volg de conventies uit @CLAUDE.md en @.claude/rules/code-style.md.
