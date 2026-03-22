---
name: react-arch
description: Create the complete frontend architecture for a new entity in the React application. Generates TypeScript types, service class, context provider, custom hook, and registers the provider in main.tsx. Use this skill when the user asks to create a new entity, feature module, or domain area in the frontend.
---

This skill defines the standard approach for scaffolding a complete frontend entity architecture in this project. It creates all necessary files following the established patterns: Types, Service, Context, Hook, and Provider registration.

## Prerequisites

Before creating the architecture, you MUST:

1. **Ask the user** for the entity name (e.g., "Clan", "Achievement", "Shop")
2. **Ask the user** for the API base path (e.g., "/api/clan", "/api/achievement")
3. **Ask the user** for the entity fields/properties or check if API documentation exists in `docs/`
4. **Check if the entity already exists** — search `src/types/`, `src/services/`, `src/contexts/`, and `src/hooks/` before creating anything

## Creation Order

Always create files in this exact order:

1. **Types** → `src/types/{entity}.ts`
2. **Service** → `src/services/{entity}Service.ts`
3. **Context** → `src/contexts/{Entity}Context.tsx`
4. **Hook** → `src/hooks/use{Entity}.ts`
5. **Provider registration** → `src/main.tsx`

## Rules

1. **Never use `any` type** — all types must be explicitly defined.
2. **Never use `alert()` or `window.confirm()`** — use `toast` from `sonner` for notifications and `ConfirmModal` for confirmation dialogs.
3. **Always use `useCallback`** for all context methods to prevent unnecessary re-renders.
4. **Always include `loading`, `error`, and main data state** in every context.
5. **Always use the class-based service pattern** with private `handleResponse` method.
6. **Always use `getHeaders(true)`** from `apiHelpers` for authenticated requests.
7. **Always check `result.sucesso`** before updating state (API responses use Portuguese keys).
8. **Always export both** the singleton instance and the class from services.
9. **Always export the context as default** and the provider as named export.
10. **Always add JSDoc comments** to service methods and type interfaces.

## Step 1: Create Types

**File**: `src/types/{entity}.ts`

```typescript
/** {Entity} Types — Types for the {entity description} system */

// Enums (if needed)
export enum {Entity}StatusEnum {
  Unknown = 0,
  Active = 1,
  Inactive = 2,
}

// Core Entity
/** Main {entity} information */
export interface {Entity}Info {
  {entity}Id: number;
  name: string;
  // ... other fields with JSDoc comments
}

// DTOs
/** Data required to create a new {entity} (no ID) */
export interface {Entity}InsertInfo {
  name: string;
  // ... fields required for creation
}

/** Data required to update an existing {entity} (includes ID) */
export interface {Entity}UpdateInfo {
  {entity}Id: number;
  name: string;
  // ... fields required for update
}

// API Response Types — always include sucesso, mensagem, erros (Portuguese keys)
export interface {Entity}ListResult {
  {entities}: {Entity}Info[];
  sucesso: boolean;
  mensagem: string | null;
  erros: string[] | null;
}

export interface {Entity}GetResult {
  {entity}: {Entity}Info;
  sucesso: boolean;
  mensagem: string | null;
  erros: string[] | null;
}

/** Status-only operation result (import from existing types file if already defined) */
export interface StatusResult {
  sucesso: boolean;
  mensagem: string;
  erros: string[] | null;
}
```

**Key conventions:**
- API responses always have `sucesso`, `mensagem`, `erros` — Portuguese keys
- Entity IDs use camelCase: `{entity}Id` (e.g., `clanId`)
- Nullable fields use `| null`, not optional `?`
- Separate interfaces for Insert (no ID) and Update (with ID) DTOs
- If `StatusResult` already exists in another types file, import it instead of redefining

## Step 2: Create Service

**File**: `src/services/{entity}Service.ts`

```typescript
import type {
  {Entity}ListResult, {Entity}GetResult,
  {Entity}InsertInfo, {Entity}UpdateInfo, StatusResult,
} from '../types/{entity}';
import { getHeaders } from './apiHelpers';

const API_BASE = `${import.meta.env.VITE_GOBLIN_API_URL || 'http://localhost:4041'}/api/{entity-kebab}`;

interface {Entity}ServiceConfig {
  onUnauthorized?: () => void;
}

/** {Entity} Service — Manages all API operations related to {entities} */
class {Entity}Service {
  private config: {Entity}ServiceConfig;

  constructor(config: {Entity}ServiceConfig = {}) {
    this.config = config;
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    if (response.status === 401) {
      this.config.onUnauthorized?.();
      throw new Error('Unauthorized');
    }
    if (!response.ok) {
      const error = await response.text();
      throw new Error(error || 'Request failed');
    }
    return response.json();
  }

  /** List all {entities} */
  async list(): Promise<{Entity}ListResult> {
    const response = await fetch(`${API_BASE}/list`, { headers: getHeaders(true) });
    return this.handleResponse<{Entity}ListResult>(response);
  }

  /** Get a {entity} by ID */
  async getById(id: number): Promise<{Entity}GetResult> {
    const response = await fetch(`${API_BASE}/getbyid/${id}`, { headers: getHeaders(true) });
    return this.handleResponse<{Entity}GetResult>(response);
  }

  /** Create a new {entity} */
  async insert(data: {Entity}InsertInfo): Promise<{Entity}GetResult> {
    const response = await fetch(`${API_BASE}/insert`, {
      method: 'POST', headers: getHeaders(true), body: JSON.stringify(data),
    });
    return this.handleResponse<{Entity}GetResult>(response);
  }

  /** Update an existing {entity} */
  async update(data: {Entity}UpdateInfo): Promise<{Entity}GetResult> {
    const response = await fetch(`${API_BASE}/update`, {
      method: 'PUT', headers: getHeaders(true), body: JSON.stringify(data),
    });
    return this.handleResponse<{Entity}GetResult>(response);
  }

  /** Delete a {entity} by ID */
  async delete(id: number): Promise<StatusResult> {
    const response = await fetch(`${API_BASE}/delete/${id}`, {
      method: 'DELETE', headers: getHeaders(true),
    });
    return this.handleResponse<StatusResult>(response);
  }
}

export const {entity}Service = new {Entity}Service();
export default {Entity}Service;
```

**Key conventions:**
- Class-based with private `handleResponse` that checks 401 and calls `onUnauthorized`
- `API_BASE` uses `VITE_GOBLIN_API_URL` env var with `http://localhost:4041` fallback
- Always use `getHeaders(true)` for authenticated requests
- Export both singleton instance (camelCase) and class (PascalCase default)

## Step 3: Create Context

**File**: `src/contexts/{Entity}Context.tsx`

The context wraps the service and provides state management with three method categories: **API Methods** (direct service wrappers returning API results), **State Management** (handle loading/error, update local state), and optionally **Utility Methods**.

```typescript
import { createContext, useState, useCallback, ReactNode } from 'react';
import { {entity}Service } from '../services/{entity}Service';
import type {
  {Entity}Info, {Entity}ListResult, {Entity}GetResult,
  {Entity}InsertInfo, {Entity}UpdateInfo, StatusResult,
} from '../types/{entity}';

interface {Entity}ContextType {
  // State
  {entities}: {Entity}Info[];
  selected{Entity}: {Entity}Info | null;
  loading: boolean;
  error: string | null;
  // API Methods (return API results for caller to check sucesso)
  list{Entities}: () => Promise<{Entity}ListResult>;
  get{Entity}ById: (id: number) => Promise<{Entity}GetResult>;
  insert{Entity}: (data: {Entity}InsertInfo) => Promise<{Entity}GetResult>;
  update{Entity}: (data: {Entity}UpdateInfo) => Promise<{Entity}GetResult>;
  delete{Entity}: (id: number) => Promise<StatusResult>;
  // State Management (return void, handle loading/error internally)
  load{Entities}: () => Promise<void>;
  refresh{Entities}: () => Promise<void>;
  setSelected{Entity}: (item: {Entity}Info | null) => void;
  clearError: () => void;
}

const {Entity}Context = createContext<{Entity}ContextType | undefined>(undefined);

export const {Entity}Provider = ({ children }: { children: ReactNode }) => {
  const [{entities}, set{Entities}] = useState<{Entity}Info[]>([]);
  const [selected{Entity}, setSelected{Entity}] = useState<{Entity}Info | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleError = (err: unknown): never => {
    const errorMsg = err instanceof Error ? err.message : 'Unknown error';
    setError(errorMsg);
    throw err;
  };

  // --- API Methods (direct service wrappers) ---

  const list{Entities} = useCallback(async (): Promise<{Entity}ListResult> => {
    try { setError(null); return await {entity}Service.list(); }
    catch (err) { return handleError(err); }
  }, []);

  const get{Entity}ById = useCallback(async (id: number): Promise<{Entity}GetResult> => {
    try { setError(null); return await {entity}Service.getById(id); }
    catch (err) { return handleError(err); }
  }, []);

  const insert{Entity} = useCallback(async (data: {Entity}InsertInfo): Promise<{Entity}GetResult> => {
    try {
      setError(null);
      const result = await {entity}Service.insert(data);
      if (result.sucesso) await load{Entities}();
      return result;
    } catch (err) { return handleError(err); }
  }, []);

  const update{Entity} = useCallback(async (data: {Entity}UpdateInfo): Promise<{Entity}GetResult> => {
    try {
      setError(null);
      const result = await {entity}Service.update(data);
      if (result.sucesso) {
        set{Entities}((prev) => prev.map((item) =>
          item.{entity}Id === data.{entity}Id ? result.{entity} : item
        ));
        if (selected{Entity}?.{entity}Id === data.{entity}Id) setSelected{Entity}(result.{entity});
      }
      return result;
    } catch (err) { return handleError(err); }
  }, [selected{Entity}]);

  const delete{Entity} = useCallback(async (id: number): Promise<StatusResult> => {
    try {
      setError(null);
      const result = await {entity}Service.delete(id);
      if (result.sucesso) {
        set{Entities}((prev) => prev.filter((item) => item.{entity}Id !== id));
        if (selected{Entity}?.{entity}Id === id) setSelected{Entity}(null);
      }
      return result;
    } catch (err) { return handleError(err); }
  }, [selected{Entity}]);

  // --- State Management ---

  const load{Entities} = useCallback(async (): Promise<void> => {
    try {
      setLoading(true);
      setError(null);
      const result = await {entity}Service.list();
      if (result.sucesso) set{Entities}(result.{entities});
      else throw new Error(result.mensagem || 'Failed to load {entities}');
    } catch (err) { handleError(err); }
    finally { setLoading(false); }
  }, []);

  const refresh{Entities} = useCallback(async () => { await load{Entities}(); }, [load{Entities}]);
  const clearError = useCallback(() => { setError(null); }, []);

  const value: {Entity}ContextType = {
    {entities}, selected{Entity}, loading, error,
    list{Entities}, get{Entity}ById, insert{Entity}, update{Entity}, delete{Entity},
    load{Entities}, refresh{Entities}, setSelected{Entity}, clearError,
  };

  return <{Entity}Context.Provider value={value}>{children}</{Entity}Context.Provider>;
};

export default {Entity}Context;
```

**Key conventions:**
- `handleError` sets error state AND re-throws (returns `never`)
- After insert: reload full list. After update: update item in local state. After delete: remove from local state.
- Check `result.sucesso` before updating state
- Export provider as named export, context as default export

## Step 4: Create Hook

**File**: `src/hooks/use{Entity}.ts`

```typescript
import { useContext } from 'react';
import {Entity}Context from '../contexts/{Entity}Context';

/** Custom hook to access the {Entity} context. Throws if used outside {Entity}Provider. */
export const use{Entity} = () => {
  const context = useContext({Entity}Context);
  if (!context) throw new Error('use{Entity} must be used within a {Entity}Provider');
  return context;
};

export default use{Entity};
```

Only add computed values/derived state if the user specifically requests it.

## Step 5: Register Provider in main.tsx

**File**: `src/main.tsx`

```typescript
// Add import at the top with other provider imports
import { {Entity}Provider } from './contexts/{Entity}Context.tsx'

// Add to the provider chain based on dependencies:
// - If it depends on AuthContext → must be inside AuthProvider
// - If it depends on GoblinContext → must be inside GoblinProvider
// - If independent → place near the end, before App
```

**Nesting rules:**
- `AuthProvider` is always the outermost (all contexts depend on auth)
- Place the new provider **as close to `<App />`** as possible unless it has dependents
- If other contexts will depend on this one, place it above those contexts
- Keep related contexts grouped (economy, gameplay, admin, etc.)

**Current provider order:**
```
AuthProvider → FinanceProvider → GoblinProvider → TeamProvider →
GoboxProvider → AuctionProvider → GLogProvider → QuestProvider →
ItemProvider → ItemClaimProvider → MiningProvider → MapProvider →
TerritoryProvider → TerritoryEnemyProvider → ArenaProvider → App
```

## Naming Convention Reference

| Item | Convention | Example |
|------|-----------|---------|
| Types file | `src/types/{entity}.ts` | `src/types/clan.ts` |
| Service file | `src/services/{entity}Service.ts` | `src/services/clanService.ts` |
| Service class | `{Entity}Service` | `ClanService` |
| Service instance | `{entity}Service` | `clanService` |
| Context file | `src/contexts/{Entity}Context.tsx` | `src/contexts/ClanContext.tsx` |
| Provider | `{Entity}Provider` | `ClanProvider` |
| Hook file | `src/hooks/use{Entity}.ts` | `src/hooks/useClan.ts` |
| Hook function | `use{Entity}` | `useClan` |
| Entity ID field | `{entity}Id` | `clanId` |
| List/Get result | `{Entity}ListResult` / `{Entity}GetResult` | `ClanListResult` / `ClanGetResult` |
| Insert/Update DTO | `{Entity}InsertInfo` / `{Entity}UpdateInfo` | `ClanInsertInfo` / `ClanUpdateInfo` |

## Verification Checklist

- [ ] Types file at `src/types/{entity}.ts` with all interfaces
- [ ] Service file at `src/services/{entity}Service.ts` with class pattern
- [ ] Context file at `src/contexts/{Entity}Context.tsx` with provider
- [ ] Hook file at `src/hooks/use{Entity}.ts` with null-check
- [ ] Provider imported and added to `src/main.tsx` in correct nesting position
- [ ] All API response types include `sucesso`, `mensagem`, `erros` fields
- [ ] All context methods use `useCallback`
- [ ] `handleError` pattern: sets error state + re-throws
- [ ] No `any` types, no `alert()`, no `window.confirm()`
- [ ] Service uses `getHeaders(true)` and `VITE_GOBLIN_API_URL` env var

## Common Gotchas

- **StatusResult may already exist**: Check `src/types/map.ts` or other type files before redefining. Import from existing file if available.
- **Entity ID naming**: Always use `{entity}Id` (camelCase), not `{entity}_id` or `id`.
- **API response keys are Portuguese**: `sucesso` (not `success`), `mensagem` (not `message`), `erros` (not `errors`).
- **Service constructor config**: Always include `onUnauthorized` callback in config interface.
- **Provider nesting order matters**: A context cannot use hooks from providers nested inside it.
