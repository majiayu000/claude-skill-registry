---
name: angular-supabase-connector-setup
description: Add, repair, or standardize Supabase in Angular 20 using DI-first providers, typed InjectionTokens, and an optional adapter bridge to existing API services. Use when users ask to install `@supabase/supabase-js`, wire `createClient` through `app.config.ts`, centralize auth/data access in a reusable connector service, or keep legacy API abstractions injectable in Supabase workflows.
---

# Angular Supabase Connector Setup

## Goal

Implement a reusable Angular 20 Supabase integration that:
- creates one DI-managed Supabase client instance
- reads Supabase URL/key from Angular environment config
- exposes a typed connector service for auth/data operations
- optionally bridges an existing project API abstraction through an adapter token

## Inputs

- `projectRoot` (string, default: current working directory)
- `featurePath` (string, default: `src/app/core/supabase`)
- `projectName` (optional: required if workspace has multiple Angular app projects)
- `apiAdapterClassOrToken` (optional: existing API service token/class to bridge)

## Success Criteria

- `@supabase/supabase-js` is installed.
- Environment config includes `supabaseUrl` and `supabaseAnonKey` in dev and production files.
- `provideSupabaseConnector()` registers a single `SUPABASE_CLIENT` provider.
- `SupabaseConnector` is injectable and exposes typed auth/query methods.
- Optional API adapter bridge is injectable without hard dependency.
- Angular build passes after wiring.

## Workflow

### 1) Validate workspace and target project

1. Confirm `angular.json` and `package.json` exist in `projectRoot`.
2. Confirm `@angular/core` major version is `20`.
3. Detect application projects:
- If exactly one app exists, select it.
- If multiple apps exist and `projectName` is not provided, stop and request `projectName`.
4. Stop and report if not Angular 20.

### 2) Install Supabase SDK deterministically

Run in `projectRoot`:

```bash
npm i @supabase/supabase-js
```

If already present in `dependencies`, keep existing version unless user requested an upgrade.

### 3) Ensure environment keys exist

Ensure `supabaseUrl` and `supabaseAnonKey` exist in development and production environment files used by the selected app.

Target commonly includes:
- `src/environments/environment.ts`
- `src/environments/environment.development.ts`
- `src/environments/environment.prod.ts`

Expected shape:

```ts
export const environment = {
  // ...
  supabaseUrl: 'https://<project-ref>.supabase.co',
  supabaseAnonKey: '<anon-or-publishable-key>',
};
```

If environment files are missing, stop and report exactly which files are missing and what must be created for this workspace layout.

### 4) Create tokens and providers

Create `src/app/core/supabase/supabase.tokens.ts`:

```ts
import { InjectionToken } from '@angular/core';
import { SupabaseClient } from '@supabase/supabase-js';

export interface SupabaseApiAdapter {
  get<T>(path: string, params?: Record<string, string | number | boolean>): Promise<T>;
  post<TBody, TResponse>(path: string, body: TBody): Promise<TResponse>;
}

export const SUPABASE_CLIENT = new InjectionToken<SupabaseClient>('SUPABASE_CLIENT');
export const SUPABASE_API_ADAPTER = new InjectionToken<SupabaseApiAdapter>('SUPABASE_API_ADAPTER');
```

Create `src/app/core/supabase/supabase.providers.ts`:

```ts
import { EnvironmentProviders, makeEnvironmentProviders } from '@angular/core';
import { createClient } from '@supabase/supabase-js';
import { environment } from '../../../environments/environment';
import { SUPABASE_CLIENT } from './supabase.tokens';

export function provideSupabaseConnector(): EnvironmentProviders {
  return makeEnvironmentProviders([
    {
      provide: SUPABASE_CLIENT,
      useFactory: () => createClient(environment.supabaseUrl, environment.supabaseAnonKey),
    },
  ]);
}
```

### 5) Create connector service

Create `src/app/core/supabase/supabase.connector.ts`:

```ts
import { Inject, Injectable, Optional, inject } from '@angular/core';
import { PostgrestSingleResponse } from '@supabase/supabase-js';
import { SUPABASE_API_ADAPTER, SUPABASE_CLIENT, SupabaseApiAdapter } from './supabase.tokens';

@Injectable({ providedIn: 'root' })
export class SupabaseConnector {
  private readonly client = inject(SUPABASE_CLIENT);

  constructor(
    @Optional() @Inject(SUPABASE_API_ADAPTER) private readonly apiAdapter?: SupabaseApiAdapter,
  ) {}

  signInWithPassword(email: string, password: string) {
    return this.client.auth.signInWithPassword({ email, password });
  }

  selectOne<T>(table: string, column: string, value: string | number): Promise<PostgrestSingleResponse<T>> {
    return this.client.from(table).select('*').eq(column, value).single();
  }

  getViaApi<T>(path: string): Promise<T> {
    if (!this.apiAdapter) {
      throw new Error('SUPABASE_API_ADAPTER is not provided.');
    }
    return this.apiAdapter.get<T>(path);
  }
}
```

### 6) Optional adapter bridge for existing API service

If the project already has an API service, add an adapter class so Supabase code stays decoupled.

Example:

```ts
import { Injectable, inject } from '@angular/core';
import { firstValueFrom } from 'rxjs';
import { ApiService } from '../api/api.service';
import { SupabaseApiAdapter } from '../supabase/supabase.tokens';

@Injectable({ providedIn: 'root' })
export class ExistingApiAdapter implements SupabaseApiAdapter {
  private readonly api = inject(ApiService);

  get<T>(path: string, params?: Record<string, string | number | boolean>): Promise<T> {
    return firstValueFrom(this.api.get<T>(path, { params }));
  }

  post<TBody, TResponse>(path: string, body: TBody): Promise<TResponse> {
    return firstValueFrom(this.api.post<TResponse>(path, body));
  }
}
```

Wire in `app.config.ts`:

```ts
import { ApplicationConfig } from '@angular/core';
import { ExistingApiAdapter } from './core/api/existing-api.adapter';
import { SUPABASE_API_ADAPTER } from './core/supabase/supabase.tokens';
import { provideSupabaseConnector } from './core/supabase/supabase.providers';

export const appConfig: ApplicationConfig = {
  providers: [
    ExistingApiAdapter,
    { provide: SUPABASE_API_ADAPTER, useExisting: ExistingApiAdapter },
    provideSupabaseConnector(),
  ],
};
```

For adapter-free projects, register only `provideSupabaseConnector()`.

### 7) Verify

Run in `projectRoot`:

```bash
npm run build
```

Then verify:
- `SupabaseConnector` injects in a feature service/component without DI errors.
- `signInWithPassword()` and `selectOne()` compile and execute.
- Adapter-enabled setup resolves `SUPABASE_API_ADAPTER` and `getViaApi()` works.
- Adapter-free setup does not fail until `getViaApi()` is explicitly called.

## Guardrails

- Keep Supabase keys in environment/deployment secrets only.
- Never hard-require `SUPABASE_API_ADAPTER` in the connector.
- Keep connector responsibilities to transport/orchestration, not page-specific state.
- Keep Supabase internals decoupled from concrete `HttpClient`/`ApiService` implementations.
- Preserve existing API abstractions via adapter mapping rather than rewriting app API layers.
- If workspace validation fails, stop before file edits and provide exact remediation steps.
