---
name: edge-function-generator
description: Expert assistant for creating and maintaining Supabase Edge Functions for the KR92 Bible Voice project. Use when (1) creating new Edge Functions, (2) setting up CORS and error handling, (3) integrating shared modules from _shared/, (4) adding JWT validation, (5) configuring environment variables, (6) auditing or updating dependency versions across functions. Triggers include "edge function", "create function", "serverless", "deno function", "update edge imports", "version drift".
---

# Edge Function Generator

## Context Files

Read from `Docs/context/` for project-specific patterns:
- `supabase-map.md` - Edge Functions list and structure
- `db-schema-short.md` - Database tables for queries

## Centralized Dependencies

**All Edge Functions import from `_shared/deps.ts`** - never use direct URLs:

```typescript
import { serve, createClient, corsHeaders, crypto } from "../_shared/deps.ts";
```

The deps.ts module centralizes all versions (deno std@0.190.0, supabase-js@2.49.1) and includes the XHR polyfill as a side-effect import. See [references/versions.md](references/versions.md) for rationale and `Docs/ops/edge-deps-standardization.md` for upgrade instructions.

## Edge Function Structure

```
supabase/functions/
├── _shared/              # Shared modules (import with ../_shared/)
│   ├── deps.ts           # Centralized dependencies - import from here!
│   ├── ai-config.ts
│   ├── ai-prompt.ts
│   ├── ai-providers.ts
│   └── ai-quota.ts
├── function-name/
│   └── index.ts
```

## Minimal Template

```typescript
import { corsHeaders, createClient, serve } from "../_shared/deps.ts";

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const supabaseKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    const supabase = createClient(supabaseUrl, supabaseKey);

    // Your logic here

    return new Response(
      JSON.stringify({ success: true }),
      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { headers: { ...corsHeaders, "Content-Type": "application/json" }, status: 500 }
    );
  }
});
```

## With JWT Authentication

```typescript
// Get user from JWT
const authHeader = req.headers.get("Authorization");
if (!authHeader) {
  return new Response(JSON.stringify({ error: "Unauthorized" }), {
    status: 401,
    headers: { ...corsHeaders, "Content-Type": "application/json" },
  });
}

const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  global: { headers: { Authorization: authHeader } },
});

const { data: { user }, error: authError } = await supabase.auth.getUser();
if (authError || !user) {
  return new Response(JSON.stringify({ error: "Invalid token" }), {
    status: 401,
    headers: { ...corsHeaders, "Content-Type": "application/json" },
  });
}
```

## With AI Integration

```typescript
// deps.ts already imports XHR polyfill as side-effect
import { corsHeaders, createClient, serve } from "../_shared/deps.ts";
import { getFeatureConfig } from "../_shared/ai-config.ts";
import { getPrompt } from "../_shared/ai-prompt.ts";
import { callProvider } from "../_shared/ai-providers.ts";
import { enforceQuotaOrThrow } from "../_shared/ai-quota.ts";

// Check quota before AI call
await enforceQuotaOrThrow(featureKey, estimatedTokens, userId);

// Get config and prompt from DB
const config = await getFeatureConfig(featureKey, "prod");
const prompt = await getPrompt(featureKey, variables, "prod");

// Call AI provider
const response = await callProvider({
  vendor: config.vendor,
  model: config.model,
  systemPrompt: prompt.systemPrompt,
  userPrompt: prompt.userPrompt,
  params: config.params,
});
```

## Version Audit Workflow

When auditing for stray direct imports:

```bash
# Should return ONLY deps.ts - no other files should have direct URLs
grep -r "deno.land/std@" supabase/functions/ | grep -v deps.ts
grep -r "esm.sh/@supabase" supabase/functions/ | grep -v deps.ts
```

If any function has direct imports, update it to use `../\_shared/deps.ts` instead. See [references/versions.md](references/versions.md) for version rationale.

## Deployment

```bash
# Deploy single function
supabase functions deploy function-name

# Deploy via MCP
mcp__supabase__deploy_edge_function
```

## Testing

```bash
# Local testing
supabase functions serve function-name

# cURL test
curl -X POST https://PROJECT.supabase.co/functions/v1/function-name \
  -H "Authorization: Bearer ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
```
