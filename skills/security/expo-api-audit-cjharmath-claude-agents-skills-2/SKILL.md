---
name: expo-api-audit
description: "Comprehensive audit of Expo/React Native app API integration layer. Use when asked to: (1) Review API interactions, auth handling, or token management, (2) Find hardcoded data or screens bypassing API, (3) Verify user interactions properly sync to backend, (4) Analyze offline behavior and caching, (5) Audit Orval/OpenAPI code generation, (6) Check for API security issues. Supports TanStack Query, Zustand, axios, Expo Router, expo-secure-store, and expo-constants patterns."
---

# Expo API Integration Audit

## Overview

This skill audits an Expo (React Native) TypeScript app's API integration layer to identify gaps, hardcoded data, auth issues, and offline behavior problems. Designed for apps using Expo Router, expo-secure-store, and expo-constants.

## Inputs

Before starting, gather from the user:
- **Known issues** (optional): Specific screens or flows suspected to be broken
- **Output format preference**: markdown report, JSON findings, fix PRs, or task list
- **Scope**: Full audit or specific focus (auth only, offline only, etc.)

## Tool Note: ripgrep

If `rg` (ripgrep) is available, use it instead of `grep`—it's significantly faster and automatically ignores node_modules/.git. All grep commands in this skill have rg equivalents:

```bash
# Check if ripgrep is available
which rg && echo "Use rg commands" || echo "Falling back to grep"

# Equivalents:
# grep -rn "pattern" --include="*.ts" | grep -v node_modules
# rg "pattern" -t ts

# grep -rln "pattern" --include="*.ts" | grep -v node_modules  
# rg -l "pattern" -t ts
```

## Phase 1: Discovery

Build a mental model before auditing. Run these commands to locate key files:

```bash
# Orval config and generated hooks
find . -name "orval.config.*" -o -name "*.orval.ts" 2>/dev/null | head -5
find . -type d -name "generated" | xargs -I{} ls {} 2>/dev/null | head -20

# API client/mutator
rg -l "customInstance|axios\.create|baseURL" -t ts | head -10

# Zustand stores
rg -l "create\(" -t ts | xargs rg -l "zustand|devtools" 2>/dev/null | head -20

# OpenAPI spec
find . -name "openapi.json" -o -name "openapi.yaml" -o -name "swagger.json" 2>/dev/null

# Auth infrastructure
rg -l "TokenManager|refreshToken|Bearer|interceptor" -t ts

# Expo config (environment variables, API URLs)
cat app.config.js 2>/dev/null || cat app.config.ts 2>/dev/null || cat app.json
rg "expoConfig|Constants\.manifest" -t ts
```

### Key File Mapping

| Component | Typical Location | What to Check |
|-----------|------------------|---------------|
| Orval config | `orval.config.ts` | client type, mutator path, output dir |
| Generated hooks | `/api/generated/` or `/src/api/` | completeness vs OpenAPI spec |
| Axios client | `/api/` or `/services/` | interceptors, base config |
| Token manager | `/services/auth/` | must use `expo-secure-store` |
| Zustand stores | `/stores/` | which hold server state (violation?) |
| OpenAPI spec | `/docs/api/` or root | last modified, version |
| Expo config | `app.config.js` or `app.json` | API URLs in `extra`, env vars |
| Screens | `/app/` (Expo Router) | file-based routing |

## Phase 2: API Layer Audit

### 2.1 Orval Generation Health

```bash
# Check if generated code matches spec
npx orval --dry-run 2>&1 | head -50

# Compare endpoint counts
jq '.paths | keys | length' docs/api/openapi.json  # endpoints in spec
find ./api/generated -name "*.ts" -exec grep -l "useQuery\|useMutation" {} \; | wc -l
```

Verify:
- [ ] Generated types match OpenAPI schemas
- [ ] All spec endpoints have corresponding hooks
- [ ] Custom mutator injects auth headers
- [ ] Query defaults sensible (staleTime, gcTime, retry)

### 2.2 Auth Token Handling

Inspect the axios client for these patterns:

```typescript
// REQUIRED: Request interceptor injects token
config.headers.Authorization = `Bearer ${token}`

// REQUIRED: Pre-emptive refresh before expiry
if (tokenExpiresWithin(600)) await refreshToken()

// REQUIRED: 401 response triggers refresh
if (error.response?.status === 401) { /* refresh logic */ }

// REQUIRED: Refresh deduplication
if (isRefreshing) return pendingRefreshPromise

// REQUIRED: Failed refresh triggers logout
clearTokens(); navigate('/auth')
```

**Expo-specific checks:**

```bash
# Token storage - MUST use expo-secure-store, not AsyncStorage
rg "AsyncStorage.*token|token.*AsyncStorage" -t ts -i  # BAD if found
rg "SecureStore|expo-secure-store" -t ts               # GOOD - should exist

# Environment variables - should use expo-constants or app.config.js
rg "process\.env\." -t ts                              # BAD for Expo (won't work in production)
rg "Constants\.expoConfig|Constants\.manifest" -t ts   # GOOD - Expo way
grep -l "extra:" app.config.* 2>/dev/null              # Config-based env vars
```

**Red flags:**
- Hardcoded tokens or API keys in source
- Tokens in AsyncStorage (must use `expo-secure-store`)
- API URLs using `process.env` (use `expo-constants` instead)
- No refresh deduplication (parallel refresh calls)
- Infinite refresh loops (refresh endpoint returns 401)
- Race conditions between token check and request

### 2.3 Direct API Violations

Find calls bypassing Orval-generated hooks:

```bash
# Raw fetch (should use generated hooks)
rg "fetch\(" -t ts -t tsx --glob '!*.d.ts'

# Direct axios (should use orval mutator)
rg "axios\.|axios\(" -t ts -t tsx --glob '!*orval*'

# Manual useQuery (should use generated)
rg "useQuery\(|useMutation\(" -t ts -t tsx --glob '!*generated*'

# Hardcoded URLs
rg "https?://[^\"']*api" -t ts -t tsx

# Expo-specific: process.env usage (won't work in Expo production builds)
rg "process\.env\." -t ts -t tsx  # Should use Constants.expoConfig.extra instead
```

Classify each finding:
- **Legitimate**: Third-party APIs, file uploads, WebSocket
- **Violation**: Backend calls not using generated hooks
- **Hardcoded**: URLs that should use `expo-constants`
- **Env error**: `process.env` usage (breaks in Expo production)

## Phase 3: Screen Data Audit

For each screen in `/app/` (Expo Router) or `/screens/`:

### 3.1 Data Source Classification

| Category | Pattern | Status |
|----------|---------|--------|
| API Data | `useGet*()`, `use*Query()` | ✓ Correct |
| Cached | React Query serving stale | ✓ Expected |
| Zustand | Business data in store | ⚠️ Should be server state? |
| Hardcoded | Mock arrays, placeholder objects | ❌ Flag |
| Derived | Calculations from API data | ⚠️ Check if backend should compute |

```bash
# Find screens with no API hooks (suspicious)
for f in $(find ./app -name "*.tsx" | grep -v "_layout"); do
  if ! grep -q "use.*Query\|use.*Mutation\|useGet\|usePost\|usePut\|useDelete" "$f"; then
    echo "NO API HOOKS: $f"
  fi
done

# Find hardcoded arrays/objects (rg version)
rg "useState\(\[" -t tsx
rg "const.*=.*\[\{" -t tsx
```

### 3.2 User Interaction Audit

Every user action that modifies data must trigger a mutation:

| Action Type | Required Pattern |
|-------------|------------------|
| Form submit | `useMutation` + `onSuccess` invalidation |
| Toggle/switch | Mutation or debounced mutation |
| Delete | Mutation with optimistic update or confirmation |
| Drag/reorder | Mutation on drop |
| Settings change | Mutation (not just Zustand) |

```bash
# Forms without mutations (suspicious)
for f in $(rg -l "onSubmit|handleSubmit" -t tsx); do
  if ! rg -q "useMutation|usePost|usePut|usePatch" "$f"; then
    echo "FORM WITHOUT MUTATION: $f"
  fi
done

# Button handlers to audit
rg "onPress=|onClick=" -t tsx | head -50
```

### 3.3 Zustand Store Audit

Zustand should hold **client-only** state. Flag if stores contain:
- Data that should come from API (users, items, records)
- Business logic calculations (should be server-side)
- Duplicates of React Query cache

```bash
# List all Zustand stores and their state shape
rg "interface.*State|type.*State" stores/ -t ts

# Check for persist middleware (may duplicate RQ cache)
rg "persist\(" stores/ -t ts
```

**Valid Zustand uses**: auth state, UI preferences, navigation state, draft forms
**Invalid**: fetched entities, computed business data, anything with an API endpoint

## Phase 4: Offline Behavior Audit

### 4.1 Network Mode Configuration

```bash
# Check query client defaults
rg "networkMode" -t ts

# Check for offline detection (Expo supports both)
rg "NetInfo|@react-native-community/netinfo" -t ts    # Community package
rg "expo-network|Network\.getNetworkStateAsync" -t ts  # Expo native package
rg "isConnected|isInternetReachable" -t ts
```

Expected patterns:
- Queries: `networkMode: 'offlineFirst'` (serve stale when offline)
- Mutations: `networkMode: 'online'` or queue implementation

### 4.2 Offline Scenarios to Test

| Scenario | Expected Behavior | Check |
|----------|-------------------|-------|
| Load screen offline | Shows cached data or empty state | `isLoading` vs `isFetching` |
| Submit form offline | Queue or clear error message | Mutation error handling |
| Token refresh offline | Graceful failure, retry on reconnect | Interceptor error path |
| App backgrounded then offline | Cache persists | AsyncStorage/MMKV check |
| Reconnect after offline | Automatic refetch | `refetchOnReconnect` |

```bash
# Check for offline queue implementation
rg "offlineQueue|pendingMutations|syncQueue" -t ts

# Check cache persistence
rg "persistQueryClient|createAsyncStoragePersister|MMKV" -t ts
```

### 4.3 Error Boundary Coverage

```bash
# Find error boundaries
rg "ErrorBoundary|errorElement|onError" -t tsx

# Check query error handling
rg "isError|error:" -t tsx | head -30
```

## Phase 5: Report Generation

Structure findings by severity:

### Critical (Auth/Security)
- Hardcoded credentials
- Tokens in AsyncStorage (must use `expo-secure-store`)
- `process.env` for secrets (won't work in Expo builds)
- Auth bypass possibilities
- Missing 401 handling

### Major (Data Integrity)
- Forms not syncing to API
- User actions not persisted
- Business logic in frontend
- Stale data served as fresh
- API URLs not using `expo-constants`

### Medium (Reliability)
- Missing error handling
- No offline fallback
- Race conditions
- Missing loading states

### Minor (Code Quality)
- Direct API calls (should use generated)
- Zustand holding server state
- Inconsistent patterns

## Output Templates

### Markdown Report
```markdown
# API Integration Audit Report

## Executive Summary
- X critical issues, Y major, Z medium

## Findings

### [CRITICAL] Tokens Stored in AsyncStorage
**File**: `services/auth/tokenStorage.ts:15`
**Issue**: JWT tokens stored in AsyncStorage instead of expo-secure-store
**Fix**: Migrate to `import * as SecureStore from 'expo-secure-store'`

### [CRITICAL] process.env in Production Code
**File**: `api/client.ts:8`
**Issue**: `process.env.API_URL` won't work in Expo production builds
**Fix**: Use `Constants.expoConfig?.extra?.apiUrl` from expo-constants

### [MAJOR] Profile Form Not Syncing
**File**: `app/profile/edit.tsx`
**Issue**: Form saves to Zustand only, no API call
**Fix**: Add `useUpdateProfile` mutation on submit
```

### JSON Findings
```json
{
  "summary": { "critical": 2, "major": 2, "medium": 5 },
  "findings": [
    {
      "severity": "critical",
      "category": "auth",
      "file": "services/auth/tokenStorage.ts",
      "line": 15,
      "issue": "Tokens in AsyncStorage instead of expo-secure-store",
      "fix": "Migrate to SecureStore.setItemAsync/getItemAsync"
    },
    {
      "severity": "critical", 
      "category": "config",
      "file": "api/client.ts",
      "line": 8,
      "issue": "process.env.API_URL won't work in Expo builds",
      "fix": "Use Constants.expoConfig.extra.apiUrl"
    }
  ]
}
```

## Quick Reference Commands

```bash
# Full audit (grep version)
echo "=== Direct fetch ===" && grep -rn "fetch(" --include="*.ts" --include="*.tsx" | grep -v node_modules | grep -v ".d.ts"
echo "=== Direct axios ===" && grep -rn "axios\." --include="*.ts" --include="*.tsx" | grep -v node_modules | grep -v orval
echo "=== Hardcoded URLs ===" && grep -rn "http://\|https://" --include="*.ts" --include="*.tsx" | grep -v node_modules
echo "=== useState arrays ===" && grep -rn "useState\(\[" --include="*.tsx" | grep -v node_modules
echo "=== Forms ===" && grep -rn "onSubmit" --include="*.tsx" | grep -v node_modules
```

```bash
# Full audit (ripgrep version - much faster)
echo "=== Direct fetch ===" && rg "fetch\(" -t ts -t tsx --glob '!*.d.ts'
echo "=== Direct axios ===" && rg "axios\." -t ts -t tsx --glob '!*orval*'
echo "=== Hardcoded URLs ===" && rg "https?://" -t ts -t tsx
echo "=== useState arrays ===" && rg "useState\(\[" -t tsx
echo "=== Forms ===" && rg "onSubmit" -t tsx
```

## Dependencies

If commands fail, install:
```bash
# ripgrep (highly recommended - 10x faster than grep)
brew install ripgrep  # or apt-get install ripgrep, cargo install ripgrep

# jq for JSON parsing
brew install jq  # or apt-get install jq

# For Orval dry-run
npm install -g orval  # or use npx
```

## Installation

To use this skill with Claude Code, add it to your project's `skills/` directory:

```
my-expo-app/
├── app/                          # Expo Router screens
├── stores/
├── api/
├── skills/
│   └── expo-api-audit/
│       └── SKILL.md
├── app.config.js                 # Expo config
├── package.json
└── ...
```

Claude Code auto-discovers skills in this directory. Once installed, trigger the audit with prompts like:
- "Run an API integration audit"
- "Check for hardcoded data in my screens"
- "Audit my auth token handling"
- "Find forms that aren't syncing to the API"
- "Check if I'm using expo-secure-store correctly"
