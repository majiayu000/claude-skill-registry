---
name: mobile-feature
description: Use when creating or modifying React Native features in apps/mobile. Enforces React Native safety patterns, i18n, and Expo best practices.
---

# Mobile Feature Development Skill

Use this skill when working on React Native features in `apps/mobile/`.

## Critical React Native Safety Patterns

### Boolean Rendering Safety

**NEVER** use truthy checks with numbers in JSX - React Native renders `0` as literal text:

```tsx
// ❌ DANGEROUS - renders '0' when count is 0
{count && <Text>{count} items</Text>}

// ✅ SAFE - explicit null check
{count != null && <Text>{count} items</Text>}

// ✅ SAFE - hide zeros
{count > 0 && <Text>{count} items</Text>}
```

**Why**: `{0 && <Component>}` causes "Text strings must be rendered within a <Text> component" error.

### Always Check For:
- Number conditionals: Replace `{number && ...}` with `{number > 0 && ...}` or `{number != null && ...}`
- Array conditionals: Use `{array.length > 0 && ...}` not `{array.length && ...}`
- Optional chains: Use `{value?.property != null && ...}` not `{value?.property && ...}`

## Internationalization Requirements

**ALL text must use translations** - no hardcoded strings:

```tsx
// ✅ REQUIRED
import { useTranslation } from '@hounii/i18n';
const { t } = useTranslation('mobile');

<Text>{t('screen.title')}</Text>

// ❌ FORBIDDEN - no fallback pattern (masks missing keys)
<Text>{t('screen.title') || 'Default'}</Text>

// ❌ FORBIDDEN - no hardcoded strings
<Text>Screen Title</Text>
```

### Translation File Structure:
- Location: `packages/i18n/translations/`
- Namespaces: `mobile.json`, `common.json`
- Languages: `en/`, `fr/`, `de/`, `ar/`

## Tamagui UI Components

Always use Tamagui components from `@hounii/ui`:

```tsx
import { Button, Text, View } from '@hounii/ui';

// Use design tokens, not hardcoded values
<View backgroundColor="$background" padding="$4">
  <Text color="$color" fontSize="$5">{t('title')}</Text>
</View>
```

## Feature-Driven Structure

Organize by feature in `apps/mobile/features/`:

```
features/
├── auth/
│   ├── screens/
│   ├── components/
│   ├── hooks/
│   └── index.ts
└── profile/
    ├── screens/
    ├── components/
    ├── hooks/
    └── index.ts
```

## State Management

Use Zustand stores from `@hounii/lib`:

```typescript
import { useUserStore } from '@hounii/lib/stores';

// Persisted stores MUST have version + migrate
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useFeatureStore = create<FeatureState>()(
  persist(
    (set) => ({
      // state
    }),
    {
      name: 'feature-store',
      version: 1,
      migrate: (persistedState: any, version: number) => {
        if (version === 0) {
          // Migration logic
        }
        return persistedState as FeatureState;
      },
    }
  )
);
```

## Solito Universal Navigation

**CRITICAL**: Use Solito for navigation (not Expo Router directly). This enables code sharing with web.

```tsx
// ✅ CORRECT - Solito Link (works on mobile + web)
import { Link } from 'solito/link';

<Link href="/profile">
  <Text>Go to Profile</Text>
</Link>

// ✅ CORRECT - Solito Router (works on mobile + web)
import { useRouter } from 'solito/router';

const router = useRouter();
router.push('/profile');
router.replace('/login');
router.push({ pathname: '/post/[id]', params: { id: '123' } });

// ❌ WRONG - Don't use Expo Router directly
import { router } from 'expo-router'; // Breaks web compatibility
```

### Route Files vs. Screens

**CRITICAL**: Route files (`app/`) should ONLY handle routing. All screens live in `features/`.

```tsx
// ✅ CORRECT - Route file (apps/mobile/app/(tabs)/index.tsx)
import { HomeScreen } from '@/features/home';
export default HomeScreen;

// ✅ CORRECT - Screen file (apps/mobile/features/home/screens/HomeScreen.tsx)
export function HomeScreen() {
  return (
    <YStack>
      <Text>{t('home.title')}</Text>
    </YStack>
  );
}

// ❌ WRONG - Don't put screen logic in route file
export default function Home() {
  // This logic belongs in features/home/screens/HomeScreen.tsx
  return <YStack>...</YStack>;
}
```

## Development Checklist

When creating a new mobile feature:

1. **Safety Patterns**
   - [ ] All number conditionals use explicit checks (`> 0` or `!= null`)
   - [ ] No truthy checks with potentially falsy values

2. **Internationalization**
   - [ ] All text uses `t()` from `@hounii/i18n`
   - [ ] Translation keys added to `packages/i18n/translations/`
   - [ ] No hardcoded strings or fallback patterns

3. **UI Components**
   - [ ] Using Tamagui components from `@hounii/ui`
   - [ ] Using design tokens (e.g., `$background`, `$4`) not hardcoded values
   - [ ] Dark mode compatibility verified

4. **Feature Organization**
   - [ ] Code in appropriate `features/` directory
   - [ ] Exports through feature `index.ts`
   - [ ] Shared logic extracted to hooks

5. **State Management**
   - [ ] Using Zustand stores from `@hounii/lib`
   - [ ] Persisted stores have `version` and `migrate` functions

6. **Type Safety**
   - [ ] TypeScript types defined
   - [ ] No `any` types without justification
   - [ ] Props interfaces exported

7. **Navigation**
   - [ ] Routes defined in `app/` directory (routing ONLY)
   - [ ] Screens in `features/` directory (logic + UI)
   - [ ] Using Solito's `Link` and `useRouter` (not Expo Router directly)

## Before Requesting Commit

1. Run quality gates: `pnpm lint && pnpm type-check`
2. Provide user with testing instructions:
   - Which screen/feature to test
   - Expected behavior
   - Edge cases to verify (e.g., when count is 0)
3. **WAIT for explicit user approval** - never commit without confirmation

## Common Pitfalls

- **Platform-specific code**: Use `Platform.OS` checks or `.ios.tsx`/`.android.tsx` files
- **Async storage**: Use `@hounii/lib/storage` wrapper, not raw AsyncStorage
- **Images**: Use `expo-image` not `react-native` Image component
- **Icons**: Use `@tamagui/lucide-icons` from `@hounii/ui`

## References

- Main config: [CLAUDE.md](../../../CLAUDE.md)
- Mobile app: [apps/mobile/](../../../apps/mobile/)
- UI package: [packages/ui/](../../../packages/ui/)
- i18n package: [packages/i18n/](../../../packages/i18n/)
