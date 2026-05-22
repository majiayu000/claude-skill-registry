---
name: Server Actions Generator
description: Génère des Next.js Server Actions comme couche d'orchestration mince entre frontend et backend NestJS. À utiliser lors de la création d'actions, mutations, ou quand l'utilisateur mentionne "server action", "mutation", "form action", "useTransition", "revalidatePath".
allowed-tools: [Read, Write, Edit, Glob, Grep]
---

# Server Actions Generator

## 🎯 Mission

Créer des **Server Actions Next.js** comme **couche d'orchestration mince** entre le frontend et le backend NestJS, avec gestion du cache et des erreurs.

## 🏗️ Philosophie Server Actions

### Qu'est-ce qu'une Server Action ?

Une **Server Action** est une fonction serveur Next.js (`'use server'`) qui :
- ✅ Exécute côté serveur (Next.js server, pas client)
- ✅ Peut être appelée directement depuis un composant client
- ✅ Simplifie les mutations (pas besoin d'API route)
- ✅ Intègre avec les forms HTML natifs

### Architecture Flow

```
Component (Client)
  ↓ useTransition() ou form action
Server Action (Next.js Server) [THIN LAYER]
  ↓ Validation Zod
  ↓ fetch/axios
Backend NestJS API
  ↓ Command Handler (CQRS)
  ↓ Domain Entity
  ↓ Repository
Database (Prisma)
```

### Responsabilités d'une Server Action

**✅ CE QU'ELLE FAIT** :
1. Valider les inputs (Zod)
2. Appeler l'API backend NestJS
3. Gérer le cache Next.js (`revalidatePath`, `revalidateTag`)
4. Formatter les erreurs pour l'UI
5. Retourner un résultat typé

**❌ CE QU'ELLE NE FAIT PAS** :
- ❌ **JAMAIS** de logique métier (dans le backend)
- ❌ **JAMAIS** d'accès direct à la DB (utiliser backend)
- ❌ **JAMAIS** dupliquer la validation backend

## 📝 Template Server Action

### Structure de Fichier

```
features/
└── club-management/
    └── actions/
        ├── create-club.action.ts
        ├── update-club.action.ts
        ├── delete-club.action.ts
        ├── subscribe-to-plan.action.ts
        └── index.ts                  # Barrel export
```

### Template Complet

```typescript
// features/club-management/actions/create-club.action.ts
'use server';

import { revalidatePath } from 'next/cache';
import { z } from 'zod';
import { clubsApi } from '../api/clubs.api';

// 1. Schema de validation (synchronisé avec backend DTO)
const createClubSchema = z.object({
  name: z
    .string()
    .min(3, 'Le nom doit contenir au moins 3 caractères')
    .max(100, 'Le nom ne peut pas dépasser 100 caractères'),
  description: z
    .string()
    .max(500, 'La description ne peut pas dépasser 500 caractères')
    .optional(),
});

// 2. Type d'input (inféré depuis schema)
export type CreateClubInput = z.infer<typeof createClubSchema>;

// 3. Type de résultat
export type CreateClubResult =
  | { success: true; data: { id: string } }
  | { success: false; error: { code: string; message: string; details?: any } };

// 4. Server Action
export async function createClubAction(input: CreateClubInput): Promise<CreateClubResult> {
  try {
    // Validate input
    const validated = createClubSchema.parse(input);

    // Call backend API
    const response = await clubsApi.create(validated);

    // Revalidate cache
    revalidatePath('/dashboard/coach');
    revalidatePath('/clubs');

    // Return success
    return {
      success: true,
      data: response,
    };
  } catch (error) {
    // Handle validation errors
    if (error instanceof z.ZodError) {
      return {
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Les données fournies sont invalides',
          details: error.errors,
        },
      };
    }

    // Handle API errors
    if (error instanceof ApiError) {
      return {
        success: false,
        error: {
          code: error.code,
          message: error.getUserMessage(),
        },
      };
    }

    // Handle unknown errors
    return {
      success: false,
      error: {
        code: 'UNKNOWN_ERROR',
        message: 'Une erreur est survenue. Veuillez réessayer.',
      },
    };
  }
}
```

## 🔄 Cache Management

### revalidatePath

Invalide le cache pour un chemin spécifique.

```typescript
'use server';

export async function createClubAction(input: CreateClubInput) {
  const response = await clubsApi.create(input);

  // Revalidate specific paths
  revalidatePath('/dashboard/coach'); // Coach dashboard
  revalidatePath('/clubs'); // Clubs list page
  revalidatePath(`/clubs/${response.id}`); // Club detail page

  return { success: true, data: response };
}
```

**Quand utiliser** :
- ✅ Après création/modification/suppression de données
- ✅ Pour forcer le re-fetch des Server Components
- ✅ Pour mettre à jour l'UI après mutation

### revalidateTag

Invalide le cache par tag (plus flexible).

```typescript
'use server';

export async function createClubAction(input: CreateClubInput) {
  const response = await clubsApi.create(input);

  // Revalidate by tags
  revalidateTag('clubs'); // All clubs-related data
  revalidateTag(`club-${response.id}`); // Specific club

  return { success: true, data: response };
}

// Dans Server Component ou API route
fetch('/api/clubs', {
  next: { tags: ['clubs'] }
});

fetch(`/api/clubs/${id}`, {
  next: { tags: [`club-${id}`, 'clubs'] }
});
```

**Quand utiliser** :
- ✅ Gestion fine du cache
- ✅ Invalidation groupée (ex: tous les "clubs")
- ✅ Avec `fetch` et Next.js cache

## 🎨 Intégration avec Composants

### Avec useTransition (Recommended)

```typescript
// components/ClubCreationForm.tsx
'use client';

import { useTransition } from 'react';
import { useRouter } from 'next/navigation';
import { createClubAction, CreateClubInput } from '../actions/create-club.action';
import { toast } from 'sonner';

export function ClubCreationForm() {
  const router = useRouter();
  const [isPending, startTransition] = useTransition();
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (formData: FormData) => {
    setError(null);

    const input: CreateClubInput = {
      name: formData.get('name') as string,
      description: formData.get('description') as string,
    };

    startTransition(async () => {
      const result = await createClubAction(input);

      if (result.success) {
        toast.success('Club créé avec succès !');
        router.push(`/clubs/${result.data.id}`);
      } else {
        setError(result.error.message);
        toast.error(result.error.message);
      }
    });
  };

  return (
    <form action={handleSubmit} className="space-y-4">
      <input name="name" placeholder="Nom du club" required />
      <textarea name="description" placeholder="Description" />

      {error && (
        <div className="text-red-500 text-sm">{error}</div>
      )}

      <button
        type="submit"
        disabled={isPending}
        className="btn btn-primary"
      >
        {isPending ? 'Création...' : 'Créer le club'}
      </button>
    </form>
  );
}
```

### Avec Form Action (HTML Native)

```typescript
// components/QuickClubForm.tsx
'use client';

import { useFormStatus } from 'react-dom';
import { createClubAction } from '../actions/create-club.action';

export function QuickClubForm() {
  return (
    <form action={createClubAction}>
      <input name="name" placeholder="Nom du club" required />
      <SubmitButton />
    </form>
  );
}

function SubmitButton() {
  const { pending } = useFormStatus();

  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Création...' : 'Créer'}
    </button>
  );
}
```

### Avec useActionState (React 19)

```typescript
'use client';

import { useActionState } from 'react';
import { createClubAction } from '../actions/create-club.action';

export function ClubForm() {
  const [state, formAction, isPending] = useActionState(
    createClubAction,
    { success: false, error: null }
  );

  return (
    <form action={formAction}>
      <input name="name" />

      {state.error && (
        <div className="error">{state.error.message}</div>
      )}

      <button disabled={isPending}>
        {isPending ? 'Envoi...' : 'Envoyer'}
      </button>
    </form>
  );
}
```

## 🚨 Error Handling

### Types d'Erreurs

```typescript
// lib/errors.ts

export class ApiError extends Error {
  constructor(
    public code: string,
    message: string,
    public status?: number,
  ) {
    super(message);
    this.name = 'ApiError';
  }

  getUserMessage(): string {
    const messages: Record<string, string> = {
      VALIDATION_ERROR: 'Les données fournies sont invalides',
      NOT_FOUND: 'La ressource demandée n\'existe pas',
      UNAUTHORIZED: 'Vous devez être connecté',
      FORBIDDEN: 'Vous n\'avez pas les permissions nécessaires',
      INTERNAL_SERVER_ERROR: 'Une erreur interne est survenue',
    };

    return messages[this.code] || this.message;
  }
}
```

### Gestion dans Server Action

```typescript
'use server';

export async function updateClubAction(id: string, input: UpdateClubInput) {
  try {
    const validated = updateClubSchema.parse(input);
    const response = await clubsApi.update(id, validated);

    revalidatePath(`/clubs/${id}`);

    return { success: true, data: response };
  } catch (error) {
    // Zod validation errors
    if (error instanceof z.ZodError) {
      return {
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Données invalides',
          details: error.errors.map(e => ({
            field: e.path.join('.'),
            message: e.message,
          })),
        },
      };
    }

    // API errors (404, 403, etc.)
    if (error instanceof ApiError) {
      return {
        success: false,
        error: {
          code: error.code,
          message: error.getUserMessage(),
        },
      };
    }

    // Network errors
    if (error instanceof TypeError && error.message.includes('fetch')) {
      return {
        success: false,
        error: {
          code: 'NETWORK_ERROR',
          message: 'Impossible de contacter le serveur',
        },
      };
    }

    // Unknown errors
    console.error('Server Action Error:', error);
    return {
      success: false,
      error: {
        code: 'UNKNOWN_ERROR',
        message: 'Une erreur est survenue',
      },
    };
  }
}
```

## 📋 Exemples Complets

### Create (POST)

```typescript
'use server';

export async function createClubAction(input: CreateClubInput) {
  const validated = createClubSchema.parse(input);
  const response = await clubsApi.create(validated);

  revalidatePath('/dashboard/coach');

  return { success: true, data: response };
}
```

### Update (PUT/PATCH)

```typescript
'use server';

export async function updateClubAction(id: string, input: UpdateClubInput) {
  const validated = updateClubSchema.parse(input);
  const response = await clubsApi.update(id, validated);

  revalidatePath(`/clubs/${id}`);
  revalidatePath('/dashboard/coach');

  return { success: true, data: response };
}
```

### Delete (DELETE)

```typescript
'use server';

export async function deleteClubAction(id: string) {
  await clubsApi.delete(id);

  revalidatePath('/dashboard/coach');
  revalidatePath('/clubs');

  return { success: true };
}
```

### Batch Operation

```typescript
'use server';

export async function removeMembersAction(clubId: string, memberIds: string[]) {
  const results = await Promise.allSettled(
    memberIds.map(id => clubsApi.removeMember(clubId, id))
  );

  const successful = results.filter(r => r.status === 'fulfilled').length;
  const failed = results.filter(r => r.status === 'rejected').length;

  revalidatePath(`/clubs/${clubId}/members`);

  return {
    success: failed === 0,
    data: { successful, failed },
  };
}
```

## ✅ Checklist Server Actions

- [ ] `'use server'` directive en première ligne
- [ ] Schema Zod pour validation
- [ ] Types inférés depuis schema (`z.infer<>`)
- [ ] Type de résultat (success/error pattern)
- [ ] Appel API backend (pas de logique métier)
- [ ] `revalidatePath()` ou `revalidateTag()` après mutation
- [ ] Error handling exhaustif (Zod, API, Network, Unknown)
- [ ] Messages d'erreur traduits pour utilisateur
- [ ] Fichier nommé `*.action.ts`
- [ ] Export dans barrel `index.ts`

## 🚨 Erreurs Courantes

### 1. Logique Métier dans Server Action

```typescript
// ❌ MAUVAIS - Logique métier dans Server Action
export async function createClubAction(input: CreateClubInput) {
  // Validation métier (devrait être dans backend)
  if (input.name.includes('bad_word')) {
    return { success: false, error: 'Name invalid' };
  }

  // Calculs métier (devrait être dans backend)
  const price = input.plan === 'PRO' ? 9.99 : 0;

  // ...
}

// ✅ BON - Délégation au backend
export async function createClubAction(input: CreateClubInput) {
  // Validation simple
  const validated = createClubSchema.parse(input);

  // Backend fait toute la logique
  const response = await clubsApi.create(validated);

  revalidatePath('/clubs');
  return { success: true, data: response };
}
```

### 2. Oublier revalidatePath

```typescript
// ❌ MAUVAIS - Cache pas invalidé
export async function createClubAction(input: CreateClubInput) {
  const response = await clubsApi.create(input);
  return { success: true, data: response };
  // UI ne se met pas à jour !
}

// ✅ BON - Cache invalidé
export async function createClubAction(input: CreateClubInput) {
  const response = await clubsApi.create(input);

  revalidatePath('/clubs'); // Important !

  return { success: true, data: response };
}
```

### 3. Erreurs Non Gérées

```typescript
// ❌ MAUVAIS - Erreurs non gérées
export async function createClubAction(input: CreateClubInput) {
  const response = await clubsApi.create(input); // Peut throw
  return { success: true, data: response };
}

// ✅ BON - Toutes les erreurs gérées
export async function createClubAction(input: CreateClubInput) {
  try {
    const response = await clubsApi.create(input);
    return { success: true, data: response };
  } catch (error) {
    // Gestion complète des erreurs
    return {
      success: false,
      error: {
        code: 'ERROR',
        message: 'Une erreur est survenue',
      },
    };
  }
}
```

## 📚 Skills Complémentaires

- **api-contracts** : DTOs, Types, Validation frontend/backend
- **use-optimistic** : Optimistic updates avec Server Actions
- **atomic-component** : Composants utilisant Server Actions

---

**Rappel** : Server Actions = **Couche mince** d'orchestration. Toute la logique métier est dans le **backend NestJS**.
