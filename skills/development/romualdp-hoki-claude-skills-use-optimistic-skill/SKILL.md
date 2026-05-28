---
name: useOptimistic Hook Generator
description: Implémente useOptimistic pour instant UI updates avec VRAIE gestion du rollback. MANDATORY pour delete operations. À utiliser lors de mutations, deletes, ou quand l'utilisateur mentionne "optimistic", "instant update", "delete", "mutation".
allowed-tools: [Read, Write, Edit]
---

# useOptimistic Hook Generator

## 🎯 Mission

Implémenter **useOptimistic** pour des **mises à jour instantanées** de l'UI avec **gestion correcte du rollback** en cas d'erreur.

## ⚡ Concept

**useOptimistic** met à jour l'UI **immédiatement** (optimistic), puis :
- ✅ Si succès : State synchronisé via props ou re-fetch
- ❌ Si erreur : **ROLLBACK MANUEL REQUIS** (pas automatique !)

## 🚨 ATTENTION : Rollback Manuel

**ERREUR COURANTE** :
```typescript
// ❌ FAUX - useOptimistic ne rollback PAS automatiquement
const handleRemove = async (memberId: string) => {
  removeOptimisticMember(memberId);
  const result = await removeMemberAction(memberId);
  // Si erreur, l'UI reste dans l'état optimiste (membre supprimé)
  // = BUG !
};
```

**useOptimistic** ne gère PAS les erreurs automatiquement. Il faut **gérer le rollback manuellement**.

## ✅ Solution Recommandée : Server Component + revalidatePath

### Template Complet

```typescript
// ==========================================
// 1. Server Component (Page)
// ==========================================
// app/clubs/[id]/members/page.tsx

export default async function MembersPage({ params }: { params: { id: string } }) {
  // Fetch data server-side
  const members = await fetchMembers(params.id);

  return (
    <div>
      <h1>Membres</h1>
      <MembersList clubId={params.id} initialMembers={members} />
    </div>
  );
}

// ==========================================
// 2. Client Component avec useOptimistic
// ==========================================
// components/MembersList.tsx
'use client';

import { useOptimistic } from 'react';
import { removeMemberAction } from '../actions/remove-member.action';
import { toast } from 'sonner';

interface Member {
  id: string;
  name: string;
  email: string;
}

interface MembersListProps {
  clubId: string;
  initialMembers: Member[];
}

export function MembersList({ clubId, initialMembers }: MembersListProps) {
  // useOptimistic hook
  const [optimisticMembers, removeOptimisticMember] = useOptimistic(
    initialMembers,
    (state, removedId: string) => state.filter(m => m.id !== removedId)
  );

  const handleRemove = async (memberId: string) => {
    // 1. Update UI instantly (optimistic)
    removeOptimisticMember(memberId);

    // 2. Call server action
    const result = await removeMemberAction(clubId, memberId);

    if (result.success) {
      // Success: revalidatePath() in action will trigger Server Component re-fetch
      // → initialMembers updated → optimisticMembers synced automatically
      toast.success('Membre retiré avec succès');
    } else {
      // Error: revalidatePath() still called in action
      // → Server Component re-fetches → initialMembers restored → ROLLBACK AUTO
      toast.error(result.error.message);
    }
  };

  return (
    <ul className="space-y-2">
      {optimisticMembers.length === 0 ? (
        <p className="text-muted-foreground">Aucun membre</p>
      ) : (
        optimisticMembers.map(member => (
          <MemberCard
            key={member.id}
            member={member}
            onRemove={() => handleRemove(member.id)}
          />
        ))
      )}
    </ul>
  );
}

// ==========================================
// 3. Server Action avec revalidatePath
// ==========================================
// actions/remove-member.action.ts
'use server';

import { revalidatePath } from 'next/cache';
import { membersApi } from '../api/members.api';

export async function removeMemberAction(clubId: string, memberId: string) {
  try {
    // Call backend API
    await membersApi.remove(clubId, memberId);

    // CRITICAL: Revalidate to trigger Server Component re-fetch
    // This works for BOTH success AND error cases
    revalidatePath(`/clubs/${clubId}/members`);

    return { success: true };
  } catch (error) {
    // Even on error, revalidate to restore correct state
    revalidatePath(`/clubs/${clubId}/members`);

    return {
      success: false,
      error: {
        code: 'REMOVE_ERROR',
        message: 'Impossible de retirer le membre',
      },
    };
  }
}
```

**Pourquoi ça fonctionne** :
1. Optimistic update → UI se met à jour immédiatement
2. Server Action exécute → Succès OU erreur
3. `revalidatePath()` appelé dans TOUS les cas → Server Component re-fetch
4. `initialMembers` mis à jour → `optimisticMembers` synchronisé automatiquement
5. **Si erreur** : Le re-fetch restaure l'état correct = **Rollback automatique**

## 🔄 Alternative : Rollback Manuel avec State

Si vous **ne pouvez pas** utiliser Server Components :

```typescript
'use client';

import { useState } from 'react';
import { removeMemberAction } from '../actions/remove-member.action';

export function MembersList({ initialMembers }: Props) {
  const [members, setMembers] = useState(initialMembers);
  const [pendingRemoveIds, setPendingRemoveIds] = useState<string[]>([]);

  // Filter out pending removals (optimistic)
  const displayedMembers = members.filter(m => !pendingRemoveIds.includes(m.id));

  const handleRemove = async (memberId: string) => {
    // 1. Add to pending (optimistic update)
    setPendingRemoveIds(prev => [...prev, memberId]);

    // 2. Call server action
    const result = await removeMemberAction(memberId);

    if (result.success) {
      // Success: Remove from actual state
      setMembers(prev => prev.filter(m => m.id !== memberId));
      setPendingRemoveIds(prev => prev.filter(id => id !== memberId));
      toast.success('Membre retiré');
    } else {
      // Error: ROLLBACK manually
      setPendingRemoveIds(prev => prev.filter(id => id !== memberId));
      toast.error(result.error.message);
    }
  };

  return (
    <ul>
      {displayedMembers.map(member => (
        <MemberCard key={member.id} member={member} onRemove={() => handleRemove(member.id)} />
      ))}
    </ul>
  );
}
```

## 🎨 Autres Patterns

### Add Operation

```typescript
// Server Component + useOptimistic (Recommended)
export function ItemsList({ initialItems }: Props) {
  const [optimisticItems, addOptimisticItem] = useOptimistic(
    initialItems,
    (state, newItem: Item) => [...state, newItem]
  );

  const handleAdd = async (item: Item) => {
    // Optimistic
    addOptimisticItem(item);

    // Server action (with revalidatePath)
    const result = await addItemAction(item);

    if (result.success) {
      toast.success('Ajouté');
      // revalidatePath() in action → Server Component re-fetch → Sync auto
    } else {
      toast.error(result.error.message);
      // revalidatePath() in action → Server Component re-fetch → Rollback auto
    }
  };

  return <div>...</div>;
}
```

### Update Operation

```typescript
export function ItemsList({ initialItems }: Props) {
  const [optimisticItems, updateOptimisticItem] = useOptimistic(
    initialItems,
    (state, updated: Item) => state.map(i => i.id === updated.id ? updated : i)
  );

  const handleUpdate = async (item: Item) => {
    // Optimistic
    updateOptimisticItem(item);

    // Server action (with revalidatePath)
    const result = await updateItemAction(item);

    if (result.success) {
      toast.success('Modifié');
    } else {
      toast.error(result.error.message);
    }
  };

  return <div>...</div>;
}
```

### Toggle Operation

```typescript
export function ToggleComponent({ initialItem }: Props) {
  const [optimisticItem, toggleOptimistic] = useOptimistic(
    initialItem,
    (state) => ({ ...state, active: !state.active })
  );

  const handleToggle = async () => {
    // Optimistic
    toggleOptimistic();

    // Server action (with revalidatePath)
    const result = await toggleItemAction(optimisticItem.id);

    if (!result.success) {
      toast.error(result.error.message);
      // revalidatePath() in action → Rollback auto
    }
  };

  return (
    <button onClick={handleToggle}>
      {optimisticItem.active ? 'Active' : 'Inactive'}
    </button>
  );
}
```

## 🔍 Exemple Complet avec Multiple Operations

```typescript
// components/MembersList.tsx
'use client';

import { useOptimistic } from 'react';
import { removeMemberAction, updateMemberRoleAction } from '../actions';

export function MembersList({ clubId, initialMembers }: Props) {
  const [optimisticMembers, updateOptimisticMembers] = useOptimistic(
    initialMembers,
    (state, action: { type: 'remove' | 'updateRole'; id: string; role?: string }) => {
      switch (action.type) {
        case 'remove':
          return state.filter(m => m.id !== action.id);
        case 'updateRole':
          return state.map(m => m.id === action.id ? { ...m, role: action.role! } : m);
        default:
          return state;
      }
    }
  );

  const handleRemove = async (memberId: string) => {
    updateOptimisticMembers({ type: 'remove', id: memberId });

    const result = await removeMemberAction(clubId, memberId);

    if (result.success) {
      toast.success('Membre retiré');
    } else {
      toast.error(result.error.message);
    }
    // revalidatePath() in action handles sync/rollback
  };

  const handleUpdateRole = async (memberId: string, newRole: string) => {
    updateOptimisticMembers({ type: 'updateRole', id: memberId, role: newRole });

    const result = await updateMemberRoleAction(clubId, memberId, newRole);

    if (result.success) {
      toast.success('Rôle modifié');
    } else {
      toast.error(result.error.message);
    }
    // revalidatePath() in action handles sync/rollback
  };

  return (
    <ul>
      {optimisticMembers.map(member => (
        <MemberCard
          key={member.id}
          member={member}
          onRemove={() => handleRemove(member.id)}
          onUpdateRole={(role) => handleUpdateRole(member.id, role)}
        />
      ))}
    </ul>
  );
}
```

## ✅ Checklist useOptimistic

- [ ] `useOptimistic` pour operations importantes (delete, update, toggle)
- [ ] **Server Component** fournit `initialData` (Recommended)
- [ ] Optimistic update AVANT server action call
- [ ] Server Action appelle `revalidatePath()` dans **TOUS les cas** (succès ET erreur)
- [ ] Toast pour feedback utilisateur (succès/erreur)
- [ ] **Pas de rollback manuel** si Server Component + revalidatePath
- [ ] Si pas Server Component : Rollback manuel avec state

## 🚨 Erreurs Courantes

### 1. Oublier revalidatePath

```typescript
// ❌ MAUVAIS - Pas de revalidatePath = Pas de sync/rollback
export async function removeMemberAction(id: string) {
  await api.remove(id);
  return { success: true };
  // UI reste dans l'état optimiste, même si erreur backend !
}

// ✅ BON - revalidatePath dans TOUS les cas
export async function removeMemberAction(id: string) {
  try {
    await api.remove(id);
    revalidatePath('/members'); // Success: sync
    return { success: true };
  } catch (error) {
    revalidatePath('/members'); // Error: rollback
    return { success: false, error: { message: 'Erreur' } };
  }
}
```

### 2. revalidatePath uniquement si succès

```typescript
// ❌ MAUVAIS - Rollback ne se fait pas
export async function removeMemberAction(id: string) {
  try {
    await api.remove(id);
    revalidatePath('/members'); // Only on success
    return { success: true };
  } catch (error) {
    // No revalidatePath = No rollback !
    return { success: false, error };
  }
}

// ✅ BON - revalidatePath dans les DEUX cas
export async function removeMemberAction(id: string) {
  try {
    await api.remove(id);
    revalidatePath('/members');
    return { success: true };
  } catch (error) {
    revalidatePath('/members'); // CRITICAL for rollback
    return { success: false, error };
  }
}
```

### 3. Utiliser useOptimistic sans Server Component

```typescript
// ❌ MAUVAIS - useOptimistic avec state local = compliqué
const [members, setMembers] = useState(initialMembers);
const [optimistic, setOptimistic] = useOptimistic(members, ...);
// Rollback manuel requis, complexe à gérer

// ✅ BON - useOptimistic avec Server Component
export default async function Page() {
  const members = await fetchMembers(); // Server-side
  return <MembersList initialMembers={members} />;
}

function MembersList({ initialMembers }) {
  const [optimistic, update] = useOptimistic(initialMembers, ...);
  // Rollback automatique via revalidatePath
}
```

## 📚 Skills Complémentaires

- **server-actions** : Server Actions avec revalidatePath
- **suspense-streaming** : Loading states pendant operations
- **atomic-component** : Composants utilisant useOptimistic

---

**Rappel CRITIQUE** : `useOptimistic` ne rollback PAS automatiquement. Utilisez **Server Component + revalidatePath** pour rollback automatique, ou gérez manuellement avec state.
