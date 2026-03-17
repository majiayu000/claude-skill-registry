---
name: react-clean-ui
description: Keep React UI components clean; move logic into hooks and services
compatibility: opencode
license: MIT
metadata:
  stack: node-react-next
  style: solid-clean-code
---
## What I do

Je fournis des règles pour garder des composants React **propres** :
- UI minimaliste (présentation)
- Logique dans hooks
- Données via TanStack Query

## UI rules
- Aucun appel réseau dans un composant UI.
- Aucun mapping DTO complexe dans JSX.
- Pas de state global implicite : state local ou query cache.

## Hook rules
- Un hook retourne un **view-model** prêt.
- Le hook parle aux services via DI.
- Les side-effects UI (toast, navigation) restent dans hooks/pages.

## Example pattern

```tsx
export function UserPage({ id }: { id: string }) {
  const vm = useUserDetails(id);
  return <UserDetailsView {...vm} />;
}
```
