---
name: tanstack-query-standards
description: TanStack Query standards (keys, caching, invalidation, error handling)
compatibility: opencode
license: MIT
metadata:
  stack: node-react-next
  style: solid-clean-code
---
## What I do

Je standardise l'usage de **TanStack Query** (React Query) :
- query keys centralisées
- invalidations précises
- gestion des erreurs

## Rules
- `queryKey` via une factory `qk.*`.
- `queryFn` appelle un service injecté.
- Mutations invalident les clés impactées uniquement.

## Default guidance (adjust per feature)
- `retry`: 0 ou 1 si l'erreur est probablement transitoire.
- `staleTime`: 0 pour données très fraîches, sinon 30s-5m.

## Anti-patterns
- `invalidateQueries()` global sans predicate.
- Mélanger logique d'UI (formatage) dans `queryFn`.
