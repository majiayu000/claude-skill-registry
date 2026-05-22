---
name: kramme:connect-extract-to-nx-libraries
description: Use this Skill when working in the Connect monorepo and needing to extract app code into proper Nx libraries.
---

# Extract Connect App Code to Nx Libraries

Migrate code from the Connect app folder (`apps/connect/`) into proper Nx libraries following established conventions.

## When to Use

- Moving feature code from `apps/connect/src/app/` to `libs/`
- Extracting shared types, components, or services into reusable libraries
- Refactoring monolithic app code into domain-driven library structure

## Library Structure

Follow the naming convention: `libs/<product>/<application>/<domain>/<type>`

**Products:** `academy`, `coaching`, `connect`, `shared`
**Applications:** `cms`, `shared`, `ufa` (User-Facing Application)
**Types:** `assets`, `data-access`, `domain`, `feature`, `styles`, `test-util`, `ui`, `util`

### Typical Feature Migration Structure

For a feature like "certification-rubrics", create:

```text
libs/connect/
├── shared/<domain>/domain/           # Shared types used by both CMS and UFA
├── cms/<domain>/
│   ├── domain/                       # CMS-specific models/types
│   ├── data-access/                  # CMS store, API clients
│   └── feature/                      # CMS components
└── ufa/<domain>/
    ├── domain/                       # UFA-specific models/types
    ├── data-access/                  # UFA store, API clients
    └── feature/                      # UFA components
```

## Discovery Phase (Required First Step)

Before planning the migration, discover ALL code related to the feature and confirm scope with the user.

### 1. Search for Feature-Related Code

Search the entire codebase for code related to the feature:

```bash
# Find all files with the feature name
find Connect/ng-app-monolith -type f -name "*<feature>*" | grep -v node_modules

# Search for feature-related imports and references
grep -r "<FeatureName>" Connect/ng-app-monolith --include="*.ts" --include="*.html" | grep -v node_modules

# Check for related types, interfaces, enums
grep -r "interface.*<Feature>\|type.*<Feature>\|enum.*<Feature>" Connect/ng-app-monolith --include="*.ts" | grep -v node_modules
```

### 2. Categorize Discovered Code

Organize findings into categories:

- **Components** (in `apps/connect/src/app/`)
  - CMS components (admin-facing)
  - UFA components (user-facing)
- **Stores/Services** (state management, API clients)
- **Types/Models** (interfaces, enums, DTOs)
- **Routes** (route definitions referencing components)
- **Related but separate features** (may share types but shouldn't be moved)

### 3. Present Findings and Ask User

**ALWAYS ask the user to confirm what should be moved:**

Present a summary like:

```markdown
## Found Feature-Related Code

### Components (X files)
- `apps/connect/src/app/site/event/components/<feature>/` (UFA)
- `apps/connect/src/app/cms/cms/components/<feature>/` (CMS)

### Stores/Services (X files)
- `libs/connect/cms/<related>/data-access/` - contains <feature> store actions

### Types (X files)
- `libs/connect/cms/<related>/data-access/src/lib/<feature>.model.ts`

### Routes referencing feature
- `apps/connect/src/app/site/event/event.routes.ts`
- `apps/connect/src/app/cms/client/client-cms.routes.ts`

### Related but potentially separate
- `apps/connect/src/app/cms/event/components/reporting/<feature>-reporting/`
  (reporting feature - may stay separate)

**Questions:**
1. Should all components be moved to new libraries?
2. Should the store be extracted or stay in existing library?
3. Should reporting components be included or remain separate?
```

### 4. Confirm Domain Name

Ask user to confirm the domain name for the new libraries:

- Suggested: `<feature>` or `<feature>-<qualifier>`
- Confirm it matches existing naming patterns in `libs/connect/`

## Git Commit Strategy

Structure commits in logical, reviewable chunks. Each commit should be atomic and build on the previous.

### Recommended Commit Sequence

1. **Extract shared types first**

   ```text
   Extract shared <Domain> types to shared domain library
   ```

   - Create `libs/connect/shared/<domain>/domain/`
   - Move enums and base interfaces used by both CMS and UFA
   - Update imports in existing code to use new library path

2. **Create domain libraries for CMS/UFA-specific types**

   ```text
   Add <Domain> domain libraries for CMS and UFA
   ```

   - Create `libs/connect/cms/<domain>/domain/`
   - Create `libs/connect/ufa/<domain>/domain/`
   - Move application-specific models and re-export shared types

3. **Move stores and API clients**

   ```text
   Move <Domain> stores to Nx data-access libraries
   ```

   - Create data-access libraries
   - Move store files and API clients
   - Update imports

4. **Move components**

   ```text
   Move <Domain> components to Nx feature libraries
   ```

   - Create feature libraries
   - Move component files
   - Update route imports
   - Delete old component folders from app

5. **Rename files and selectors to match conventions**

   ```text
   Rename <Domain> files, components, and selectors
   ```

   - Rename files: `my-component.ts` → `ufa-<domain>-my-component.ts`
   - Update component selectors: `co-my-component` → `co-ufa-<domain>-my-component`
   - Update template references

6. **Add metadata and cleanup**

   ```text
   Add tech-debt tags to <Domain> libraries
   ```

   - Add appropriate tech-debt tags to `project.json`
   - Clean up any remaining old imports or exports

### Commit Message Guidelines

- Use imperative mood: "Move components" not "Moved components"
- Keep first line short and descriptive
- No conventional commit prefixes (`feat:`, `fix:`, etc.)
- No issue numbers in commit messages

### Why This Order?

1. **Types first** - Other code depends on types; moving them first prevents broken imports
2. **Data-access before feature** - Components often depend on stores
3. **Rename last** - Renaming is cosmetic; do functional moves first
4. **Metadata last** - Tags and cleanup don't affect functionality

## Migration Steps

### 1. Plan Library Structure

Based on discovery phase, identify what code moves where:

- **Shared types** → `libs/connect/shared/<domain>/domain/`
- **CMS components** → `libs/connect/cms/<domain>/feature/`
- **CMS stores/clients** → `libs/connect/cms/<domain>/data-access/`
- **UFA components** → `libs/connect/ufa/<domain>/feature/`
- **UFA stores/clients** → `libs/connect/ufa/<domain>/data-access/`

### 2. Create Libraries Using Custom Generators

```bash
cd Connect/ng-app-monolith

# Create domain libraries for types
yarn exec nx g @consensus/nx:angular-library --product=connect --application=shared --domain=<domain> --type=domain
yarn exec nx g @consensus/nx:angular-library --product=connect --application=cms --domain=<domain> --type=domain
yarn exec nx g @consensus/nx:angular-library --product=connect --application=ufa --domain=<domain> --type=domain

# Create data-access libraries for stores/clients
yarn exec nx g @consensus/nx:angular-library --product=connect --application=cms --domain=<domain> --type=data-access
yarn exec nx g @consensus/nx:angular-library --product=connect --application=ufa --domain=<domain> --type=data-access

# Create feature libraries for components
yarn exec nx g @consensus/nx:angular-library --product=connect --application=cms --domain=<domain> --type=feature
yarn exec nx g @consensus/nx:angular-library --product=connect --application=ufa --domain=<domain> --type=feature
```

### 3. Move and Rename Files

**Naming conventions:**

- CMS components: `cms-<domain>-<name>.component.ts`
- UFA components: `ufa-<domain>-<name>.component.ts`
- Stores: `<application>-<domain>.store.ts`
- Clients: `<application>-<domain>.client.ts`
- Types: `<application>-<domain>.model.ts` or `shared-<domain>.types.ts`

**Selector prefixes:**

- CMS: `co-cms-<domain>-`
- UFA: `co-ufa-<domain>-`

### 4. Type Separation Best Practices

**Shared types** (in `shared/<domain>/domain/`):

- Enums used by both CMS and UFA
- Base interfaces/types for entities
- Types that mirror backend DTOs

**CMS-specific types** (in `cms/<domain>/domain/`):

- Admin-only fields (e.g., `locked`, `distribution`)
- CMS action models (Create, Update, Delete)
- Re-export shared types for convenience

**UFA-specific types** (in `ufa/<domain>/domain/`):

- Use `Omit<SharedType, 'adminField'>` to hide admin-only fields
- Client-specific view models
- User-facing answer/response types

Example type separation:

```typescript
// shared-certification-rubrics.types.ts
export interface CertificationsQuestionnaire {
  id: string;
  title: string;
  locked: boolean;  // Admin-only concept
  // ...
}

// ufa-certification-rubrics.model.ts
import { CertificationsQuestionnaire } from '@consensus/connect/shared/certification-rubrics/domain';

// Hide 'locked' from UFA consumers
export type ClientCertificationQuestionnaire = Omit<CertificationsQuestionnaire, 'locked'>;
```

### 5. Update Imports and Exports

**In each library's `index.ts`:**

```typescript
// Only export public API
export * from './lib/<domain>.model';
export { MyComponent } from './lib/my-component/my-component.component';
```

**Update consuming code:**

```typescript
// Before (relative import from app)
import { MyComponent } from './components/my-component/my-component.component';

// After (library import)
import { MyComponent } from '@consensus/connect/ufa/<domain>/feature';
```

### 6. Update Route Files

Update route imports to use the new library paths:

```typescript
// apps/connect/src/app/site/event/event.routes.ts
import {
  ComponentA,
  ComponentB,
} from '@consensus/connect/ufa/<domain>/feature';
```

### 7. Add Tech-Debt Tags

If migrating legacy code with known issues, add appropriate tags in `project.json`:

```json
{
  "tags": [
    "product:connect",
    "application:ufa",
    "domain:<domain>",
    "type:feature",
    "tech-debt:default-change-detection",
    "tech-debt:lax-typing"
  ]
}
```

### 8. Clean Up Old Location

After migration:

1. Delete the old component folders from `apps/connect/`
2. Remove old exports from app-level barrel files
3. Update any remaining imports in the app

### 9. Verify Path Aliases

Confirm `tsconfig.base.json` has the new path aliases:

```json
{
  "@consensus/connect/shared/<domain>/domain": ["libs/connect/shared/<domain>/domain/src/index.ts"],
  "@consensus/connect/cms/<domain>/data-access": ["libs/connect/cms/<domain>/data-access/src/index.ts"],
  "@consensus/connect/cms/<domain>/domain": ["libs/connect/cms/<domain>/domain/src/index.ts"],
  "@consensus/connect/cms/<domain>/feature": ["libs/connect/cms/<domain>/feature/src/index.ts"],
  "@consensus/connect/ufa/<domain>/data-access": ["libs/connect/ufa/<domain>/data-access/src/index.ts"],
  "@consensus/connect/ufa/<domain>/domain": ["libs/connect/ufa/<domain>/domain/src/index.ts"],
  "@consensus/connect/ufa/<domain>/feature": ["libs/connect/ufa/<domain>/feature/src/index.ts"]
}
```

## Post-Migration Verification

### 1. Build and Test

```bash
# Build affected projects
yarn exec nx affected --targets=build --base=master

# Lint affected projects
yarn exec nx affected --targets=lint --base=master

# Run affected tests
yarn exec nx affected --targets=test --base=master
```

### 2. Verify No Leftover Code

```bash
# Check for remaining feature code in app folder
find Connect/ng-app-monolith/apps/connect -type d -name "*<domain>*"
find Connect/ng-app-monolith/apps/connect -type f -name "*<domain>*"

# Check for old import paths still in use
grep -r "from '\.\./.*<domain>" Connect/ng-app-monolith/apps/connect --include="*.ts"
```

### 3. Verify Routes Work

- Test CMS routes that use the migrated components
- Test UFA routes that use the migrated components
- Confirm lazy loading still works

## Common Pitfalls

1. **Don't break circular dependencies** - Ensure domain libs don't import from feature libs
2. **Don't duplicate types** - Use re-exports in CMS/UFA domain libs for shared types
3. **Don't forget route updates** - App routes must import from new library locations
4. **Don't mix concerns** - Keep stores in data-access, components in feature, types in domain
5. **Don't over-export** - Only export public API from library index.ts
6. **Don't move related but separate features** - Reporting, analytics, etc. may share types but stay separate

## Reference

See branch `Abildtoft/wan-148-impl` for a complete example of migrating Certification Rubrics from `apps/connect/` into proper Nx libraries.
