---
name: frontend
description: Use when working on app-partners (partner dashboard) or app-observatory (public statistics). Covers Next.js 15 patterns, DSFR components, API hooks, maps (MapLibre/Deck.gl), charts, and Meilisearch.
---

# Frontend Developer Skill

> **Read `app-partners/README.md` or `app-observatory/README.md` first** for setup and configuration.

---

## App Partners — Key Patterns

### API Integration

Custom `useRestQuery` hook:

```typescript
const { data, loading, error, refetch } = useRestQuery<DataType>(
  "v3",           // API version
  "endpoint/path",
  params,
  { method: "POST", paginate: false },
  [dependencies]
);
```

Available hooks:
- `useCampaignList()`, `useCampaignFind()`
- `useUsersList()`, `useOperatorsList()`, `useTerritoriesList()`
- `useExportsList()`, `useExportCreate()`, `useExportDownloadLink()`
- `useIncentiveGraph()`, `useOperatorsGraph()`

### State Management

React Context for authentication, no Redux/Zustand:

```typescript
const { isAuth, user, logout } = useAuth();
```

### DSFR Components

```typescript
import { Button, Input, Select, Table, Alert } from "@codegouvfr/react-dsfr";
import { fr } from "@codegouvfr/react-dsfr";

className={fr.cx("fr-container", "fr-mb-7w")}
```

Key components: Header, Footer, Button, Input, Select, Table, Pagination, Alert, Badge, Download.

### Form Validation (Zod)

```typescript
import { z } from "zod";

const schema = z.object({
  email: z.string().email(),
  name: z.string().min(1),
});
```

Input error state:

```typescript
<Input
  state={errors.email ? "error" : "default"}
  stateRelatedMessage={errors.email}
/>
```

### Modal Forms

`useActionsModal` hook for CRUD operations:

```typescript
const modal = useActionsModal<DataType>();
// modal.setCurrentRow(), modal.setOpenModal(), modal.setTypeModal()
```

### Authentication

ProConnect SSO flow:
1. Login via `ProConnectButton` -> ProConnect URL
2. Session check on load: `GET /auth/me`
3. Role-based access control

Role helpers:

```typescript
isRegistry(), isTerritory(), isOperator(), isAdmin(), isUser()
```

### Analytics

```typescript
import { sendEvent } from "@socialgouv/matomo-next";
void sendEvent({ category: "campagne", action: "Consultation" });
```

### Conventions

- Components: PascalCase (`AuthButton.tsx`)
- Hooks: camelCase with `use` prefix (`useCampaignList.ts`)
- Interfaces: PascalCase with `Interface` suffix
- Client components: Add `"use client"` directive
- Pre-build hook: `react-dsfr update-icons`

---

## App Observatory — Key Patterns

### Map Integration

```typescript
import Map from "react-map-gl/maplibre";
import DeckGL from "@deck.gl/react";
```

Deck.gl layers:
- `H3HexagonLayer` - Density visualization with hexagonal bins
- `ArcLayer` - Origin-destination flow visualization

### H3 Hexagonal Binning

```typescript
import { cellToBoundary, cellToLatLng } from "h3-js";
const h3Index = latLngToCell(lat, lng, 9); // Resolution 9 for journey data
```

### Data Visualization

Chart.js with react-chartjs-2:

```typescript
import { Line } from "react-chartjs-2";
import { Chart, CategoryScale, LinearScale, PointElement, LineElement } from "chart.js";
Chart.register(CategoryScale, LinearScale, PointElement, LineElement);
```

### API Data Fetching

```typescript
const { data, loading, error } = useApi<DataType>(url, params);
const jsonData = useJson<DataType>(url);
```

Key endpoints:

| Endpoint | Purpose |
|----------|---------|
| `/observatory/journeys` | Journey statistics |
| `/observatory/directions` | Direction analysis |
| `/observatory/od` | Origin-destination matrices |
| `/observatory/territories` | Territory data |

### Meilisearch Integration

```typescript
import { MeiliSearch } from "meilisearch";

const client = new MeiliSearch({ host: MEILISEARCH_URL });
const results = await client.multiSearch({
  queries: [
    { indexUid: "article", q: query },
    { indexUid: "resource", q: query },
    { indexUid: "page", q: query },
  ],
});
```

### MDX Content

```typescript
import { MDXRemote } from "next-mdx-remote/rsc";
import remarkGfm from "remark-gfm";
import rehypeSlug from "rehype-slug";

<MDXRemote
  source={content}
  options={{ mdxOptions: { remarkPlugins: [remarkGfm], rehypePlugins: [rehypeSlug] }}}
/>
```

Content fetched from Strapi CMS with 60s revalidation.

### Geographic Data

```typescript
type PerimeterType = "country" | "region" | "department" | "aom" | "epci" | "commune";
type INSEECode = string; // 5-digit commune code
```

Jenks natural breaks for choropleth maps:

```typescript
import { jenks } from "simple-statistics";
const breaks = jenks(values, 5);
```

### Conventions

- Suspense boundaries for async data
- Server/client component split
- Container/presentational pattern
- Strong TypeScript typing for geographic data
- Pre-build hook: `only-include-used-icons`
