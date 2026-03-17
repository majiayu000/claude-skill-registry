---
name: Parallel Routes Generator
description: Implémente les Parallel Routes Next.js pour modals sans layout shifts. MANDATORY pour modals. À utiliser lors de modals, dialogs, ou quand l'utilisateur mentionne "modal", "dialog", "parallel route", "intercepted route".
allowed-tools: [Read, Write, Edit, Bash]
---

# Parallel Routes Generator

## 🎯 Mission

Implémenter des **modals** avec **Parallel Routes** Next.js pour éviter les layout shifts et améliorer l'UX.

## 🏗️ Structure

```
app/(dashboard)/
├── @modal/
│   ├── (..)upgrade/
│   │   └── page.tsx          # Modal interceptée
│   ├── (..)confirm-delete/
│   │   └── page.tsx
│   └── default.tsx            # Returns null
├── layout.tsx                 # Accepte {children, modal}
└── page.tsx
```

### Layout avec Modal Slot

```typescript
// app/(dashboard)/layout.tsx

export default function DashboardLayout({
  children,
  modal,
}: {
  children: React.ReactNode;
  modal: React.ReactNode;
}) {
  return (
    <>
      {children}
      {modal}
    </>
  );
}
```

### Default Modal

```typescript
// app/(dashboard)/@modal/default.tsx

export default function Default() {
  return null;
}
```

### Modal Intercepté

```typescript
// app/(dashboard)/@modal/(..)upgrade/page.tsx

import { Modal } from '@/components/ui/modal';
import { UpgradeForm } from '@/features/subscription/components/UpgradeForm';

export default function UpgradeModal() {
  return (
    <Modal>
      <UpgradeForm />
    </Modal>
  );
}
```

### Modal Component

```typescript
'use client';

import { useRouter } from 'next/navigation';
import { Dialog, DialogContent } from '@/components/ui/dialog';

export function Modal({ children }: { children: React.ReactNode }) {
  const router = useRouter();

  return (
    <Dialog open onOpenChange={() => router.back()}>
      <DialogContent>
        {children}
      </DialogContent>
    </Dialog>
  );
}
```

### Usage

```typescript
// Link ouvre le modal
<Link href="/upgrade">Upgrade</Link>

// URL directe charge la page complète
// URL via navigation charge le modal
```

## ✅ Checklist

- [ ] Slot `@modal` créé
- [ ] `default.tsx` retourne null
- [ ] Route interceptée avec `(..)`
- [ ] Modal composant avec close handler
- [ ] Layout accepte `{modal}` slot

---

**Rappel**: Parallel Routes = Better UX que modals traditionnels.
