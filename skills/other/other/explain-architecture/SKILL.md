---
name: explain-architecture
description: Explain the system architecture or a specific part of the codebase
disable-model-invocation: true
user-invocable: true
allowed-tools: Read, Grep, Glob
argument-hint: "[onderdeel]"
---

Leg de architectuur uit van `$ARGUMENTS`:

1. **Overzicht**: Begin met een korte samenvatting in 1-2 zinnen
2. **Diagram**: Teken een ASCII-diagram dat de structuur en dataflow toont
3. **Componenten**: Beschrijf elk component en zijn verantwoordelijkheid
4. **Relaties**: Leg uit hoe componenten met elkaar communiceren
5. **Domeincontext**: Relateer aan korfbal-domeinconcepten waar relevant (zie @docs/KORFBAL-DOMEIN.md)

Communiceer in het Nederlands. Houd het begrijpelijk voor iemand die de codebase nog niet kent.
