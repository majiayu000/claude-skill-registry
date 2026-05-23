---
description: Generate TypeScript API client from OpenAPI spec using Orval for NovaTune frontend (project)
---
# Generate API Client Skill

Generate a typed TypeScript client from the NovaTune API's OpenAPI specification using Orval.

## Overview

This skill configures Orval to generate:
- TypeScript types for all API models
- Axios-based HTTP client functions
- Request/response types for all endpoints
- Integration with custom HTTP instance for auth injection

## Orval Configuration

### packages/api-client/orval.config.ts

```typescript
import { defineConfig } from 'orval';

export default defineConfig({
  novatune: {
    input: {
      target: 'http://localhost:5000/openapi/v1.json',
    },
    output: {
      mode: 'tags-split',
      target: './src/generated',
      schemas: './src/generated/models',
      client: 'axios',
      override: {
        mutator: {
          path: '../http/axios-instance.ts',
          name: 'customInstance',
        },
        query: {
          useQuery: true,
          useInfinite: true,
          useInfiniteQueryParam: 'cursor',
        },
      },
    },
    hooks: {
      afterAllFilesWrite: 'prettier --write',
    },
  },
});
```

## Custom HTTP Instance

### packages/api-client/src/http/axios-instance.ts

```typescript
import axios, { AxiosRequestConfig } from 'axios';

const instance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:5000',
  timeout: 30_000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const customInstance = <T>(config: AxiosRequestConfig): Promise<T> => {
  return instance(config).then(({ data }) => data);
};

export default instance;
```

## Generated Output Structure

```
packages/api-client/src/
├── index.ts
├── generated/
│   ├── auth/
│   │   ├── auth.ts
│   │   └── index.ts
│   ├── tracks/
│   │   ├── tracks.ts
│   │   └── index.ts
│   ├── playlists/
│   │   ├── playlists.ts
│   │   └── index.ts
│   ├── admin/
│   │   ├── admin.ts
│   │   └── index.ts
│   ├── telemetry/
│   │   ├── telemetry.ts
│   │   └── index.ts
│   └── models/
│       ├── index.ts
│       ├── loginRequest.ts
│       ├── loginResponse.ts
│       ├── track.ts
│       ├── playlist.ts
│       └── ...
└── http/
    └── axios-instance.ts
```

## Usage Example

```typescript
// In apps/player/src/features/library/composables/useTracks.ts
import { useQuery, useInfiniteQuery } from '@tanstack/vue-query';
import { getTracksV1 } from '@novatune/api-client';

export function useTracks(filters: Ref<TrackFilters>) {
  return useInfiniteQuery({
    queryKey: ['tracks', filters],
    queryFn: ({ pageParam }) => getTracksV1({
      ...filters.value,
      cursor: pageParam,
    }),
    getNextPageParam: (lastPage) => lastPage.nextCursor,
  });
}
```

## Package Exports

### packages/api-client/src/index.ts

```typescript
// Re-export all generated clients and types
export * from './generated/auth';
export * from './generated/tracks';
export * from './generated/playlists';
export * from './generated/admin';
export * from './generated/telemetry';
export * from './generated/models';

// Re-export custom HTTP instance for advanced usage
export { customInstance, default as axiosInstance } from './http/axios-instance';
```

## Generation Workflow

### 1. Ensure API is Running

```bash
# Start the backend
dotnet run --project src/NovaTuneApp/NovaTuneApp.AppHost
```

### 2. Generate Client

```bash
cd src/NovaTuneClient
pnpm --filter @novatune/api-client generate
```

### 3. Verify Output

```bash
ls packages/api-client/src/generated/
```

## CI Integration

### Generate in CI (Option A - Committed Code)

```yaml
# .github/workflows/frontend.yml
- name: Check API client is up to date
  run: |
    pnpm --filter @novatune/api-client generate
    git diff --exit-code packages/api-client/src/generated/
```

### Generate in CI (Option B - Generate Fresh)

```yaml
# .github/workflows/frontend.yml
- name: Start API for OpenAPI spec
  run: |
    dotnet run --project src/NovaTuneApp/NovaTuneApp.AppHost &
    sleep 30  # Wait for API to start

- name: Generate API client
  run: pnpm --filter @novatune/api-client generate
```

## OpenAPI Endpoint Reference

The NovaTune API exposes:
- **OpenAPI JSON**: `GET /openapi/v1.json`
- **Scalar UI**: `GET /scalar/v1`

## Type Customizations

### Handle Problem Details

```typescript
// packages/api-client/src/types/problem-details.ts
export interface ProblemDetails {
  type: string;
  title: string;
  status: number;
  detail?: string;
  instance?: string;
  extensions?: Record<string, unknown>;
}
```

### Extend Generated Types

```typescript
// packages/api-client/src/types/extensions.ts
import type { Track } from './generated/models';

export interface TrackWithStreamUrl extends Track {
  streamUrl?: string;
}
```

## Related Documentation

- **Frontend Plan**: `doc/implementation/frontend/main.md`
- **API Integration**: `doc/implementation/frontend/main.md#4-api-integration`

## Related Skills

- **setup-vue-workspace** - Create workspace structure first
- **implement-player-app** - Uses generated client
- **implement-admin-app** - Uses generated client

## Claude Agents

- **vue-app-implementer** - Uses generated client
- **api-client-generator** - Dedicated agent for API client tasks
