---
name: react-compound-components
description: React compound components pattern (safe, minimal context, ergonomic API)
compatibility: opencode
license: MIT
metadata:
  stack: node-react-next
  style: solid-clean-code
---
## What I do

Je fournis un guide pour implémenter des **Compound Components** sûrs :
- contexte minimal
- API ergonomique
- erreurs explicites

## Minimal template

```tsx
type Ctx = { id: string };
const Ctx = createContext<Ctx | null>(null);

export function Root({ id, children }: { id: string; children: ReactNode }) {
  return <Ctx.Provider value={{ id }}>{children}</Ctx.Provider>;
}

Root.Label = function Label({ children }: { children: ReactNode }) {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error('Root.Label must be used within Root');
  return <label htmlFor={ctx.id}>{children}</label>;
};
```

## Example

```tsx
// ui/form/FormField.tsx
import React, { createContext, useContext } from "react";

type Ctx = { id: string };
const FieldCtx = createContext<Ctx | null>(null);

export function FormField({ id, children }: { id: string; children: React.ReactNode }) {
  return <FieldCtx.Provider value={{ id }}>{children}</FieldCtx.Provider>;
}

FormField.Label = function Label({ children }: { children: React.ReactNode }) {
  const ctx = useContext(FieldCtx);
  if (!ctx) throw new Error("FormField.Label must be used within FormField");
  return <label htmlFor={ctx.id} className="text-sm font-medium">{children}</label>;
};

FormField.Input = function Input(props: React.InputHTMLAttributes<HTMLInputElement>) {
  const ctx = useContext(FieldCtx);
  if (!ctx) throw new Error("FormField.Input must be used within FormField");
  return <input id={ctx.id} {...props} className="w-full rounded-md border p-2" />;
};
```

Utilisation :

```tsx
<FormField id="email">
  <FormField.Label>Email</FormField.Label>
  <FormField.Input type="email" />
</FormField>
```

## When NOT to use
- Si l'état partagé devient complexe : passer à props explicites + hook.
