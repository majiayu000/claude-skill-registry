---
name: feature-structure
description: Architecture patterns for organizing feature modules in the codebase. Use when creating new files, brand new features or pages.
---


### Tech Stack

React 18 · Next.js 15 · TypeScript · Wagmi · TanStack Query · Biome

### Feature Structure

```
src/features/{feature-name}/
├── {feature-name}-view.tsx    # Main orchestrator
├── components/                 # Feature-specific components
│   ├── filters/
│   ├── table/
│   └── {component}.tsx
├── hooks/                     # Feature-specific hooks (optional)
└── utils/                     # Feature-specific utilities (optional)
```


## Architecture

### Project Structure
```
/app                    # Next.js App Router pages
  /markets             # Market listing
  /market/[chainId]/[marketId]  # Market detail
  /positions/[account] # User positions
  /autovault           # Vault listing + detail
  /rewards             # Rewards dashboard
  /history/[account]   # Transaction history
  /settings            # User settings
  /admin/stats         # Admin stats
  /api/balances        # Only API route (token balances)

/src
  /data-sources        # Data fetching layer
    /morpho-api/       # Morpho API fetchers (14 files)
    /subgraph/         # Subgraph fallback fetchers
  /hooks               # 53 custom hooks
    /queries/          # React Query hooks (13+)
  /stores              # Zustand stores (16 total)
  /features            # Feature modules (markets, positions, autovault, swap, rewards)
  /constants           # Static data (oracle cache, chain configs)
  /utils               # Utilities (types, networks, RPC, etc.)
```

### File Naming

- Stores: `src/stores/use{Feature}{State}.ts`
- Queries: `src/hooks/queries/use{Entity}Query.ts`
- Derived hooks: `src/hooks/use{Processed|Filtered}{Entity}.ts`
- Features: `src/features/{name}/{name}-view.tsx`
