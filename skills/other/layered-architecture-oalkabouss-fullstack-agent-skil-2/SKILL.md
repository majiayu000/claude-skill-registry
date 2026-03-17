---
name: layered-architecture
description: Apply layered architecture (Clean Architecture) across backend and frontend
compatibility: opencode
license: MIT
metadata:
  stack: node-react-next
  style: solid-clean-code
---
## What I do\n\nJe fournis un cadre pratique pour appliquer une **architecture en couches** (Clean Architecture / Ports & Adapters) sur Node.js + Next.js.\n\n## Non‑negotiables\n- Domain pur (pas d'I/O, pas de libs).\n- Use-cases/Hooks dépendent de ports (interfaces).\n- Implémentations en infrastructure/services.\n- Un composition root instancie toutes les concrétions.\n\n## Backend layering (recipe)\n1. Controller : parse + validate (Zod) + call use-case\n2. Use-case : orchestration + appels aux ports\n3. Domain : invariants, règles, services purs\n4. Infra : DB/HTTP/cache\n\n## Frontend layering (recipe)\n1. UI : rendu + événements simples\n2. Hooks : Query + mapping + side effects UI\n3. Services : HTTP + errors + DTO mapping\n\n## Quick anti-pattern detector\n- Vous importez / dans un hook : mauvais (passer par service).\n- Vous importez Prisma dans un use-case : mauvais (passer par repository).\n- Vous mappez un DTO dans JSX : mauvais (mapper dans hook/service).\n
