---
name: search-web-implementation
description: Search the web monorepo (../app) to find how web handles equivalent functionality. Use when implementing mobile features that need to match web behavior, finding web routes, or understanding how web handles a specific feature like statements, portfolios, or user flows.
---

# Search Web Implementation

Find how the web app handles equivalent functionality to ensure mobile/web consistency.

## Web Monorepo Location

The web monorepo is located at `../app` relative to the mobile-app workspace, or at the absolute path `/Users/timmy.garrabrant/Developer/app`.

## Key Directories

| Directory     | Contents                                         |
| ------------- | ------------------------------------------------ |
| `client/`     | Frontend React/TypeScript code (.tsx, .jsx, .ts) |
| `app/`        | Rails controllers, views, models                 |
| `engines/`    | Rails engines (modular features)                 |
| `subsystems/` | Domain subsystems (business logic)               |
| `config/`     | Routes, configuration                            |

## Search Strategy

### 1. Find Routes

Search Rails routes for URL patterns:

```bash
# Search route definitions
rg "quarterly_statements|annual_reports" ../app/config/ ../app/engines/*/config/
rg "activity.report|activity-report" ../app/config/ ../app/engines/*/config/
```

### 2. Find Frontend Components

Search React components in `client/`:

```bash
rg "QuarterlyStatement|AnnualReport" ../app/client/ --type tsx --type ts
rg "statement.*url|getStatementUrl" ../app/client/ -i
```

### 3. Find Backend Logic

Search subsystems and engines:

```bash
rg "def quarterly_statement|quarterly_statements" ../app/subsystems/ ../app/engines/
rg "activity_report|ActivityReport" ../app/subsystems/ ../app/engines/
```

### 4. Find Savers Routes

For savers-specific implementations:

```bash
rg "/savers/" ../app/client/ --type ts --type tsx
rg "savers.*route|route.*savers" ../app/config/ -i
```

## Common Search Patterns

### Find Feature by Name

```bash
rg "<feature_name>" ../app/client/ ../app/subsystems/ ../app/engines/
```

### Find URL/Route Definitions

```bash
rg "<url_pattern>" ../app/config/routes.rb ../app/engines/*/config/routes.rb
```

### Find React Components

```bash
rg "<ComponentName>" ../app/client/ --type tsx
```

### Find GraphQL Resolvers

```bash
rg "<resolver_name>" ../app/subsystems/*/lib/*/graphql/
```

## Workflow

1. **Identify the feature** - What mobile feature needs web parity?
2. **Search client/** - Find frontend implementation
3. **Search routes** - Find URL structure
4. **Search subsystems/** - Find backend business logic
5. **Compare patterns** - Note differences and document findings

## Output Format

When reporting findings, include:

```markdown
## Web Implementation: [Feature Name]

### Routes

- URL pattern: `/path/to/feature`
- File: `config/routes.rb:123`

### Frontend

- Component: `client/path/to/Component.tsx`
- Key logic: [brief description]

### Backend

- Subsystem: `subsystems/feature_name/`
- Key files: [list relevant files]

### Mobile Recommendation

[What the mobile app should do to match web]
```
