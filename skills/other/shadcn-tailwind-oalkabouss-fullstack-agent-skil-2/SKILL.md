---
name: shadcn-tailwind
description: Shadcn UI + Tailwind conventions (variants, reuse, dumb components)
compatibility: opencode
license: MIT
metadata:
  stack: node-react-next
  style: solid-clean-code
---
## What I do

Je fournis des conventions pour Shadcn UI + Tailwind :
- composants réutilisables
- variants via cva
- classes Tailwind non dupliquées

## Rules
- Créer des composants de base (`Button`, `PageHeader`, `DataTable`).
- Les composants UI restent "dumb" (props + slots).
- Centraliser `cn` et `cva`.
