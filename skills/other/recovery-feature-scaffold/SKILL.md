---
name: recovery-feature-scaffold
description: Scaffold complete features for the Steps to Recovery app including database schema, encrypted storage, offline sync, React Query hooks, screens, and tests. Use when adding new data models (gratitude lists, resentments, daily inventory), creating new journaling features, building step work tools, or implementing any new feature requiring SQLite + Supabase sync.
---

# Recovery Feature Scaffold

Generate complete, production-ready features for Steps to Recovery with one command.

## Quick Start

```bash
# From project root
cd .claude/skills/recovery-feature-scaffold/scripts
node scaffold.js <FeatureName>

# Example - creates a complete gratitude list feature
node scaffold.js GratitudeList
```

This generates **9 files** in under 1 second with all boilerplate wired up.

This generates:

- Database migration (SQLite + Supabase)
- TypeScript types
- Encrypted storage hooks (useFeature.ts)
- CRUD operations with React Query
- List screen + Detail/Edit screen
- Navigation updates
- Test file

## What Gets Generated

```
feature: GratitudeList

apps/mobile/src/
├── features/gratitude-list/
│   ├── types.ts              # TypeScript interfaces
│   ├── hooks/
│   │   └── useGratitude.ts   # React Query + encryption
│   ├── screens/
│   │   ├── GratitudeListScreen.tsx
│   │   └── GratitudeDetailScreen.tsx
│   ├── components/
│   │   └── GratitudeCard.tsx
│   └── __tests__/
│       └── gratitude.test.ts
├── lib/
│   └── database/
│       └── migrations/
│           └── 007_add_gratitude_list.sql
└── navigation/
    └── AppNavigator.tsx      # Auto-updated

supabase/migrations/
└── 007_add_gratitude_list.sql  # RLS policies included
```

## Manual Scaffolding (No Script)

Follow this 5-step workflow when script isn't available:

### Step 1: Define Types

Create `src/features/<feature>/types.ts`:

```typescript
export interface GratitudeItem {
  id: string;
  user_id: string;
  encrypted_content: string;
  category: 'people' | 'things' | 'experiences' | 'other';
  created_at: string;
  updated_at: string;
}

export interface CreateGratitudeInput {
  content: string;
  category: GratitudeItem['category'];
}

export interface UpdateGratitudeInput {
  id: string;
  content?: string;
  category?: GratitudeItem['category'];
}
```

### Step 2: Create Database Migration

SQLite migration (`src/lib/database/migrations/XXX_add_feature.sql`):

```sql
-- SQLite migration
CREATE TABLE IF NOT EXISTS gratitude_items (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  encrypted_content TEXT NOT NULL,
  category TEXT CHECK (category IN ('people', 'things', 'experiences', 'other')),
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_gratitude_user ON gratitude_items(user_id);
CREATE INDEX IF NOT EXISTS idx_gratitude_created ON gratitude_items(created_at DESC);
```

Supabase migration (`supabase/migrations/XXX_add_feature.sql`):

```sql
-- Supabase table
CREATE TABLE IF NOT EXISTS public.gratitude_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  encrypted_content TEXT NOT NULL,
  category TEXT CHECK (category IN ('people', 'things', 'experiences', 'other')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- RLS Policies
ALTER TABLE public.gratitude_items ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can only access their own gratitude items"
  ON public.gratitude_items FOR ALL
  USING (auth.uid() = user_id);

-- Trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_gratitude_items_updated_at
  BEFORE UPDATE ON public.gratitude_items
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

### Step 3: Create Encrypted Hooks

`src/features/<feature>/hooks/useFeature.ts`:

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useDatabase } from '../../../contexts/DatabaseContext';
import { encryptContent, decryptContent } from '../../../utils/encryption';
import { generateUUID } from '../../../utils/uuid';
import type { GratitudeItem, CreateGratitudeInput, UpdateGratitudeInput } from '../types';

const FEATURE_KEY = 'gratitude-items';

export function useGratitudeItems() {
  const { db, userId } = useDatabase();

  return useQuery({
    queryKey: [FEATURE_KEY],
    queryFn: async (): Promise<GratitudeItem[]> => {
      if (!db) throw new Error('Database not initialized');

      const items = await db.getAllAsync<GratitudeItem>(
        'SELECT * FROM gratitude_items WHERE user_id = ? ORDER BY created_at DESC',
        userId,
      );

      // Decrypt content for display
      return Promise.all(
        items.map(async (item) => ({
          ...item,
          content: await decryptContent(item.encrypted_content),
        })),
      );
    },
    enabled: !!db && !!userId,
  });
}

export function useCreateGratitude() {
  const { db, userId } = useDatabase();
  const queryClient = useQueryClient();
  const { enqueueSync } = useSyncQueue();

  return useMutation({
    mutationFn: async (input: CreateGratitudeInput): Promise<GratitudeItem> => {
      if (!db) throw new Error('Database not initialized');

      const id = generateUUID();
      const now = Date.now();
      const encrypted = await encryptContent(input.content);

      await db.runAsync(
        `INSERT INTO gratitude_items (id, user_id, encrypted_content, category, created_at, updated_at)
         VALUES (?, ?, ?, ?, ?, ?)`,
        id,
        userId,
        encrypted,
        input.category,
        now,
        now,
      );

      const item: GratitudeItem = {
        id,
        user_id: userId!,
        encrypted_content: encrypted,
        category: input.category,
        created_at: now.toString(),
        updated_at: now.toString(),
      };

      // Queue for sync
      await enqueueSync('gratitude_items', id, 'INSERT', item);

      return item;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [FEATURE_KEY] });
    },
  });
}

export function useUpdateGratitude() {
  const { db } = useDatabase();
  const queryClient = useQueryClient();
  const { enqueueSync } = useSyncQueue();

  return useMutation({
    mutationFn: async (input: UpdateGratitudeInput): Promise<void> => {
      if (!db) throw new Error('Database not initialized');

      const now = Date.now();
      const updates: string[] = [];
      const values: (string | number)[] = [];

      if (input.content) {
        updates.push('encrypted_content = ?');
        values.push(await encryptContent(input.content));
      }
      if (input.category) {
        updates.push('category = ?');
        values.push(input.category);
      }

      updates.push('updated_at = ?');
      values.push(now);
      values.push(input.id);

      await db.runAsync(`UPDATE gratitude_items SET ${updates.join(', ')} WHERE id = ?`, ...values);

      // Queue for sync
      await enqueueSync('gratitude_items', input.id, 'UPDATE', { id: input.id });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [FEATURE_KEY] });
    },
  });
}

export function useDeleteGratitude() {
  const { db } = useDatabase();
  const queryClient = useQueryClient();
  const { enqueueSync } = useSyncQueue();

  return useMutation({
    mutationFn: async (id: string): Promise<void> => {
      if (!db) throw new Error('Database not initialized');

      await db.runAsync('DELETE FROM gratitude_items WHERE id = ?', id);

      // Queue for sync
      await enqueueSync('gratitude_items', id, 'DELETE');
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [FEATURE_KEY] });
    },
  });
}
```

### Step 4: Create Screens

`src/features/<feature>/screens/FeatureListScreen.tsx`:

```typescript
import { useGratitudeItems, useDeleteGratitude } from '../hooks/useGratitude';
import { GratitudeCard } from '../components/GratitudeCard';
import { EmptyState } from '../../../components/EmptyState';
import { Button } from '../../../components/ui/Button';

export function GratitudeListScreen({ navigation }): React.ReactElement {
  const { data: items, isLoading } = useGratitudeItems();
  const deleteMutation = useDeleteGratitude();

  if (isLoading) return <LoadingScreen />;

  return (
    <View className="flex-1 bg-slate-900">
      <FlatList
        data={items}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <GratitudeCard
            item={item}
            onPress={() => navigation.navigate('GratitudeDetail', { id: item.id })}
            onDelete={() => deleteMutation.mutate(item.id)}
          />
        )}
        ListEmptyComponent={
          <EmptyState
            icon="Heart"
            title="No Gratitude Items"
            description="Start building your gratitude practice by adding your first item."
          />
        }
      />
      <FloatingActionButton
        onPress={() => navigation.navigate('GratitudeDetail', { id: 'new' })}
      />
    </View>
  );
}
```

### Step 5: Add Navigation

Update `src/navigation/AppNavigator.tsx`:

```typescript
import { GratitudeListScreen } from '../features/gratitude-list/screens/GratitudeListScreen';
import { GratitudeDetailScreen } from '../features/gratitude-list/screens/GratitudeDetailScreen';

// Add to stack navigator
<Stack.Screen
  name="GratitudeList"
  component={GratitudeListScreen}
  options={{ title: 'Gratitude' }}
/>
<Stack.Screen
  name="GratitudeDetail"
  component={GratitudeDetailScreen}
  options={{ title: 'Gratitude Item' }}
/>
```

Update `src/navigation/types.ts`:

```typescript
export type RootStackParamList = {
  // ... existing screens
  GratitudeList: undefined;
  GratitudeDetail: { id: string };
};
```

## Feature Templates

### Template: Simple List (Gratitude, Affirmations)

Single text field + category/tags.

### Template: Journal Entry (Daily Reflection, Step Work)

Rich text content + mood/feelings + date.

### Template: Checklist (Step Tasks, Daily Goals)

Multiple items with checkboxes + progress tracking.

### Template: Relationship (People, Sponsors)

Contact info + relationship type + notes.

## Best Practices

1. **Always encrypt sensitive content** - Use `encryptContent()` before storing
2. **Queue all mutations** - Call `enqueueSync()` after every write
3. **Invalidate queries** - Use `queryClient.invalidateQueries()` after mutations
4. **Add indexes** - Index `user_id` and `created_at` columns
5. **Test encryption** - Verify roundtrip in generated tests

## Complete Example

See [references/example-output.md](references/example-output.md) for full generated code from `node scaffold.js GratitudeList`.

## Common Feature Patterns

| Feature Type  | Command                           | Use Case                        |
| ------------- | --------------------------------- | ------------------------------- |
| Simple List   | `node scaffold.js GratitudeList`  | Gratitude, affirmations, quotes |
| Journal Entry | `node scaffold.js DailyInventory` | Reflections, step work          |
| Checklist     | `node scaffold.js StepOneTasks`   | Step work tasks, goals          |
| Relationships | `node scaffold.js SponsorContact` | People, sponsors, contacts      |

## Troubleshooting

### Migration number collision

Script auto-detects next migration number. If you have conflicts, manually rename files.

### Missing imports

Add to `tsconfig.json` paths if needed:

```json
"@/features/*": ["./src/features/*"]
```

### Supabase deploy fails

Ensure you're logged in:

```bash
npx supabase login
npx supabase link --project-ref tbiunmmvfbakwlzykpwq
```
