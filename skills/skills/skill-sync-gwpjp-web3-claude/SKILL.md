---
name: skill-sync
description: Syncs .claude knowledge files with the codebase. Detects stale reference files (hook catalogs, type indexes, schema references, theme docs) and regenerates them from source. Run after adding hooks, types, components, or schema changes.
disable-model-invocation: true
---

# Skill Sync

You are the **.claude folder synchronization agent**. Your job is to keep the knowledge files in `.claude/` in sync with the actual codebase. Stale reference files cause incorrect agent behavior, hallucinated hook names, and outdated patterns.

## When to Run

- After adding, removing, or modifying hooks in `src/hooks/`
- After adding, removing, or modifying types in `src/types/`
- After changes to `ponder.schema.ts`
- After changes to `src/theme/themeConfig.tsx`
- After adding, removing, or modifying Common components
- After adding or removing pages/routes
- Before major releases or after large refactors
- When Claude mentions hooks/types/tables that don't exist (indicates staleness)

## Sync Targets

| Knowledge File                                 | Source                                | Trigger                             |
| ---------------------------------------------- | ------------------------------------- | ----------------------------------- |
| `ponder-schema-specialist/schema-reference.md` | `ponder.schema.ts`                    | Schema table/column/index changes   |
| `wagmi-specialist/hook-reference.md`           | `src/hooks/blockchain/`               | Hook added/removed/renamed          |
| `wagmi-specialist/contracts-reference.md`      | `src/services/contracts/generated.ts` | Contract ABI added/removed/modified |
| `web3-implementer/ponder-reference.md`         | `src/hooks/ponder/`                   | Ponder hook added/removed           |
| `typescript-specialist/type-index.json`        | `src/types/`                          | Type added/removed/modified         |
| `.claude/docs/theme-reference.md`              | `src/theme/themeConfig.tsx`           | Palette/typography changes          |
| `.claude/docs/component-reference.md`          | `src/components/Common/`              | Common component API changes        |
| `skills/routes.json`                           | Router config / `src/pages/`          | Page added/removed                  |

## Workflow

### Step 0: Check Last Sync

Before detecting staleness, check when `/skill-sync` was last run:

1. Read `.claude/skills/skill-sync/.last-sync` (if it exists)
2. If it exists:
   - Get current branch: `git branch --show-current`
   - Check if stored commit is reachable: `git merge-base --is-ancestor <commitHash> HEAD`
   - Show status based on result:

   **Same branch, commit reachable:**

   ```
   Last sync: 2024-01-29 at commit abc1234 (main)
   Run `git diff abc1234..HEAD --stat` to see changes since last sync
   ```

   **Different branch but commit reachable:**

   ```
   Last sync: 2024-01-29 at commit abc1234 (main)
   ⚠️ Currently on feature-branch (synced on main)
   Run `git diff abc1234..HEAD --stat` to see changes since last sync
   ```

   **Commit not reachable (diverged branches):**

   ```
   Last sync: 2024-01-29 at commit abc1234 (main)
   ⚠️ Commit not in current branch history (branches diverged)
   Consider running a full sync on this branch
   ```

3. If `.last-sync` doesn't exist, note this is the first sync

### Step 1: Detect Staleness

For each sync target, check if the knowledge file is stale:

1. **Schema reference**: Compare table count in schema-reference.md vs tables in ponder.schema.ts
2. **Hook references**: Compare hook lists in reference files vs actual exports from index.ts files
3. **Type index**: Compare type names in type-index.json vs actual exports from src/types/
4. **Theme reference**: Compare palette keys in theme-reference.md vs themeConfig.tsx
5. **Component reference**: Compare component list vs actual files in src/components/Common/
6. **Routes**: Compare routes in routes.json vs pages in src/pages/

### Step 2: Report Findings

Present a sync status report:

```
## Sync Status

| File | Status | Details |
|------|--------|---------|
| schema-reference.md | ⚠️ STALE | Missing 3 tables: newTable1, newTable2, newTable3 |
| hook-reference.md | ✅ Current | 45 hooks match |
| ponder-reference.md | ⚠️ STALE | Missing hook: usePonderNewEntity |
| type-index.json | ✅ Current | 28 types match |
| theme-reference.md | ✅ Current | Palette unchanged |
| component-reference.md | ⚠️ STALE | New component: CommonNewWidget |
| routes.json | ✅ Current | 7 routes match |

**Action needed:** 3 files require sync
```

### Step 3: Ask User

Use `AskUserQuestion` to confirm:

```
Question: "Which files should I sync?"
Options:
  1. "Sync all stale files" (Recommended)
  2. "Sync specific files" - "Let me choose which ones"
  3. "Skip for now" - "I'll handle it manually"
```

### Step 4: Regenerate

For each file to sync:

#### Schema Reference (`ponder-schema-specialist/schema-reference.md`)

If a generation script exists:

```bash
npx tsx scripts/generate-schema-reference.ts
```

Otherwise, read `ponder.schema.ts` (or `src/services/ponder/ponder.schema.ts`) and extract:

- All `onchainTable()` definitions → table names, columns, types
- All `index()` calls → indexes
- All `relations()` calls → relationships
- ID format conventions from comments or patterns

Format as markdown tables matching the existing schema-reference.md structure.

#### Hook Reference (`wagmi-specialist/hook-reference.md`)

Scan `src/hooks/blockchain/` and extract:

1. **Read Hooks** (`useGet*.ts` excluding `*Live.ts`):
   - Hook name, file path
   - Parameters (from function signature)
   - Return type
   - Brief description (from JSDoc or infer from name)

2. **Transform Hooks** (`useGet*Live.ts`):
   - Hook name, file path
   - What ponder data it consumes
   - What domain type it returns

3. **Write Hooks** (`use*.ts` that import `useContractWriteWithState`):
   - Hook name, file path
   - Contract function it calls
   - Parameters

Format as categorized tables matching existing hook-reference.md structure.

#### Ponder Reference (`web3-implementer/ponder-reference.md`)

Scan `src/hooks/ponder/` and extract:

1. All exported hooks from index.ts
2. For each hook:
   - Name
   - What table(s) it queries
   - Whether it's live (SSE) or one-shot
   - Key parameters

Format as a hook catalog with query patterns.

#### Type Index (`typescript-specialist/type-index.json`)

Scan `src/types/` and extract:

```json
{
  "interfaces": [
    { "name": "Entity", "file": "entity.ts", "extends": "BaseEntity" },
    ...
  ],
  "types": [
    { "name": "EntityStatus", "file": "entity.ts", "kind": "union" },
    ...
  ],
  "transforms": [
    { "name": "transformPonderEntity", "file": "entity.ts", "input": "PonderEntity", "output": "Entity" },
    ...
  ]
}
```

#### Theme Reference (`.claude/docs/theme-reference.md`)

Read `src/theme/themeConfig.tsx` and extract:

1. **Palette colors**: All keys under `palette` with their values
2. **Typography variants**: All variants with size, weight, font family
3. **Spacing scale**: If customized
4. **Component overrides**: Key MUI component customizations

Format as the existing theme-reference.md structure (tables for palette, typography).

#### Component Reference (`.claude/docs/component-reference.md`)

Scan `src/components/Common/` and for each component:

1. Read the file
2. Extract the props interface
3. Extract key behaviors from implementation
4. Document usage patterns

Format as the existing component-reference.md structure (grouped by category).

#### Routes Config (`skills/routes.json`)

Scan `src/pages/` and router configuration:

1. List all page components
2. Map to routes (from router config or file structure)
3. Determine which require addresses (look for `:address` or similar params)
4. Add focus areas for each QA skill type

### Step 5: Verify

After regeneration:

1. Read back each regenerated file to verify it's valid
2. Check that the format matches the expected structure
3. Report completion:

```
## Sync Complete

✅ schema-reference.md - Regenerated (73 tables)
✅ ponder-reference.md - Regenerated (12 hooks)
✅ component-reference.md - Regenerated (added CommonNewWidget)

All knowledge files are now in sync with the codebase.
```

### Step 6: Record Sync

After successful sync, record when it happened:

1. Get current commit hash: `git rev-parse HEAD`
2. Get current branch: `git branch --show-current`
3. Get current timestamp
4. Write to `.claude/skills/skill-sync/.last-sync`:
   ```json
   {
     "lastSyncAt": "2024-01-29T14:30:00Z",
     "commitHash": "abc1234def5678",
     "branch": "main",
     "commitMessage": "Update CommonCard",
     "filesRegenerated": ["hook-reference.md", "schema-reference.md"]
   }
   ```

This file is gitignored (add to `.gitignore` if not already) since each developer may sync at different times.

## Quick Sync Commands

For partial syncs, the user may specify a target:

- `/skill-sync schema` - Only sync schema-reference.md
- `/skill-sync hooks` - Only sync hook references (wagmi + ponder)
- `/skill-sync contracts` - Only sync contracts-reference.md
- `/skill-sync types` - Only sync type-index.json
- `/skill-sync theme` - Only sync theme-reference.md
- `/skill-sync components` - Only sync component-reference.md
- `/skill-sync routes` - Only sync routes.json
- `/skill-sync all` - Full sync (default)

Parse `$ARGUMENTS` to determine scope.

## Staleness Detection Patterns

### Schema Staleness

```typescript
// Count tables in schema file
const schemaContent = await read("ponder.schema.ts");
const tableMatches = schemaContent.match(/export const \w+ = onchainTable/g);
const actualTableCount = tableMatches?.length ?? 0;

// Count tables in reference
const refContent = await read("schema-reference.md");
const refTableCount = (refContent.match(/^### /gm) ?? []).length;

const isStale = actualTableCount !== refTableCount;
```

### Hook Staleness

```typescript
// Get actual hooks from index.ts
const indexContent = await read("src/hooks/blockchain/index.ts");
const exportedHooks = indexContent.match(/export \* from "\.\/use\w+"/g);

// Get hooks from reference
const refContent = await read("hook-reference.md");
const documentedHooks = refContent.match(/`use\w+`/g);

const missingInRef = exportedHooks.filter((h) => !documentedHooks.includes(h));
const extraInRef = documentedHooks.filter((h) => !exportedHooks.includes(h));
```

### Type Staleness

```typescript
// Get actual types from src/types/index.ts
const indexContent = await read("src/types/index.ts");
const exportedTypes = indexContent.match(/export (type|interface) \w+/g);

// Compare with type-index.json
const typeIndex = JSON.parse(await read("type-index.json"));
const indexedTypes = [...typeIndex.interfaces, ...typeIndex.types].map(
  (t) => t.name
);
```

## What NOT to Do

- Do not modify source code files (only .claude/ knowledge files)
- Do not guess at hook parameters or types -- read the actual code
- Do not remove entries from reference files without checking if they still exist
- Do not skip the staleness check -- always detect before regenerating
- Do not regenerate files that are already current
